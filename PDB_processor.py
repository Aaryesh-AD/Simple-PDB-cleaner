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
