import argparse
import numpy as np 
import pandas as pd 

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=str)
    cli = vars(parser.parse_args())

    return cli 

def add_colunm_wavelengths(matrix): 
    numbers = list(range(400, 701, 10))
    matrix.columns = numbers
    
def main(): 
    cli_args = get_cli_args()
    csv_file = cli_args["csv"]
    matrix = pd.read_csv(csv_file, header=None)
    add_colunm_wavelengths(matrix)
    matrix.to_csv(csv_file, index=False)

    print("The CSV file has been annotated with column names!")

# Run the main function
if __name__ == "__main__":
    main()