#!/bin/bash

input_image_name=$1

input_directory="."
output_directory="."


if [ $# -ge 2 ]; then
    input_directory="$2"
    output_directory="$3"
    echo "Input directory: $input_directory"
    echo "Output directory: $output_directory"
else
    echo "Input directory: $input_directory"
    echo "Output directory: $output_directory"
fi

let length=${#input_image_name}
length=$((length-3))

output_image_name=${input_image_name:0:length}
output_image_name+="DNG"

output_image_name="$output_directory/$output_image_name"
input_image_name="$input_directory/$input_image_name"

echo "imput image = $input_image_name"

echo "saving $output_image_name"
gpr_tools -i $input_image_name -o $output_image_name

echo "saving tiff image"
dcraw -4 -D -T $output_image_name

echo "removing $output_image_name"
rm $output_image_name
