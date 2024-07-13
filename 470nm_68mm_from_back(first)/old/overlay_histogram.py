import matplotlib.pyplot as plt
import numpy as np
import sys

INPUT_DIRECTORY = "./outputs/"

def read_filenames(filename):
    with open(filename, 'r') as file:
        filenames = [line.strip() for line in file.readlines()]
    return filenames

def read_data_from_file(filename):
    X = []
    weights = []
    distance = -1
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            distance = float(parts[1])
            X.append(float(parts[2]))
            weights.append(float(parts[3]))
    return X, weights, distance

def overlay_histograms(filenames, x_label):
    plt.figure(figsize=(10, 6))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'black', 'purple', 'orange', 'pink', 'brown', 'lime',  'tomato']

    
    for i in range(len(filenames)):
        #        plot_cos_theta_with_weights(filenames[i])
        X, weights, distance = read_data_from_file(filenames[i])
        plt.hist(X, weights = weights, bins=49, alpha=0.5, label=f'd= {distance}', color=colors[i%len(colors)], histtype='step')
        #    for i, filename in enumerate(filenames):
        #       data = read_data_from_file(filename)
        #      
    plt.xlabel(x_label)
    plt.ylabel('Intensity')
    plt.title( x_label+' vs intensity')
    plt.legend(loc='upper left')
    plt.show()

    
def main():
    #filename contins text file containing names of individual histogram
    if len(sys.argv) < 3:
        print("Usage: python3 overlay_histogram.py <filename> <x_axis_label>")
        sys.exit(1)
        
    filename = sys.argv[1]
    x_label = sys.argv[2]
    filenames = read_filenames(filename) 

    print(filenames)

    overlay_histograms(filenames, x_label)
        
    
if __name__ == "__main__":
    main()
