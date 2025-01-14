# Import Modules

import os
import argparse
import string
from Bio.PDB import PDBParser, PDBIO, Chain, Residue

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

def remove_water(structure):
    """Remove water molecules from the structure."""
    for model in structure:
        for chain in list(model):
            for residue in list(chain):
                if residue.get_resname() == "HOH":
                    chain.detach_child(residue.id)
    return structure

def keep_only_protein_residues(structure):
    """Keep only standard protein residues in the structure."""
    for model in structure:
        for chain in list(model):
            for residue in list(chain):
                if residue.get_resname() not in aal_prot:
                    chain.detach_child(residue.id)
    return structure

def remove_heteroatoms(structure, hetatm_set):
    """Remove specified heteroatoms from the structure."""
    for model in structure:
        for chain in list(model):
            for residue in list(chain):
                if residue.get_resname() in hetatm_set:
                    chain.detach_child(residue.id)
    return structure

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

def process_pdb(input_file, output_file, hetatm_set):
    """Parse, clean, and save the PDB file."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", input_file)

    # Remove water, keep only protein residues, and remove specified heteroatoms
    structure = remove_water(structure)
    structure = keep_only_protein_residues(structure)
    structure = remove_heteroatoms(structure, hetatm_set)

    # Extract and split residues
    residues = get_residues(structure)
    chains, hetero_chains = split_residues(residues)

    # Save the cleaned structure
    io = PDBIO()
    io.set_structure(structure)
    io.save(output_file)

# Main Function
def main():
    """Main function to handle argument parsing and execution."""
    parser = argparse.ArgumentParser(description="Clean PDB files by removing water, heteroatoms, and non-protein residues.")
    parser.add_argument("-i","--input", type=str, help="Path to the input PDB file.")
    parser.add_argument("-o","--output", type=str, help="Path to save the cleaned PDB file.")
    parser.add_argument("-r","--hetatm", type=str, nargs="*", default=["PO4"], help="List of heteroatoms to remove.")
    parser.add_argument("-p","--keep-protein-only", action="store_true", help="Remove all non-protein residues except specified heteroatoms.(If added). Keeps only protein residues.")
    parser.add_argument("-w","--remove-water", action="store_true", help="Remove all water molecules from the structure.")

    args = parser.parse_args()

    # Process the PDB file with provided options
    process_pdb(args.input, args.output, set(args.hetatm), args.keep_protein_only, args.remove_water)

if __name__ == "__main__":
    print("\nPDB_processor - Simple PDB file cleaning script using Biopython.")
    print("Author: Aaryesh Deshpande (aaryeshad@gmail.com)")
    main()