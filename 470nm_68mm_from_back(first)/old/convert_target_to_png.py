import sys
from PIL import Image
import image_load_lib as image_lib
import numpy as np

OUTPUT_DIRECTORY = "./target/"

def main():
    IMAGE_DIRECTORY = "./target/"
    image_name = sys.argv[1]
    
    image = image_lib.load_image(IMAGE_DIRECTORY+image_name, True)
    
    
    output_image_name = OUTPUT_DIRECTORY+image_name[:-4]+"png"
    scaled_matrix = (image * 255).astype(np.uint8)
    image = Image.fromarray(scaled_matrix)

    image.save(output_image_name)


    return

if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    main()
