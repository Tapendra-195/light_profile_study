#!/bin/bash                                                                     

# Check if a filename is provided as an argument                                                                                              
if [ $# -lt 2 ]; then
    echo "Usage: $0 <filename> <directory>"
    exit 1
fi

filename=$1
DIRECTORY=$2

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File $filename not found."
    exit 1
fi

# Read the file line by line
while IFS= read -r line;
do
    echo "running $line"
    python3 analyze.py $line $DIRECTORY
done < "$filename"
