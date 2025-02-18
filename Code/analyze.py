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

def circle(image, a, b, radius, thickness):
    a = round(a)
    b = round(b)
    radius = math.ceil(radius)

    indices = np.indices(image.shape)
    distance_from_center = np.sqrt((a - indices[1])**2 + (b - indices[0])**2)
        
    if thickness == -1:
        circle_mask = distance_from_center <= radius
        image[circle_mask] = 1.0

    elif thickness > 0:
        ring_mask = (distance_from_center >= radius) & (distance_from_center < radius+thickness)
        image[ring_mask] = 1.0

def rect(image, bottom_left, top_right, thickness = 1):
    # Extract coordinates of the two diagonal points of rectangle
    min_x = bottom_left[0]
    max_x = top_right[0]
    min_y = top_right[1]
    max_y = bottom_left[1]
    
    #min_x, min_y = bottom_left
    #max_x, max_y = top_right
        
    # Create an array of indices
    indices = np.indices(image.shape)

    horizontal_line_mask = (indices[1] > min_x-thickness) & (indices[1] < max_x+thickness)&(((indices[0] > min_y-thickness) & (indices[0] < min_y) ) | ((indices[0] > max_y) & (indices[0] < max_y+thickness)))

    vertical_line_mask = (indices[0] > min_y-thickness) & (indices[0] < max_y+thickness)&(((indices[1] < min_x) & (indices[1] > min_x-thickness)) | ((indices[1] > max_x) & (indices[1] < max_x+thickness)))

    rectangle_mask = horizontal_line_mask | vertical_line_mask 
    
    # Set values outside the rectangular region to 0
    image[rectangle_mask] = 1.0
          
    
                        
# Define Gaussian function
def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x - mean) / stddev)**2 / 2)

def fit_gaussian(data, weights, initial_guess, label, image_name, number_of_bins):
    hist, bins, _ = plt.hist(data, bins=number_of_bins, range=None, density=None, weights=weights)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    
    params, covariance = curve_fit(gaussian, bin_centers, hist, p0=initial_guess)

    plt.plot(bin_centers, gaussian(bin_centers, *params), color='red', label='Gaussian Fit')

    plt.xlabel(label)
    plt.ylabel('Intensity')
    plt.title(label+'_vs_Intensity')

    output_filename = OUTPUT_DIRECTORY+image_name+"_"+label+"_vs_Intensity.pdf"
    print("saving")
    print(output_filename)
    # Annotate the fit parameters on the plot
    fit_label = f'A = {params[0]:.2f} \n$\mu$={params[1]:.2f} \n$\sigma$={params[2]:.2f}'
    plt.text(0.75, 0.8, fit_label, fontsize=12, ha='left', transform=plt.gca().transAxes)

    plt.savefig(output_filename)
    plt.close()

    return params


def find_spot_center(image_gray, image_name):
    image_width = image_gray.shape[1]
    image_height = image_gray.shape[0]

    x = []
    y = []
    intensity = [] 
    cutoff = int((image_width-image_height)/2)
    for j in range(image_height):
        for i in range(image_height):#image_width):
            x.append(i+cutoff)
            y.append(j)
            intensity.append(image_gray[j][i+cutoff])
           
    print(image_height)
    #2D histogram
    plt.hist2d(x, y, bins=image_height, range=None, density=None, weights=intensity)
    plt.colorbar()
    plt.xlabel('u')
    plt.ylabel('v')
    plt.title('u_v_vs_Intensity')
    plt.savefig(OUTPUT_DIRECTORY+image_name+"_u_v_vs_Intensity.png")
    plt.close()

    #Fitting
    initial_guess = [1, image_width/2 , 1]    
    params_x = fit_gaussian(x, intensity, initial_guess, "u", image_name, image_height)

    initial_guess = [params_x[0], image_height/2 , params_x[2]]    
    params_y = fit_gaussian(y, intensity, initial_guess, "v", image_name, image_height)

    mean_x = params_x[1]
    mean_y = params_y[1]
    sigma_x = math.fabs(params_x[2]) #Since gaussian i am using has sigma^2, fit doesn't care if sigma is positive or negative.
    sigma_y = math.fabs(params_y[2])

    FWHM_x = sigma_x * 2.355
    FWHM_y = sigma_y * 2.355
    
    return (mean_x, mean_y), (FWHM_x, FWHM_y)

def rgb_to_gray(rgb_image):
    r = rgb_image[:,:,0]
    g = rgb_image[:,:,1]
    b = rgb_image[:,:,2]

    image_gray = (r+g+b)/3
    
    return np.array(image_gray)


def px_to_cm(p):
    return interp_func(p)

