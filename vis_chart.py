import cv2
import argparse
import numpy as np 
import pandas as pd

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="Path to a CSV file with RGB values")
    parser.add_argument("outfile", type=str, help="Path to an output PDF file")
    parser.add_argument("-s", "--shape", nargs=2, type=int, default=[1, -1], help="Shape of the color chart: number rows and columns")
    return vars(parser.parse_args())

def plot_image(I, cli):
    # Normalize I to the range [0, 255] (assuming I contains values in [0, 1])
    I_normalized = (I/I.max()* 255).astype(np.uint8)
    # Reshape the RGB image to a one-dimensional array of pixel values
    # The new shape will have 3 columns representing the RGB channels, and the number of rows will be automatically calculated.
    #image_reshaped = I_normalized.reshape(1, -1, 3)
    image_reshaped = I_normalized.reshape(cli["shape"]+[3])

    cv2.imwrite(cli["outfile"], image_reshaped)
    #GIVE AN OPTION TO RESIZE AN IMAGE (NO NEED TO ZOOM IN)

def main():
    cli = get_cli_args()
    
    I = pd.read_csv(cli["infile"], dtype='float64', #header=None
                    ).values
    I = I**(1/2.2) #Making the image more pleasant to the human eye #ADD AS A VIS_EXPONENT PARAMETER WITH 1 AS A DEFAULT 

    plot_image(I, cli)

if __name__ == '__main__': main()