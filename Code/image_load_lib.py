#image_load_lib.py

from PIL import Image
import numpy as np 
 
#super pixel method decreases the resolution by 1/4.
#Gives accurate value of intensity because there is no interpolation.
def debayer_superpixel(cfa_input):
    #gbrg CFA is used in GoPro Hero 10
    r = cfa_input[1::2, 0::2]
    g1 = cfa_input[0::2, 0::2]
    g2 = cfa_input[1::2, 1::2]
    g = (g1+g2)/2
    b = cfa_input[0::2, 1::2]

    #combine r,g,b channel to get 3 channel (R,G,B) image
    rgb_image = np.stack((r,g,b), axis=2)    

    return rgb_image


def load_image(image_name, map_color=False):
    raw_data = Image.open(image_name)
    raw = np.array(raw_data).astype(np.double)

    #camera parameters
    black = 12 #Least amount of darkness camera can record
    white = 4095 #Max value camera can record for each sub-pixel. So 2^12 = 4095 => 12 bit per sub-pixel.

    #convert the intensity values to [0,1] range
    if map_color:
        raw = (raw - black)/(white-black)
        raw = np.clip(raw, 0, 1)
        
    return debayer_superpixel(raw)

def rotate_image_180(image):
    return image[::-1,::-1]
