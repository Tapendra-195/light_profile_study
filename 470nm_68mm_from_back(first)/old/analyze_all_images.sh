#!/bin/bash                                                                     

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
    echo "running $line"
    python3 analyze.py $line
done < "$filename"
