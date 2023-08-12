import cv2
import argparse
import numpy as np 
import pandas as pd

from fpdf import FPDF

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="Path to a CSV file with RGB values")
    parser.add_argument("outfile", type=str, help="Path to an output PDF file")
    parser.add_argument("-s", "--shape", nargs=2, type=int, default=[1, -1], help="Shape of the color chart: number rows and columns")
    return vars(parser.parse_args())

def reshape_colorchart(rows, cols, img):
    return img.reshape(rows, cols, 3)

def plot_image(I, cli):
    # Normalize I to the range [0, 255] (assuming I contains values in [0, 1])
    I_normalized = (I/I.max()* 255).astype(np.uint8)
    # Reshape the RGB image to a one-dimensional array of pixel values
    # The new shape will have 3 columns representing the RGB channels, and the number of rows will be automatically calculated.
    image_reshaped = I_normalized.reshape(1, -1, 3)

    if cli["shape"]: 
        rows, cols = cli["shape"]
        image_reshaped = reshape_colorchart(rows, cols, image_reshaped)

    #Save the reshaped RGB image to a file using imwrite
    cv2.imwrite(cli["outfile"], image_reshaped)
    cv2.namedWindow('Color Chart', cv2.WND_PROP_ASPECT_RATIO)
    cv2.setWindowProperty('Color Chart', cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Color Chart', image_reshaped)
    cv2.waitKey(0)

    return image_reshaped
    
def main():
    cli = get_cli_args()
    outfile = cli["outfile"]
    
    I = pd.read_csv(cli["infile"], dtype='float64', #header=None
                    ).values
    I = I**(1/2.2) #Making the image more pleasant to the human eye 

    plot_image(I, cli)
    
    cv2.destroyAllWindows()

    

if __name__ == '__main__': main()