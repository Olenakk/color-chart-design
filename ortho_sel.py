import argparse
import numpy as np 
import pandas as pd 


def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("refl", type=str, help="Path to a CSV file with reflectances")
    parser.add_argument("lt", type=str, help="Path to a CSV file with Illuminant")
    parser.add_argument("-o", "--output", type=str, default="selected_vectors.csv", help="Output file path")
    cli = vars(parser.parse_args())

    return cli 

def load_data(cli_args):
    refl_file = cli_args["refl"]
    light_file = cli_args["lt"]
    
    # Read the CSV file using the provided file name
    R = pd.read_csv(refl_file#, header=None
                    ).values
    L = pd.read_csv(light_file #, header=None
                    ).values
    
    data = dict(
        cli_args = cli_args, 
        R        = R, 
        L        = L, 
    )

    return data


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
            dot = np.dot(candidate_vector, projection)/(np.linalg.norm(candidate_vector)*np.linalg.norm(projection))
            if dot < min_dot:
                min_dot = dot
                best_index = i
        selected_indexes.append(best_index)
        selected_vectors = gram_schmidt_append(selected_vectors, matrix[best_index, :])

    return selected_indexes, selected_vectors

#Selecting most orthogonal reflectances based on the standard light 
def select_orthonormal_vectors_given_light(R, L, num_dimensions):
    num_rows, num_cols = R.shape
    R_L = R*L.reshape((1,num_cols))
    selected_indexes, selected_vectors = select_orthonormal_vectors(R_L, num_dimensions)
    
    return selected_indexes, selected_vectors

def main():

    # Get command-line arguments
    cli_args = get_cli_args()
    data = load_data(cli_args)
    output_file = cli_args["output"]

    #selected_indexes, selected_vectors = select_orthonormal_vectors(matrix, 24)
    selected_indexes, selected_vectors = select_orthonormal_vectors_given_light(data["R"], data["L"], 24)
    create_csv_file(output_file, data["R"], selected_indexes)
    print("CSV file has been successfully created! ")


# Run the main function
if __name__ == "__main__":
    main()
