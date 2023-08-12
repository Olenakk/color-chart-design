import cv2
import numpy as np 
import pandas as pd 
import argparse

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("reflectances", type=str, help="Path to reflectances data base in the CSV format")
    parser.add_argument("light", type=str, help="Path to ligth CSV file")
    parser.add_argument("sensitivity", type=str, help="Path to CSV file with camera sensitivity or observer")
    parser.add_argument("outfile", type=str, help="Path to the output CSV file")
    parser.add_argument("-i", "--index", action="store_true", help="Ignore the first column of the provided reflectances data (that might include indices)" )
    return vars(parser.parse_args())

def calc_GBR(R, L, S): 
    num_rows, num_cols = R.shape
    R_L = R*L.reshape((1,num_cols))
    I = R_L@S.T

    return I

def calc_GBR_uniform(R, S): 
    I = R@S.T

    return I 

def main():
    cli = get_cli_args()

    R = pd.read_csv(cli["reflectances"], dtype='float64', #header=None
                    ).values

    #Ignore the first column of the reflectances data 
    if cli["index"]: # Check if the index flag is present
       R = pd.read_csv(cli["reflectances"], dtype='float64', usecols=range(1,R.shape[1]), #header=None, 
                       ).values
          
    L = pd.read_csv(cli["light"], dtype='float64', #header=None
                    ).values
    
    S = pd.read_csv(cli["sensitivity"], dtype='float64', #header=None
                    ).values

    #R /= np.linalg.norm(R, axis=1).reshape(-1,1) #Remove normalization - distorts visualization 
    I_GBR = calc_GBR(R, L, S)
    I_RGB = np.concatenate([I_GBR[:, i].reshape(-1, 1) for i in [2,1,0]], axis=1)

    np.savetxt(cli["outfile"], I_RGB, header="R,G,B", delimiter = ",", fmt='%.4f', comments='')

    


if __name__ == '__main__': main()