def save_to_text(image_name, distance, X, Y, x_label):
    output_filename = OUTPUT_DIRECTORY+image_name+"_dis_"+str(distance)+"_"+x_label+"_and_weights.txt"

    print("saving "+output_filename)

    f = open(output_filename, "w")
    for i in range(len(X)):
        f.write(str(image_name) + "\t" + str(distance) + "\t" + str(X[i]) + "\t" + str(Y[i]) + "\n")
 
    f.close()

def get_cos_theta_and_weights(image_gray, center, radius, distance):
    a = round(center[0])
    b = round(center[1])
    radius = round(radius)
    base = distance
    p0 = px_to_cm((a,b))
    
    cos_thetas = []
    weights = []
    for j in range(2*radius+1):
        for i in range(2*radius+1):
            x = i+a-radius
            y = j+b-radius
            if (x-a)**2+(y-b)**2<=radius**2:
                p = px_to_cm((x,y))
                dp = (p[0]-p0[0], p[1]-p0[1])
                perpendicular = math.sqrt(dp[0]**2 + dp[1]**2)
                hypotenuse = math.sqrt(perpendicular**2 + base**2)
                cos_theta = base/hypotenuse

                cos_thetas.append(cos_theta)
                weights.append(image_gray[y][x])

    return cos_thetas, weights

def plot_theta_vs_intensity(cos_thetas, weights, distance,  image_name, number_of_bins = 100):
                           
    hist, bins, _ = plt.hist(cos_thetas, bins=number_of_bins, weights=weights)
   
    plt.xlabel("cos(theta)")
    plt.ylabel('Intensity')
    plt.title('cos(theta)_vs_Intensity, d = '+str(distance) + " cm")

    output_filename = OUTPUT_DIRECTORY+image_name+"_dis_"+str(distance)+"_cos(theta)_vs_Intensity.pdf"
    print("saving")
    print(output_filename)
    plt.savefig(output_filename)
    plt.close()


    output_filename = OUTPUT_DIRECTORY+image_name+"_dis_"+str(distance)+"_cos(theta)_vs_Intensity_graph.pdf"
    print("saving")
    print(output_filename)
    plt.plot(cos_thetas, weights, '.')
    plt.xlabel("cos(theta)")
    plt.ylabel('Intensity')
    plt.title('cos(theta)_vs_Intensity, d = '+str(distance)+ " cm")
    plt.savefig(output_filename)
    plt.close()


def get_phi_and_weights(image_gray, center, radius):
    a = round(center[0])
    b = round(center[1])
    radius = round(radius)
    p0 = px_to_cm((a,b))
    
    phis = []
    weights = []
    for j in range(2*radius+1):
        for i in range(2*radius+1):
            x = i+a-radius
            y = j+b-radius
            if (x-a)**2+(y-b)**2<=radius**2:
                p = px_to_cm((x,y))
                dp = (p[0]-p0[0], p[1]-p0[1])
                phi = np.arctan2(dp[1], dp[0])
                phis.append(phi)
                weights.append(image_gray[y][x])

    return phis, weights


    
def plot_phi_vs_intensity(phis, weights, distance,  image_name, number_of_bins = 100):
    hist, bins, _ = plt.hist(phis, bins=number_of_bins, weights=weights)
   
    plt.xlabel("phi")
    plt.ylabel('Intensity')
    plt.title('phi_vs_Intensity, d = '+str(distance) + " cm")

    output_filename = OUTPUT_DIRECTORY+image_name+"_dis_"+str(distance)+"_phi_vs_Intensity.pdf"
    print("saving")
    print(output_filename)
    plt.savefig(output_filename)
    plt.close()


    output_filename = OUTPUT_DIRECTORY+image_name+"_dis_"+str(distance)+"_phi_vs_Intensity_graph.pdf"
    print("saving")
    print(output_filename)
    plt.plot(phis, weights, '.')
    plt.xlabel("phi")
    plt.ylabel('Intensity')
    plt.title('phi_vs_Intensity, d = '+str(distance)+ " cm")
    plt.savefig(output_filename)
    plt.close()


    
def initialize_interpolator(filename = "interpolation.txt"):
    print("loading interpolator with " + filename)
    
    u_v_points = []
    x_y_points = []
    global interp_func
    bottom_left = (0,0)
    top_right = (0,0)
    min_x = 100
    min_y = 100
    max_x = 0
    max_y = 0
    with open(TARGET_DIRECTORY+filename) as fp:
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

            if x<=min_x and y<=min_y:
                min_x = x
                min_y = y
                bottom_left = (u,v)
                
            if x>=max_x and y>=max_y:
                max_x = x
                max_y = y
                top_right = (u,v)
                
    interp_func = LinearNDInterpolator(u_v_points, x_y_points)

    return bottom_left, top_right



