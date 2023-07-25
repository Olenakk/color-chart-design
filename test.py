import orthonormal_vectors_csv_creator
import numpy as np 
import pandas as pd
import scipy
import matplotlib.pyplot as plt
from orthonormal_vectors_csv_creator  import *

#Test with a matrix where the last 31 entries are orthogonal vectors 
def test_selection_of_orthonormal_vectors(): 
    I = np.eye(31)
    I[-1,:] *= 2
    B = np.zeros((100, 31))
    B[:,0] = 1
    C = np.concatenate([B, I], axis = 0) * 42
    selected_indexes, selected_vectors = select_orthonormal_vectors(C, 24)

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

def plot_interp_data(xp, fp, pts, data_interp):
    # Plot original and interpolated data
    #plt.figure(figsize=(8, 6))
    plt.plot(xp, fp, label='Original Data', color='blue', marker='.')
    plt.scatter(pts, data_interp, label='Interpolated Data', color='red')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.title('Interpolated Data Visualization')
    plt.grid()
    plt.show()

def main(): 

    selected_indexes, selected_vectors = test_selection_of_orthonormal_vectors()
    orthogonal_matrix = generate_QR_orthogonal_matrix(31)
    print(is_orthogonal(orthogonal_matrix))
    N = insert_zeroth_row_after_each_row(orthogonal_matrix)

    N = pd.DataFrame(N) 
    print(N)
    N.to_csv("test_csv", index=False)

    


# Run the main function
if __name__ == "__main__":
    main()