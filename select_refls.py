import argparse
import numpy as np 
import pandas as pd 


def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("reflectances", type=str, help="Path to a CSV file with reflectances data base")
    parser.add_argument("light", type=str, help="Path to a CSV file with Illuminant")
    parser.add_argument("num_rows", type=int, help="Number of reflectance vectors to be selected")
    parser.add_argument("outfile", type=str, help="Path to an output CSV file")
    parser.add_argument("-m", "--method", choices=["mincos"], default="mincos",
                    help="Select one or more methods") #Extend when more methods are developed 
    parser.add_argument("--min_norm_2", type=float, default=0.0)
    parser.add_argument("--min_norm_inf", type=float, default=0.0)
    cli = vars(parser.parse_args())

    return cli 

def load_data(cli_args):
    refl_file = cli_args["reflectances"]
    light_file = cli_args["light"]
    num_rows = cli_args["num_rows"]
    outfile = cli_args["outfile"]
    
    # Read the CSV file using the provided file name
    R = pd.read_csv(refl_file#, header=None
                    ).values
    L = pd.read_csv(light_file #, header=None
                    ).values
    
    data = dict(
        cli_args = cli_args, 
        R        = R, 
        L        = L, 
        num_rows = num_rows, 
        outfile = outfile
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

def greedy_cosmin(matrix, num_dimensions):
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

    return selected_indexes

#Selecting most orthogonal reflectances based on the standard light 
def select_orthonormal_vectors_given_light(R, L, num_dimensions):
    num_rows, num_cols = R.shape
    R_L = R*L.reshape((1,num_cols))
    selected_indexes = greedy_cosmin(R_L, num_dimensions)
    
    return selected_indexes

def process_data(data):
    filtered_idxs = [
        i for i,row in enumerate(data["R"])
        if np.linalg.norm(row) >= data["cli_args"]["min_norm_2"]
        and np.linalg.norm(row, ord=np.inf) >= data["cli_args"]["min_norm_inf"]
    ]
    R = data["R"][filtered_idxs]
    idx_map = {i:idx for i,idx in enumerate(filtered_idxs)}
    #print(idx_map)

    return dict(
        cli_args = data["cli_args"],
        R_unfiltered = data["R"],
        R        = R,
        L        = data["L"],
        num_rows = data["num_rows"],
        outfile  = data["outfile"],
        idx_map  = idx_map,
    )

def main():

    # Get command-line arguments
    cli_args = get_cli_args()
    data = process_data(load_data(cli_args))

    if cli_args["method"] == "mincos": 
        selected_indexes = select_orthonormal_vectors_given_light(data["R"], data["L"], data["num_rows"])
        selected_indexes = [data["idx_map"][idx] for idx in selected_indexes]

    create_csv_file(data["outfile"], data["R_unfiltered"], selected_indexes)
    print("CSV file has been successfully created! ")


# Run the main function
if __name__ == "__main__":
    main()
