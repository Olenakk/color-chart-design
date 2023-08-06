import argparse
import numpy as np 
import pandas as pd 
import glob 
from pathlib import Path

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("matfolder", type=str, help="Path to a folder that includes all the matrices to be compared")
    parser.add_argument("outfile", type=str, help="Path to a CSV file with sorted matnames by their orthogonality")
    parser.add_argument("-i", "--index", action="store_true", help="Ignore the first column of the provided reflectances data (that might include indices)" )
    cli = vars(parser.parse_args())

    # Use glob to extract files from the matfolder
    matfolder = cli["matfolder"]
    matfiles = glob.glob(matfolder)

    return cli, matfiles

def ortho_defect_col(matrix):
    print("value of the determinant", np.linalg.det(matrix.T @ matrix))
    return np.prod(np.linalg.norm(matrix, axis=0)) / np.sqrt(abs(np.linalg.det(matrix.T @ matrix))) #Olena messes up here: Some determinans were negative, so I added an absolute value
    
def main(): 
    # Get command-line arguments
    cli_args, matfiles = get_cli_args()
    outfile = cli_args["outfile"]

    for matfile in matfiles: 
        matrix = pd.read_csv(matfile#, header=None
                        ).values
        
        #Code for ignoring the first column of the reflectances data 
        if cli_args["index"]: # Check if the index flag is present
            matrix = pd.read_csv(matfile, dtype='float64', usecols=range(1,matrix.shape[1]), #header=None, 
                            ).values
            
        #Normalizing the matrix
        matrix /= np.linalg.norm(matrix, axis=1).reshape(-1,1)

        #Calculating the orthogonality defect 
        defect = ortho_defect_col(matrix)
        print(f"Orthogonal defect for the {Path(matfile).stem} is: ", defect)



    
    
    
if __name__ == "__main__": main()     
