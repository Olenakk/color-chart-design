import orthonormal_vectors_csv_creator
import numpy as np 

from orthonormal_vectors_csv_creator  import *

#Test with a matrix where the last 31 entries are orthogonal vectors 
def test_selection_of_orthonormal_vectors(): 
    I = np.eye(31)
    I[-1,:] *= 2
    B = np.zeros((100, 31))
    B[:,0] = 1
    C = np.concatenate([B, I], axis = 0)
    selected_indexes, selected_vectors = select_orthonormal_vectors(C, 24)

    return selected_indexes, selected_vectors

def main(): 
    selected_indexes, selected_vectors = test_selection_of_orthonormal_vectors()
    print(selected_vectors)
    print(selected_indexes)

# Run the main function
if __name__ == "__main__":
    main()