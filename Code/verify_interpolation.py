#!/usr/bin/env python
import sys,os
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from scipy.stats import norm
from scipy.optimize import curve_fit
import math
from scipy.interpolate import LinearNDInterpolator
import image_load_lib as image_lib

def put_pixel(image, x,y,color):
    x= round(x)
    y= round(y)
    image[y][x] = [color[0], color[1], color[2]]

def circle(image, a, b, radius, color):
    a = round(a)
    b = round(b)
    for j in range(2*radius+1):
        for i in range(2*radius+1):
            x = i+a-radius
            y = j+b-radius
            if(x>=0 and y>=0 and x<=image.shape[1] and y <= image.shape[0]):
                if (x-a)**2+(y-b)**2<=radius**2:
                    put_pixel(image, x,y,color)


def initialize_interpolator(INTERPOLATION_PATH):
    u_v_points = []
    x_y_points = []
    with open(INTERPOLATION_PATH) as fp:
        max_x = 0
        max_y = 0
        for line in fp:
            u,v,x,y = line.split()
            u = float(u)
            v = float(v)
            x = float(x)
            y = float(y)


            u = int(u)
            v = int(v)
            x = int(x)
            y = int(y)
            u_v_points.append([u,v])
            x_y_points.append([x,y])
            if x>max_x:
                max_x = x
            if y>max_y:
                max_y =y
                
    interp_func = LinearNDInterpolator(x_y_points, u_v_points)
    global rows
    global cols
    rows = max_y + 1
    cols = max_x + 1
    
    return interp_func

                    
def main():
    EXPECTED_ARGV = 2
    if len(sys.argv) != (EXPECTED_ARGV+1):
        print("python3 verify_interpolation.py <image path> <interpolation path>")
        sys.exit(1)


    image_name = sys.argv[1]
    INTERPOLATION_PATH = sys.argv[2]
        
    image_rgb = image_lib.load_image(image_name, True)
    image_rgb = image_lib.rotate_image_180(image_rgb)     #original image was taken with camera upside down

    #initialize interpolator
    interp_func = initialize_interpolator(INTERPOLATION_PATH)
    

    original_points = []
    x_center = []
    y_center = []
    square_center = []
    
    for j in range(rows):
        for i in range(cols):
            original_points.append(interp_func([i,j]))
            circle(image_rgb, interp_func([i,j])[0][0] ,interp_func([i,j])[0][1], 5, (1.0,0,0))
            if i<cols-1 :
                x_center.append(interp_func([i+0.5,j]))
                circle(image_rgb, interp_func([i+0.5,j])[0][0] ,interp_func([i+0.5,j])[0][1], 5, (0,1.0,0))
            if j < rows-1:
                y_center.append(interp_func([i,j+0.5]))
                circle(image_rgb, interp_func([i,j+0.5])[0][0] ,interp_func([i,j+0.5])[0][1], 5, (0,0,1.0))
            if i<cols-1 and j < rows-1:
                square_center.append(interp_func([i+0.5,j+0.5]))
                circle(image_rgb, interp_func([i+0.5,j+0.5])[0][0] ,interp_func([i+0.5,j+0.5])[0][1], 5, (1.0,1.0,.0))



    #put_pixel(image_rgb1, center[0], center[1], (1,1.0,1))
    scaled_matrix = (image_rgb * 255).astype(np.uint8)
    image = Image.fromarray(scaled_matrix)

    output_image_name = image_name[:-5]+"_verify_interpolation.png"
    
    image.save(output_image_name)

    return

if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    main()
