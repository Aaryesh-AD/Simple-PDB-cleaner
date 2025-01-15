#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDB_processor.py
Simple PDB file cleaning script using Biopython.
Dependencies: Biopython (pip install biopython) or (conda install conda-forge::biopython)

Author: Aaryesh Deshpande (aaryeshad@gmail.com)
Date: 01-14-2025
"""

# Import Modules

import os
import argparse
from Bio.PDB import PDBParser, PDBIO

# Suppress PDB warnings
import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)

# List of standard amino acids and common protonation variants
aal_prot = {
    "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "ILE", 
    "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL",
    "ASH", "GLH", "HIE", "HID", "HIP", "LYN", "CYX", "CYM", "TYM"
}

# Function Definitions
# Removes water molecules from the structure
def remove_water(structure):
    """Remove water molecules from the structure."""
    for model in structure:
        for chain in list(model):
            for residue in list(chain):
                if residue.get_resname() == "HOH":
                    chain.detach_child(residue.id)
    return structure

# Keeps only standard protein residues in the structure
def keep_only_protein(structure):
    """Keep only standard protein residues in the structure."""
    for model in structure:
        for chain in list(model):
            for residue in list(chain):
                if residue.get_resname() not in aal_prot:
                    chain.detach_child(residue.id)
    return structure

# Removes specified heteroatoms from the structure
def remove_heteroatoms(structure, hetatm_set):
    """Remove specified heteroatoms from the structure."""
    for model in structure:
        for chain in list(model):
            for residue in list(chain):
                if residue.get_resname() in hetatm_set:
                    chain.detach_child(residue.id)
    return structure

# Extracts residues from the structure and returns as a list of dictionaries
def get_residues(structure):
    """Extract residues from the structure and return as a list of dictionaries."""
    residues = []
    for model in structure:
        for chain in model:
            for residue in chain:
                residues.append({
                    'resname': residue.get_resname(),
                    'resnum': residue.get_id()[1],
                    'chain_id': chain.id,
                    'residue': residue
                })
    return residues

# Splits residues into chains based on chain IDs and separates heteroatoms
def split_residues(residues):
    """Split residues into chains based on chain IDs and separate heteroatoms."""
    chains = {}
    hetero_chains = {}

    for res in residues:
        chain_id = res['chain_id']
        resname = res['resname']

        if resname in aal_prot:
            if chain_id not in chains:
                chains[chain_id] = []
            chains[chain_id].append(res['residue'])
        else:
            if chain_id not in hetero_chains:
                hetero_chains[chain_id] = {}
            if resname not in hetero_chains[chain_id]:
                hetero_chains[chain_id][resname] = []
            hetero_chains[chain_id][resname].append(res['residue'])

    return chains, hetero_chains

# Processes the PDB file by parsing, cleaning, and saving the structure
def process_pdb(input_file, output_file, hetatm_set, keep_protein_only, remove_water_flag):
    """Parse, clean, and save the PDB file."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", input_file)

    # Perform cleaning operations based on flags
    if keep_protein_only:
        structure = remove_water(structure)
        structure = keep_only_protein(structure)
        structure = remove_heteroatoms(structure, hetatm_set)
    else:
        if remove_water_flag:
            structure = remove_water(structure)
        if hetatm_set:
            structure = remove_heteroatoms(structure, hetatm_set)

    # Save the cleaned structure
    io = PDBIO()
    io.set_structure(structure)
    io.save(output_file)

# Argument validation function
def validate_args(args):
    """Validate argument combinations to avoid conflicts."""
    if args.keep_protein_only and args.hetatm:
        raise ValueError("Error: --keep-protein-only cannot be used together with --hetatm.")
    if not args.input or not args.output:
        raise ValueError("Error: Both --input and --output files must be specified.")
    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"Error: Input file '{args.input}' not found.")

# Main Function
def main():
    """Main function to handle argument parsing and execution."""
    parser = argparse.ArgumentParser(description="Clean PDB files by removing water, heteroatoms, and non-protein residues.")
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to the input PDB file.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to save the cleaned PDB file.")
    parser.add_argument("-r", "--hetatm", type=str, nargs="*", default=[], help="List of heteroatoms to remove.")
    parser.add_argument("-p", "--keep-protein-only", action="store_true", help="Remove all non-protein residues and specified heteroatoms. Keeps only protein residues.")
    parser.add_argument("-w", "--remove-water", action="store_true", help="Remove all water molecules from the structure.")

    args = parser.parse_args()

    # Validate arguments
    try:
        validate_args(args)
        process_pdb(args.input, args.output, set(args.hetatm), args.keep_protein_only, args.remove_water)
        print(f"\nSuccessfully processed PDB file '{args.input}' and saved to '{args.output}'.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("\nPDB_processor - Simple PDB file cleaning script using Biopython.")
    print("Author: Aaryesh Deshpande (aaryeshad@gmail.com)")
    main()
