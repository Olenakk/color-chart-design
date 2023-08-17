import argparse
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

def get_cli_args():
    # Create an argument parser
    parser = argparse.ArgumentParser()
    # Add command-line arguments
    parser.add_argument("ground_truth", type=str, help="Path to the CSV file with groud truth")
    parser.add_argument("reflectances", type=str, help="Path to the CSV file containing reflectances data")
    parser.add_argument("light", type=str, help="Path to the CSV file containing light data")
    #parser.add_argument("observer", type=str, help="Path to the CSV file containing the CIE Standard Observer data")
    parser.add_argument("-i", "--index", action="store_true", help="Ignore the first column of the provided reflectances data (that might include indices)" )

    cli = vars(parser.parse_args())

    return cli 
#Adjust noise based on intensity 
def calc_RGB_error(R_L, S, noise_intensity): 
    #num_rows, num_cols = R.shape
    I = R_L@S.T 

    #Adding ramdom noise to the colors
    noise = np.random.normal(0, noise_intensity, I.shape)
    I = I + noise

    S_hat, residuals, RANK, sing = np.linalg.lstsq(R_L, I, rcond=None)

    return np.linalg.norm(S - S_hat)

def main(): 
    cli_args = get_cli_args()

    S = pd.read_csv(cli_args["ground_truth"], dtype="float64", #header=None
                           ).values
    
    R = pd.read_csv(cli_args["reflectances"], dtype="float64", #header=None
                    ).values
    
    L = pd.read_csv(cli_args["light"], dtype = 'float64', #header=None
                    ).values

    #Ignore the first column of the reflectances data 
    if cli_args["index"]: # Check if the index flag is present
       #R = pd.read_csv(cli_args["reflectances"], dtype='float64', usecols=range(1,R.shape[1]), #header=None, 
       #                ).values
       R = R[:,1:]

    num_reps = 1000
    resolution = 100
    max_noise = 10000.0
    R_L = R*L.reshape((1,-1))   
    intensities = np.linspace(0, max_noise, resolution)
    errors = np.array([[calc_RGB_error(R_L, S, ni) for ni in intensities] for _ in range(num_reps)]).mean(axis=0)
    
    plt.plot(intensities, errors)
    plt.show()

if __name__ == "__main__": main()