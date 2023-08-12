import os
from PIL import Image
import matplotlib.pyplot as plt
import argparse

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infolder", type=str, help="Path to the folder with input images") 

    cli = vars(parser.parse_args())

    return cli 

def plot_images(infolder):
    # Get a list of all files in the specified folder
    file_list = os.listdir(infolder)
    
    # Filter for image files (you might need to adjust the extensions)
    image_files = [f for f in file_list if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # Calculate number of rows and columns for subplots
    num_images = len(image_files)
    num_rows = int(num_images ** 0.5)
    num_cols = (num_images + num_rows - 1) // num_rows
    
    # Create subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
    fig.subplots_adjust(hspace=0.5)
    
    # Loop through image files and plot them
    for i, img_file in enumerate(image_files):
        row = i // num_cols
        col = i % num_cols
        
        img_path = os.path.join(infolder, img_file)
        img = Image.open(img_path)
        
        ax = axes[row, col]
        ax.imshow(img)
        ax.set_title(img_file)
        ax.axis('off')  # Turn off axis labels
    
    plt.show()

def main(): 
    cli = get_cli_args()
    infolder = cli["infolder"]
    plot_images(infolder) 

if __name__ == "__main__":
    main()    