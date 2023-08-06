import argparse
import numpy as np 
import pandas as pd 

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=str)
    parser.add_argument("outfile", type=str)
    parser.add_argument("min_wavelength", type=int)
    parser.add_argument("max_wavelength", type=int)
    parser.add_argument("step", type=int)
    parser.add_argument("-t", "--transpose", action="store_true", help="Transpose the data before interpolation")
    cli = vars(parser.parse_args())

    return cli 

def add_colunm_wavelengths(matrix, min, max, step): 
    numbers = list(range(min, max, step))
    matrix.columns = numbers
    
def main(): 
    cli_args = get_cli_args()
    csv_file = cli_args["csv"]
    outfile = cli_args["outfile"]
    min = cli_args["min_wavelength"]
    max = cli_args["max_wavelength"]
    step = cli_args["step"]
    matrix = pd.read_csv(csv_file, header=None)

    if cli_args["transpose"]: # Check if the '--transpose' flag is present
        matrix = matrix.T

    add_colunm_wavelengths(matrix, min, max, step)
    matrix.to_csv(outfile, index=False)

    print("The CSV file has been annotated with column names!")

# Run the main function
if __name__ == "__main__":
    main()