import argparse
import numpy as np 
import pandas as pd 
from pathlib import Path
import matplotlib.pyplot as plt


def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help = "Path to a CSV file with data to be plotted")
    parser.add_argument("outfile", type=str, help="Path to a PDF file where the plot is saved")
    parser.add_argument("-i", "--index", action="store_true", help="Ignore the first column of the provided reflectances data (that might include indices)" )
    parser.add_argument("-p", "--plot", action="store_true", help="Flag to show the plot")
    return vars(parser.parse_args())

def plot_data(x, y, cli, filename):
    for row in y:
        plt.plot(x, row)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"{filename}-data-plot")
    plt.savefig(cli["outfile"])
    plt.show() #MAKE THIS OPTIONAL 

def main():
    cli = get_cli_args()
    data = pd.read_csv(cli["infile"], header=None).values
    
    if cli["index"]: # Check if the index flag is present
        data = pd.read_csv(
            cli["infile"], dtype="float64", usecols=range(1,data.shape[1]), header=None
        ).values

    x = data[0,:]
    y = data[1:,:]

    filename = str(Path(cli["infile"]).stem)

    if cli["plot"]: 
        plot_data(x, y, cli, filename)

if __name__ == '__main__': main()