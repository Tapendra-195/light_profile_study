import matplotlib.pyplot as plt
import numpy as np
import sys


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

def overlay_histograms(filenames, x_label, x_min, x_max, n_bins):
    plt.figure(figsize=(10, 6))
    colors = [
        'red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 
        'black', 'orange', 'purple', 'brown', 'pink', 
        'lime', 'olive', 'navy', 'teal'
    ]


    #colors = ['b', 'g', 'r', 'c', 'm', 'y', 'black', 'purple', 'orange', 'pink', 'brown', 'lime',  'tomato']

    
    for i in range(len(filenames)):
        #        plot_cos_theta_with_weights(filenames[i])
        X, weights, distance = read_data_from_file(DIRECTORY+filenames[i])

        hist, bin_edges = np.histogram(X, bins=n_bins, range=(x_min, x_max), weights=weights)
        # Find the index of the bin closest to x=0.95
        print(bin_edges)
        index = np.abs(bin_edges - 0.9996).argmin()
        # Calculate the height of the bin at x=0.95
        target_bin_height = hist[index]
        # Normalize the histogram heights by dividing by the height at x=0.95
        normalized_hist = hist / target_bin_height
        # Plot the normalized histogram
        plt.hist(bin_edges[:-1], bins=bin_edges, weights=normalized_hist, alpha=0.5, 
                 label=f'd= {distance}', color=colors[i % len(colors)], histtype='step')



        #plt.hist(X, weights = weights, bins=n_bins, range = (x_min, x_max), alpha=0.5, label=f'd= {distance}', color=colors[i%len(colors)], histtype='step')
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
    if len(sys.argv) < 4:
        print("Usage: python3 overlay_histogram.py <file path> <histogram directory> <x_axis_label>")
        sys.exit(1)

    global DIRECTORY
    filename = sys.argv[1]
    DIRECTORY = sys.argv[2]
    x_label = sys.argv[3]
    filenames = read_filenames(filename) 
    
    
    print(filenames)
    x_min= 0.988;
    x_max = 1.0
    n_bin = 50
    overlay_histograms(filenames, x_label,x_min,x_max, n_bin)
        
    
if __name__ == "__main__":
    main()
