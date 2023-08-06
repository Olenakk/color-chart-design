import argparse
import numpy as np 
import pandas as pd 

def get_cli_args():
    # Create an argument parser
    parser = argparse.ArgumentParser()
    # Add command-line arguments
    parser.add_argument("refl", type=str, help="Path to the CSV file containing reflectances data")
    parser.add_argument("lt", type=str, help="Path to the CSV file containing light data")
    parser.add_argument("obs", type=str, help="Path to the CSV file containing the CIE Standard Observer data")
    parser.add_argument("-i", "--index", action="store_true", help="Ignore the first column of the provided reflectances data (that might include indices)" )

    cli = vars(parser.parse_args())

    return cli 

def calc_RGB(R, L, S): 
    num_rows, num_cols = R.shape
    
    R_L = R*L.reshape((1,num_cols))
    I = R_L@S.T 

    #Adding ramdom noise to the colors
    noise = np.random.normal(0, .1, I.shape)
    I = I + noise

    return I, R_L

def main(): 
    cli_args = get_cli_args()

    R = pd.read_csv(cli_args["refl"], dtype="float64", #header=None
                    ).values
    
    L = pd.read_csv(cli_args["lt"], dtype = 'float64', #header=None
                    ).values
    
    S = pd.read_csv(cli_args["obs"], dtype = 'float64', #header=None
                    ).values

    #Ignore the first column of the reflectances data 
    if cli_args["index"]: # Check if the index flag is present
       R = pd.read_csv(cli_args["refl"], dtype='float64', usecols=range(1,R.shape[1]), #header=None, 
                       ).values

    I, R_L = calc_RGB(R, L, S)
    S_hat, residuals, RANK, sing = np.linalg.lstsq(R_L, I, rcond=None)

    print(S.T - S_hat)


if __name__ == "__main__": main()