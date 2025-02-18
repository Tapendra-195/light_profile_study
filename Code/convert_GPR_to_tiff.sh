#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <image path> [output directory]"
    exit 1
fi

input_image_name=$1

output_directory="."

if [ $# -ge 2 ]; then
    output_directory="$2"
fi


output_image_name=$(basename "$input_image_name")
let length=${#output_image_name}
length=$((length-3))
output_image_name=${output_image_name:0:length}
output_image_name+="DNG"

output_image_name="$output_directory$output_image_name"
echo " "
echo "imput image = $input_image_name"
echo "saving $output_image_name"
echo " "

gpr_tools -i $input_image_name -o $output_image_name

echo "saving tiff image"
dcraw -4 -D -T $output_image_name

echo "removing $output_image_name"
rm $output_image_name
