#!/bin/bash
#######################################################################
# ./convert_all.sh <filename = text file containing names of gpr images> #
#######################################################################

readonly INPUT_DIRECTORY="./image_raw"
readonly OUTPUT_DIRECTORY="./image_tiff"

# Check if a filename is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename=$1

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File $filename not found."
    exit 1
fi

# Read the file line by line
while IFS= read -r line;
do
     ./convert_GPR_to_tiff.sh $line $INPUT_DIRECTORY $OUTPUT_DIRECTORY
done < "$filename"
