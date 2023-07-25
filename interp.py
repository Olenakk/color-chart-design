import argparse
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

def get_cli_args():
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description=
        """
        Linearly interpolates vectors v1, ..., vn on points x1, ..., xm.
        The rows of the [data] file contain the values of the vectors vi, except for the first row, which contains the corresponding evaluation points.
        The [pts] file contains new evaluation points x1, ..., xm.
        """
        )

    # Add command-line arguments
    parser.add_argument("data", type=str, help="Path to the CSV file containing data to be interpolated.")
    parser.add_argument("pts", type=str, help="Path to the CSV file containing points to be interpolated (wavelength)") 
    parser.add_argument("output", type=str, help="Output file path to save the interpolated data as a CSV file")
    parser.add_argument("-p", "--plot", type=str, help="Flag to plot the interpolated data")
    parser.add_argument("-t", "--transpose", action="store_true", help="Transpose the data before interpolation")
    
    # Parse the command-line arguments
    cli = vars(parser.parse_args())

    return cli 

def plot_interp_data(xp, fp, data_interp, pts, cli_args): 
    # Plot original and interpolated data for each row separately
    for row_original, row_interp in zip(fp, data_interp): 
        plt.plot(xp, row_original, label='Original Data', marker='.')
        plt.scatter(pts, row_interp, label='Interpolated Data', color='black')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Interpolated Data')
    plt.grid()

    # Custom legend entries and labels
    legend_entries = [
        (plt.plot([], [], color='black', linestyle='-', linewidth=2)[0], 'Original Data'),
        (plt.scatter([], [], marker='o', color='black'), 'Interpolated Data')
    ]
    
    # Create a custom legend using the legend_entries list
    plt.legend(handles=[entry[0] for entry in legend_entries], labels=[entry[1] for entry in legend_entries])

    # Save the plot to the PDF file
    plt.savefig(cli_args["plot"], bbox_inches="tight")   
    #plt.show()    

def main(): 
    # Get command-line arguments
    cli_args = get_cli_args()

    # Read the data and points from CSV files
    data = pd.read_csv(cli_args["data"], dtype='float64', header=None).values
    pts = pd.read_csv(cli_args["pts"], header=None, dtype='float64').values.flatten()
    
    if cli_args["transpose"]: # Check if the '--transpose' flag is present
        data = data.T
    
    # Separate 'xp' and 'fp' from the 'data'. See numpy.interp(): https://numpy.org/doc/stable/reference/generated/numpy.interp.html
    xp = data[0,:]
    fp = data[1:,:]
    # Perform interpolation for each row of 'fp' using 'xp' and 'pts'
    data_interp = np.array([np.interp(pts, xp, row) for row in fp])

    # Check if the plot flag is provided
    if cli_args["plot"] is not None: 
        plot_interp_data(xp, fp, data_interp, pts, cli_args)

    # Save interpolated data to the output file
    np.savetxt(cli_args["output"], data_interp, delimiter=",", fmt='%.4f')

if __name__ == "__main__":  main()
