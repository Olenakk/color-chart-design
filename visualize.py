import cv2
import argparse
import numpy as np 
import pandas as pd 

def get_cli_args():
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description=
        """
        Takes as input 
        """
        )

    # Add command-line arguments
    parser.add_argument("refl", type=str, help="Path to the CSV file containing reflectances data")
    parser.add_argument("lt", type=str, help="Path to the CSV file containing light data")
    parser.add_argument("obs", type=str, help="Path to the CSV file containing the CIE Standard Observer data")
    parser.add_argument("o", type=str, help="Path to the output CSV file")
    parser.add_argument("-cols", type=int, help="Not sure what to write!!")
    parser.add_argument("-rows", type=int, help="not sure what to say")

    # Parse the command-line arguments
    cli = vars(parser.parse_args())

    return cli 

def calc_RGB(R, L, S): 
    num_rows, num_cols = R.shape
    R_L = R*L.reshape((1,num_cols))
    I = R_L@S.T

    return I

def plot_image(I, cli_args):
    # Normalize I to the range [0, 255] (assuming I contains values in [0, 1])
    I_normalized = (I/I.max()* 255).astype(np.uint8)
    # Reshape the RGB image to a one-dimensional array of pixel values
    # The new shape will have 3 columns representing the RGB channels, and the number of rows will be automatically calculated.
    print(I_normalized)
    image_reshaped = I_normalized.reshape(1, -1, 3)

    # Save the reshaped RGB image to a file using imwrite
    cv2.imwrite(cli_args["o"], image_reshaped)

def main(): 
    # Get command-line arguments
    cli_args = get_cli_args()
    
    R = pd.read_csv(cli_args["refl"], dtype='float64', header=None).values
    L = pd.read_csv(cli_args["lt"], dtype='float64', header=None).values
    S = pd.read_csv(cli_args["obs"], dtype='float64', header=None).values

    I = calc_RGB(R, L, S)
    
    plot_image(I, cli_args)

if __name__ == "__main__":  main()