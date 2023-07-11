import argparse
import numpy as np 
import pandas as pd 



def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=str)
    parser.add_argument("-c", "--config", type=str, default="config.toml")

    return vars(parser.parse_args())

# Rewrite using sum() and comprehension: return sum(dot(...) for vector in orthonormal_vectors)
def project_onto_orthonormal_space(orthonormal_vectors, vector_to_project):
    projected_vector = np.zeros_like(vector_to_project)  # Initialize the projected vector

    for vector in orthonormal_vectors:
        #print(vector)
        projection = np.dot(vector, vector_to_project) * vector
        #print('PROJ',projection)
        projected_vector += projection

    return projected_vector

# Perfect
def gram_schmidt_append(orthonormal_vectors, vector_to_project):
    projected_vector = vector_to_project - project_onto_orthonormal_space(orthonormal_vectors, vector_to_project)
    norm_vector = projected_vector / np.linalg.norm(projected_vector)
    orthonormal_vectors.append(norm_vector)
    return orthonormal_vectors

# Clean up: max_index,...
def select_orthonormal_vectors(matrix, num_dimensions):
    max_index = np.argmax(np.abs(matrix[:, 0]))  # Find the index of the row with the maximum absolute value in the first column
    initial_vector = matrix[max_index, :]  # Get the initial vector using the max_index
    normalized_initial_vector = initial_vector / np.linalg.norm(initial_vector)
    selected_indexes = [max_index]  # Initialize a list to store the indexes of the selected vectors
    selected_vectors = [normalized_initial_vector]  # Initialize a list to store the selected orthonormal vectors

    while len(selected_indexes) < num_dimensions:
        min_dot = float("inf")
        best_index = None
        for i in range(matrix.shape[0]):
            if i in selected_indexes:
                continue
            candidate_vector = matrix[i, :]
            projection = project_onto_orthonormal_space(selected_vectors, candidate_vector)
            dot = np.dot(candidate_vector, projection)
            if dot < min_dot:
                min_dot = dot
                best_index = i
        selected_indexes.append(best_index)
        selected_vectors = gram_schmidt_append(selected_vectors, matrix[best_index, :])

    return selected_vectors, selected_indexes

# Rename to mention select_orthonormal_vectors, place tests in separate file
def test(): 
    I = np.eye(31)
    B = np.zeros((100, 31))
    B[:,0] = 1
    C = np.concatenate([B, I], axis = 0)
    selected_indexes, selected_vectors = select_orthonormal_vectors(C, 24)

    return selected_indexes, selected_vectors

# Save a csv with desired output
# Better naming: df is not a dataframe
# Print: Created output.csv...
# In get_cli_args, ask for where to save output
def main():

    # Get command-line arguments
    cli_args = get_cli_args()
    csv_file = cli_args["csv"]

    # Read the CSV file using the provided file name
    #df = pd.read_csv(csv_file, header=None).values
    #selected_indexes, selected_vectors = select_orthonormal_vectors(df, 24)
    selected_indexes, selected_vectors = test()
    print(selected_indexes)
    print(selected_vectors)



# Run the main function
if __name__ == "__main__":
    main()
