import pandas as pd 
import argparse

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="Path to the input file")
    parser.add_argument("outfile", type=str, help="Path to an output file with a transposed matrix")
    return vars(parser.parse_args())

def main():
    cli = get_cli_args()
    infile = cli["infile"]
    outfile = cli["outfile"]
    pd.DataFrame(pd.read_csv(infile, dtype='float64', header=None).values.T).to_csv(outfile, index=False, header=False)
    
if __name__ == '__main__': main()