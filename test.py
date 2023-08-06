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
    parser.add_argument("outfile", type=str, help="Path to an output file")

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
    x = np.arange(0, N)
    y = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu)**2 / (2 * sigma**2))

    return y 

def main():
    cli_args = get_cli_args()
    outfile = cli_args["outfile"]

    R = np.array([gaussian(10*i, 50, 31) for i in range(50)])

    print(R.shape)
    selected_indexes, selected_vectors = ortho_sel.select_orthonormal_vectors(R, 24)
    ortho_sel.create_csv_file(outfile, R, selected_indexes)

# Run the main function
if __name__ == "__main__":
    main()