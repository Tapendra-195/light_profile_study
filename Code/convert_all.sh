#!/bin/bash

# Check if the directory is passed as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <input directory> [output directory]"
    exit 1
fi

# Get the directory from the command line argument
INPUT_DIRECTORY=$1
OUTPUT_DIRECTORY=$1

if [ -n "$2" ]; then
    OUTPUT_DIRECTORY=$2
fi

# Check if the provided argument is a directory
if [ ! -d "$INPUT_DIRECTORY" ]; then
    echo "Error: $INPUT_DIRECTORY is not a directory"
    exit 1
fi

# List the files in the directory line by line
for image in "$INPUT_DIRECTORY"/*; do
    if [ -f "$image" ]; then
        ./convert_GPR_to_tiff.sh $image $OUTPUT_DIRECTORY
    fi
done
