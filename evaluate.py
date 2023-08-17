import argparse
import numpy as np 
import pandas as pd 
import toml
import matplotlib.pyplot as plt

import select_refls 


def get_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("reflectances", type=str, help="Path to a CSV file with reflectances")
    parser.add_argument("light", type=str, help="Path to a CSV file with light")
    parser.add_argument("outfile", type=str, help="Path to a toml file with metrix values") #MAKE THIS OPTIONAL, DUMP STATS IN THE TERMINAL 
    parser.add_argument("-i", "--index", action="store_true", help="Ignore the first column of the provided reflectances data (that might include indices)" )
    parser.add_argument("-p", "--plot", action="store_true", help="Plot singular values for each row" )
    cli = vars(parser.parse_args())

    return cli

def ortho_defect_col(R):
    """
    Calculate the orthogonality defect of a matrix based on its columns.
    Parameters:
    matrix (numpy.ndarray): Input matrix for which the orthogonality defect is computed.
    Returns:
    float: Orthogonality defect value.
    """
    print("value of the determinant", np.linalg.det(R.T @ R), R.shape)
    ortho_defect = np.prod(np.linalg.norm(R, axis=0)) / np.sqrt(abs(np.linalg.det(R.T @ R))) 
    return ortho_defect

#NO NEED TO RUN THE SELECTION AGAIN, JUST LOOK AT 1ST ROW, 2 ROWS, 3 ROWS, AND SO ON.. 

# Perform row-wise orthogonal selection and calculate the orthogonality defect for each
def seq_ortho_defect(R):
    #print([R[:i+1].shape for i in range(R.shape[0])] )
    #print([np.linalg.norm(R[:i+1]) for i in range(R.shape[0])] )
    seq_ortho = [ortho_defect_col(R[:(i+1)].T) for i in range(R.shape[0])]
    #for i in range(1, num+1): 
    #    selected_indexes = select_refls.greedy_cosmin(R, L, i)
    #    original_selected_vectors = np.array(R[selected_indexes])
    #    ortho_defect = ortho_defect_col(original_selected_vectors.T)
    #    seq_ortho.append(ortho_defect)

    return seq_ortho

def calc_sing_values(R): 
    U, S, Vh = np.linalg.svd(R, full_matrices=True)

    return S

def plot_singular_values(sing_values):
    plt.plot(sing_values, marker='o')
    plt.xlabel("Row")
    plt.ylabel("Singular Value")
    plt.title("Singular Values")
    plt.grid(True)
    plt.show()

def main(): 
    # Get command-line arguments
    cli = get_cli()

    R = pd.read_csv(cli["reflectances"]#, header=None
                    ).values
    
    L = pd.read_csv(cli["light"]#, header=None
                    ).values
    
    #Code for ignoring the first column of the reflectances data 
    if cli["index"]: # Check if the index flag is present
        R = pd.read_csv(cli["reflectances"], dtype='float64', usecols=range(1,R.shape[1]), #header=None, 
                        ).values
        
    #Normalizing the matrix
    R /= np.linalg.norm(R, axis=1).reshape(-1,1)

    #Calculating metrix for the reflectances matrix
    ortho_defect = ortho_defect_col(R.T)
    seq_ortho = seq_ortho_defect(R*L)
    sing_values = calc_sing_values(R) 

    if cli["plot"]: 
        plot_singular_values(sing_values)

    # Create a dictionary to store the results
    results = {
        "ortho_defect": ortho_defect,
        "seq_ortho": seq_ortho,
        "sing_values": sing_values
    }

    # Save results to a TOML file
    with open(cli["outfile"], "w") as toml_file:
        toml.dump(results, toml_file)

    
if __name__ == "__main__": main()     
