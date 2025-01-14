# PDB Structure Cleaning and Preprocessing Script

This Python script provides a simple automated approach for cleaning and preprocessing PDB files using Biopython. It allows users to remove water molecules, specific heteroatoms, and non-standard residues, ensuring that the resulting structures are clean and standardized for downstream computational analyses like molecular dynamics (MD) simulations, docking, or structural analysis.

## Features

- **Remove Water Molecules**: Option to remove all water molecules (`HOH, WAT`) from the PDB structure.
- **Selective Heteroatom Removal**: Remove specified heteroatoms (e.g., `PO4`, `SO4`) by providing their residue names.
- **Keep Only Protein Residues**: Retains only standard amino acids and common protonation variants, removing all non-protein residues.
- **Flexible Usage**: Users can apply different cleaning operations based on their specific requirements.

## Requirements

- Python 3.6+
- Biopython

To install Biopython, run:

```
# Using python pip 
pip install biopython

# Using conda
conda install conda-forge::biopython
```

## Usage

Run the script using the following command:

```
python pdb_processor.py -i <input_pdb_file> -o <output_pdb_file> [options]
```

### Command-line Arguments

| Argument                  | Description                                                  |
| ------------------------- | ------------------------------------------------------------ |
| `-i, --input`             | Path to the input PDB file (required).                       |
| `-o, --output`            | Path to save the cleaned PDB file (required).                |
| `-r, --hetatm`            | List of heteroatoms to remove (e.g., `PO4`, `SO4`).          |
| `-p, --keep-protein-only` | Remove all non-protein residues, keeping only protein residues (cannot be used with `--hetatm`). |
| `-w, --remove-water`      | Remove all water molecules from the structure.               |

### Example Usages

1. **Remove water and keep only protein residues**:

   ```
   python pdb_processor.py -i input.pdb -o output_cleaned.pdb -p
   ```

2. **Remove specific heteroatoms (e.g., PO4) and water molecules**:

   ```
   python pdb_processor.py -i input.pdb -o output_no_hetatm.pdb -r PO4 -w
   ```

3. **Error Example**: The following command will raise an error because `--hetatm` and `--keep-protein-only` are incompatible:

   ```
   python pdb_processor.py -i input.pdb -o output_error.pdb -r PO4 -p
   ```

**Error Handling**: Ensures incompatible options are not used together (e.g., `--hetatm` and `--keep-protein-only`).

## Issues and Contributions

If you encounter any issues, discover any bugs, or would like to contribute to the project, feel free to:

1. **Report an Issue**: Open an issue describing the problem in detail, including error messages, input files, and the command used.
2. **Request a Feature**: If you have a feature in mind that would enhance the script, you can create a feature request.
3. **Contribute**: Fork the repository, make your changes, and submit a pull request. Contributions are always welcome, and your support will help improve the project!



Aaryesh Deshpande
*Email*: aaryeshad@gmail.com

