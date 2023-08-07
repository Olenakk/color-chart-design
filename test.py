import argparse
import ortho_sel
import numpy as np 
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import ortho_sel 
import ortho_defect 

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", type=str, help="Path to an input file") 
    parser.add_argument("-o", "--outfile", type=str, help="Path to an output file")

    cli = vars(parser.parse_args())

    return cli 

#Test with a matrix where the last 31 entries are orthogonal vectors 
##########################################################################
def test_selection_of_orthonormal_vectors(): 
    I = np.eye(31)
    I[-1,:] *= 2
    B = np.zeros((100, 31))
    B[:,0] = 1
    C = np.concatenate([B, I], axis = 0) * 42
    selected_indexes, selected_vectors = ortho_sel.select_orthonormal_vectors(C, 24)

    return selected_indexes, selected_vectors

def generate_orthogonal_matrix(num_rows, num_cols):
    # Generate a random matrix
    random_matrix = np.random.rand(num_rows, num_cols)
    
    # Initialize the orthogonal matrix
    orthogonal_matrix = np.zeros((num_rows, num_cols))
    
    # Process each row
    for i in range(num_rows):
        orthogonal_matrix[i] = random_matrix[i]  # Take the i-th row as is
        
        # Orthogonalize the i-th row with respect to previous rows
        for j in range(i):
            orthogonal_matrix[i] -= np.dot(random_matrix[i], orthogonal_matrix[j]) * orthogonal_matrix[j]
        
        # Normalize the i-th row
        orthogonal_matrix[i] /= np.linalg.norm(orthogonal_matrix[i])
    
    return orthogonal_matrix

def generate_QR_orthogonal_matrix(n):
    while True:
        matrix = np.random.rand(n, n)
        if np.linalg.det(matrix) != 0:
            break

    Q,R = scipy.linalg.qr(matrix)
    return Q.T

def is_orthogonal(matrix):
    num_rows, num_cols = matrix.shape
    
    # Check the dot product of each pair of rows
    for i in range(num_rows):
        for j in range(i + 1, num_rows):
            dot_product = np.dot(matrix[i], matrix[j])
            if not np.isclose(dot_product, 0):
                return False
    
    return True

def insert_zeroth_row_after_each_row(orthogonal_matrix): 
    row_pairs = [(row, orthogonal_matrix[0,:]) for row in orthogonal_matrix]
    N = np.array([row for pair in row_pairs for row in pair])

    return N

#Testing orthogonality defect using an identity matrix 
##########################################################################
def test_ortho_defect_col(): 
    defect = ortho_defect.ortho_defect_col(np.identity(10))
    print(defect)


#Testing the visualization using the normal distribution. 
#Note: should be visualized as colors of the rainbow 
##########################################################################
def gaussian(mu, sigma, N): 
    #x = np.arange(0, N)
    x = np.linspace(0, 1, N)
    #y = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu)**2 / (2 * sigma**2))
    y = np.exp(-(x - mu)**2 / (2 * sigma**2))

    return y 

#Testing rainbow colors (visualization) 
def test_gaus(num, cli_args): 
    outfile = cli_args["outfile"]
    #num - number of normal distributions to be generated 
    #num = 10 
    R = np.array([gaussian(1/num*i, 0.1, 31) for i in range(num+1)])

    for row in R:
        plt.plot(np.linspace(0, 1, 31), row)

    plt.show()
    np.savetxt(outfile, R, delimiter=',', fmt='%.4f')

#Shuffle the dataset to see if it produces the same output 
##########################################################################
def shuffle(cli_args): 
    infile = cli_args["infile"]
    outfile = cli_args["outfile"]
    matrix = pd.read_csv(infile#, header=None
                    ).values
    np.random.shuffle(matrix)
    df = pd.DataFrame(matrix)

    return df 

def main():
    cli_args = get_cli_args()
    matrix = shuffle(cli_args)
    numbers = list(range(400, 701, 10))
    matrix.to_csv(cli_args["outfile"], index=False, header = numbers)


# Run the main function
if __name__ == "__main__":
    main()