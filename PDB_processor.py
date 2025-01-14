# Import Modules

import os
import argparse
import string
from Bio.PDB import PDBParser, PDBIO, Chain, Residue

# Suppress PDB warnings
import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)