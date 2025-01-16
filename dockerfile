# Use a smaller base image
FROM python:3.12-slim

# Metadata labels
LABEL Script_name="PDB_processor.py"
LABEL Description="This script processes PDB files and extracts the information of the atoms and residues."
LABEL Version="0.0.1"
LABEL Build_date="2025-01-15"
LABEL Maintainer="Aaryesh Deshpande"

# Set environment variable to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install biopython directly (pip comes pre-installed with python:slim images)
RUN pip install --no-cache-dir biopython

# Working directory set
WORKDIR /data

# Copy the script to the container
COPY PDB_processor.py /Script_dir/

# Entrypoint set
ENTRYPOINT ["python3", "/Script_dir/PDB_processor.py"]

# Set the default command to run the script
CMD ["python3", "/Script_dir/PDB_processor.py"]

