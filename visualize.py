import cv2
import argparse
import numpy as np 
import pandas as pd 

def get_cli_args():
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description=
        """
        Takes as input reflectances, light, and standard observer and 
        produces a visualization of the provided reflectances
        """
        )

    # Add command-line arguments
    parser.add_argument("refl", type=str, help="Path to the CSV file containing reflectances data")
    parser.add_argument("lt", type=str, help="Path to the CSV file containing light data")
    parser.add_argument("obs", type=str, help="Path to the CSV file containing the CIE Standard Observer data")
    parser.add_argument("o", type=str, help="Path to the output CSV file")
    parser.add_argument("-i", "--index", action="store_true", help="Ignore the first column of the provided reflectances data (that might include indices)" )
    parser.add_argument("--rows", type=int, help="Indicates the number of rows in a color chart")
    parser.add_argument("--cols", type=int, help="Indicates the number of columns in a color chart")
    
    # Parse the command-line arguments
    cli = vars(parser.parse_args())

    return cli 

def calc_RGB(R, L, S): 
    num_rows, num_cols = R.shape
    R_L = R*L.reshape((1,num_cols))
    I = R_L@S.T

    return I

def reshape_colorchart(rows, cols, img):
    return img.reshape(rows, cols, 3)

def plot_image(I, cli_args):
    # Normalize I to the range [0, 255] (assuming I contains values in [0, 1])
    I_normalized = (I/I.max()* 255).astype(np.uint8)
    # Reshape the RGB image to a one-dimensional array of pixel values
    # The new shape will have 3 columns representing the RGB channels, and the number of rows will be automatically calculated.
    image_reshaped = I_normalized.reshape(1, -1, 3)

    if cli_args["rows"] and cli_args["cols"]:
        image_reshaped = reshape_colorchart(cli_args["rows"], cli_args["cols"], image_reshaped)
        print(image_reshaped.shape)

    # Save the reshaped RGB image to a file using imwrite
    cv2.imwrite(cli_args["o"], image_reshaped)

def main(): 
    # Get command-line arguments
    cli_args = get_cli_args()

    R = pd.read_csv(cli_args["refl"], dtype='float64', #header=None
                    ).values

    #Ignore the first column of the reflectances data 
    if cli_args["index"]: # Check if the index flag is present
       R = pd.read_csv(cli_args["refl"], dtype='float64', usecols=range(1,R.shape[1]), #header=None, 
                       ).values
          
    L = pd.read_csv(cli_args["lt"], dtype='float64', #header=None
                    ).values
    
    S = pd.read_csv(cli_args["obs"], dtype='float64', #header=None
                    ).values

    R /= np.linalg.norm(R, axis=1).reshape(-1,1)
    I = calc_RGB(R, L, S)
    
    plot_image(I, cli_args)

if __name__ == "__main__":  main()