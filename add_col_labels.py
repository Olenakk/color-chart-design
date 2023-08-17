import argparse
import numpy as np 
import pandas as pd 

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str)
    parser.add_argument("outfile", type=str)
    parser.add_argument("-b", "--bounds", nargs=3, type=int, default=[400, 700, 10], help="Start, end, and step for wavelength bounds")
    parser.add_argument("-t", "--transpose", action="store_true", help="Transpose the data before interpolation")
    cli = vars(parser.parse_args())

    return cli 

def add_colunm_wavelengths(matrix, bounds): 
    min_val, max_val, step = bounds
    numbers = list(range(min_val, max_val+1, step))
    matrix.columns = numbers
    
def main(): 
    cli_args = get_cli_args()
    csv_file = cli_args["infile"]
    outfile = cli_args["outfile"]
    bounds = cli_args["bounds"]
    matrix = pd.read_csv(csv_file, header=None
                         )

    if cli_args["transpose"]: # Check if the '--transpose' flag is present
        matrix = matrix.T

    add_colunm_wavelengths(matrix, bounds)
    matrix.to_csv(outfile, index=False)

    print("The CSV file has been annotated with column names!")

# Run the main function
if __name__ == "__main__":
    main()