import argparse
import numpy as np 
import pandas as pd 
import test
import process_spectra_csv

from test import *
from process_spectra_csv import *


def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=str)
    parser.add_argument("-o", "--output", type=str, default="selected_vectors.csv", help="Output file path")
    cli = vars(parser.parse_args())

    return cli 

def create_csv_file(file_name, matrix, selected_indexes):
   original_selected_vectors = np.array(matrix[selected_indexes])
   concatinated_array = np.concatenate([np.array(selected_indexes).reshape(-1, 1),original_selected_vectors], axis=1)
   df = pd.DataFrame(concatinated_array)
   numbers = list(range(400, 701, 10))
   numbers.insert(0, "Index")
   df.to_csv(file_name, index=False, header = numbers)
   

def project_onto_orthonormal_space(orthonormal_vectors, vector_to_project):
    return sum(np.dot(vector, vector_to_project) * vector for vector in orthonormal_vectors)

def gram_schmidt_append(orthonormal_vectors, vector_to_project):
    projected_vector = vector_to_project - project_onto_orthonormal_space(orthonormal_vectors, vector_to_project)
    norm_vector = projected_vector / np.linalg.norm(projected_vector)
    orthonormal_vectors.append(norm_vector)
    return orthonormal_vectors

def select_orthonormal_vectors(matrix, num_dimensions):
    max_index = np.argmax(np.linalg.norm(matrix, axis=1))
    initial_vector = matrix[max_index, :]  # Get the initial vector using the max_index
    normalized_initial_vector = initial_vector / np.linalg.norm(initial_vector)
    selected_indexes = [max_index]  # Initialize a list to store the indexes of the selected vectors
    selected_vectors = [normalized_initial_vector]  # Initialize a list to store the selected orthonormal vectors

    while len(selected_indexes) < num_dimensions:
        print("Progress: " + str(len(selected_vectors)) + "/" + str(num_dimensions))
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

    return selected_indexes, selected_vectors


def main():

    # Get command-line arguments
    cli_args = get_cli_args()
    csv_file = cli_args["csv"]
    output_file = cli_args["output"]

    # Read the CSV file using the provided file name
    #matrix = pd.read_csv(csv_file, header=0).values

    

    #orthogonal_matrix = generate_orthogonal_matrix(31, 31)
    #matrix = construct_matrix_with_zeroth_row(orthogonal_matrix)

    Q_matrix = insert_zeroth_row_after_each_row(generate_QR_orthogonal_matrix(31))


    selected_indexes, selected_vectors = select_orthonormal_vectors(Q_matrix, 24)

    #selected_indexes, selected_vectors = test_selection_of_orthonormal_vectors()
    #print(selected_vectors)
    #print(selected_indexes)

    create_csv_file(output_file, Q_matrix, selected_indexes)
    print("CSV file has been successfully created! ")


# Run the main function
if __name__ == "__main__":
    main()