#sets points outside the rectangle to 0
def set_outside_to_zero(image, bottom_left, top_right):
    # Extract coordinates of the two diagonal points of rectangle
    min_x = bottom_left[0]
    max_x = top_right[0]
    min_y = top_right[1]
    max_y = bottom_left[1]

    # Create an array of indices
    indices = np.indices(image.shape)

    # Set values outside the rectangular region to 0
    image[(indices[0] < min_y) | (indices[0] > max_y) | (indices[1] < min_x) | (indices[1] > max_x)] = 0
    


def is_circle_contained_in_rect(circle, rect):
    a = circle[0]
    b = circle[1]
    r = circle[2]

    bottom_left = rect[0]
    top_right = rect[1]
    min_x = bottom_left[0]
    max_x = top_right[0]
    min_y = top_right[1]
    max_y = bottom_left[1]

    if a-r >= min_x and a+r <= max_x and b-r >= min_y and b+r <= max_y:
        return True
    else:
        return False

def main():
    EXPECTED_ARGV = 3
    if len(sys.argv) != (EXPECTED_ARGV+1):
        print("python3 analyze.py <image name> <distance> <directory>")
        sys.exit(1)
    
    image_name = sys.argv[1]
    distance = float(sys.argv[2])
    DIRECTORY = sys.argv[3]
    print("distance = ")
    print(distance)
    
    #Background image
    background_name = DIRECTORY+"background/background.tiff" #sys.argv[2]
   

    
    print(DIRECTORY)
    global INPUT_DIRECTORY
    global OUTPUT_DIRECTORY
    global TARGET_DIRECTORY
    
    INPUT_DIRECTORY = DIRECTORY+"image_tiff/"
    OUTPUT_DIRECTORY = DIRECTORY+"outputs/"
    TARGET_DIRECTORY = DIRECTORY+"target/"

    
    
    #*****************************************#
    # 1. Loading and initialization section   # 
    #*****************************************#
    #rectangular region of target
    #interpolation only valid in this region
    '''
    a-------b
    |       |
    c-------d
    '''

    bottom_left, top_right = initialize_interpolator() #interpolation.txt contains (u, v, x, y)
    
    
    print("loading image " + image_name)
    image_rgb = image_lib.load_image(INPUT_DIRECTORY+image_name)
    print("loading background image " + background_name)
    image_background = image_lib.load_image(background_name)

    image_spot = image_rgb - image_background #remove background
    image_spot = image_lib.rotate_image_180(image_spot)     #original image was taken with camera upside down
    image_gray = rgb_to_gray(image_spot)

    set_outside_to_zero(image_gray, bottom_left, top_right)
    
    #************************************#
    # 2. Finding source center section   # 
    #************************************#
    center, FWHM = find_spot_center(image_gray, image_name[:-5])
    

    #************************************#
    # 3.      Plotting section           # 
    #************************************#
    radius = min(FWHM[0],FWHM[1])/2
        
    print("center = " + str(center))
    print("FWHM = " + str(FWHM))
    print("radius(1/2 FWHM) = " + str(radius))

    cos_thetas, weights = get_cos_theta_and_weights(image_gray, center, 2*radius, distance)
    number_of_bins = 100
    plot_theta_vs_intensity(cos_thetas, weights, distance,  image_name[:-5], number_of_bins)

    save_to_text(image_name[:-5], distance, cos_thetas, weights, "cos(theta)")

    #phi data
    phi, weights = get_phi_and_weights(image_gray, center, 2*radius)
    number_of_bins = 100
    plot_phi_vs_intensity(phi, weights, distance,  image_name[:-5], number_of_bins)

    save_to_text(image_name[:-5], distance, phi, weights, "phi")

    #plot_phi_vs_intensity(image_gray, center, radius)
            
    #************************************#
    # 3.  showing radius section         # 
    #************************************#
    image_circled = image_lib.load_image(INPUT_DIRECTORY+image_name, True)
    image_circled = image_lib.rotate_image_180(image_circled)     #original image was taken with camera upside down
    
    output_image_name = OUTPUT_DIRECTORY+image_name[:-4]+"png"
    circle(image_circled, center[0], center[1], 2*radius, 5)
    rect(image_circled, bottom_left, top_right, 5)
    scaled_matrix = (image_circled * 255).astype(np.uint8)
    image = Image.fromarray(scaled_matrix)

    image.save(output_image_name)

    if is_circle_contained_in_rect((center[0], center[1], 2*radius), (bottom_left, top_right)):
        print("circle contained inside rect")
    else:
        print("circle not contained inside rect")


#    print(image_rgb1[round(center[1])][round(center[0])])
    return

if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    main()
