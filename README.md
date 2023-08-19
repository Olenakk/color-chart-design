
# Color Chart Detection Tool
Welcome to the project repository focused on crafting an exceptional color checker (color chart) with color patches exhibiting linearly independent reflectance properties. Our mission revolves around providing a comprehensive toolkit, empowering users to preprocess their input datasets seamlessly, visualize both initial and intermediate data representations, select the most orthogonal reflectances embedded within the dataset, and conduct thorough evaluations of the curated dataset.

## <font color=FD8D14> **Key Features:** </font>

* **Optimal Color Checker Design:** Our project centers on the creation of a color chart that boasts an optimal selection of color patches, each characterized by linearly independent reflectance attributes.

* **Robust Toolkit:** We've developed a toolkit that streamlines the process of preprocessing input datasets.

* **Data Visualization:** Gain valuable insights by visualizing initial and intermediate data representations. Our visualization tools facilitate a deeper understanding of the data transformation process.
* **Reflectance Selection:** The heart of our project lies in the ability to identify and select the most orthogonal reflectances from user's dataset. This crucial step ensures the quality and independence of user's chosen reflectance values.

* **Comprehensive Evaluation:** We offer tools to comprehensively evaluate the selected reflectance dataset. Multiple assessment metrix ensure the reliability and effectiveness of the chosen reflectances.
****
## <font color=FD8D14> **Prerequisites**</font>
* Python 3.x
* Required Python packages: argparse, numpy, pandas, pathlib, cv2, toml, and matplotlib
****
# 1. Select Data 
<font color=FD8D14>_The data utilized should be in CSV format_</font>
## Reflectances 
* User's reflectances database should be an _m by n_ CSV file with a header that indicates a wavelength spectrum. See the format of the table below: 

**R, Reflectances for a given wavelength spectrum**

400 |410 | 420 |430|...|690|700|
----|----|-----|---|---|---|---|
 R00 | R01 | R02 |R03| ... | R0(n-1)|R0(n)
 R10 | R11 | R12 |R13| ... | R1(n-1)|R1(n)
 R20 | R21 | R22 |R23| ... | R2(n-1)|R2(n)
 ... | ... | ... |...| ... | ...|...
R(m)0 | R(m)1 | R(m)2 |R(m)3| ... | R(m)(n-1)|R(m)(n)

 * Choose data for user's reflectance database here: https://docs.google.com/spreadsheets/d/10-a_kN8EUBj3IciJ1KHhYuio1Qp91VryB2-H4EuhYZs/edit?usp=sharing

* The user can find sample reflectances files in <font color=FD8D14>data\reflectances</font>
## Illuminants (light)
* User's light data should be a _2 by n_ CSV file with a header that indicates a wavelength spectrum:

**L, Light for a given wavelength spectrum**

400 |410 | 420 |430|...|690|700|
----|----|-----|---|---|---|---|
 L0 | L1 | L2 | L3 |...|L(n-1)| L(n)

 * The user can find sample light files in <font color=FD8D14>data\illuminants</font>
## Sensitivity 
* User's sensitivity data should be a _3 by n_ CSV file with a header that indicates a wavelength spectrum:

**S, Sensitivity for a given wavelength spectrum**

400 |410 | 420 |430|...|690|700|
----|----|-----|---|---|---|---|
 S00 | S01 | S02 | S03| ... | S0(n-1)|S0(n)
 S10 | S11 | S12 | S13| ... | S1(n-1)|S1(n)
 S20 | S21 | S22 | S23| ... | S2(n-1)|S2(n)

* The user can find sample sensitivity data in <font color=FD8D14>data\sensitivity</font>

## Wavelengths 

* User's wavelengths data should be a _1 by n_ CSV file: 

**λ, Wavelength spectrum**

400 |410 | 420 |430|...|690|700|
----|----|-----|---|---|---|---|
* The user can find sample wavelengths data in <font color=FD8D14>data\wavelengths</font>
****
# 2. Preprocess Data 
<font color=FD8D14>_Ensure that all data used in the program includes a header with wavelength information and is defined on the same wavelength spectrum with uniform intervals_</font>

The user can preprocess data in the following ways:
* Interpolate 
* Transpose
* Format (add column labels)

## <font color=FD8D14> **Linear Interpolation Tool (interp.py)**</font>
## Usage
```
python interp.py <infile> <waves> <outfile> [-p <plot_filename>] [-t]
```
* `<infile>`: Path to the CSV file containing data to be interpolated.
* `<waves>`: Path to the CSV file containing points to be interpolated (wavelengths).
* `<outfile>`: Output file path to save the interpolated data as a CSV file.
* `-p <plot_filename>` or `--plot <plot_filename>`: (Optional) Flag to plot the interpolated data and save the plot as a PDF file named <plot_filename>.
* `-t or --transpose`: (Optional) Transpose the data before interpolation.

## Input Files
**Input Data File** (`<infile>`)
The input data file should be a CSV file containing the values of vectors to be interpolated. Each row represents a vector, and the first row contains the corresponding evaluation points.

**Evaluation Points File** (`<waves>`)
The evaluation points file should be a CSV file containing new evaluation points (wavelengths) for interpolation. It should have a single row with the evaluation point values.

**Output**
The interpolated data will be saved as a CSV file specified by `<outfile>`. Each row in the output file corresponds to an interpolated vector.

## Example Usage
1. Interpolate data using default settings:
    ```
    python interp.py input_data.csv evaluation_points.csv output_interpolated.csv
    ```
2. Interpolate data, transpose the input data, and save the plot:
    ```
    python interp.py input_data.csv evaluation_points.csv output_interpolated.csv -p interpolated_plot.pdf -t
    ```

## Additional Information
For more information about linear interpolation and the mathematical details behind this tool, refer to the documentation for the numpy.interp() function: numpy.interp() [documentation](https://numpy.org/doc/stable/reference/generated/numpy.interp.html)

For more information about argparse, numpy, pandas, and matplotlib, please consult their respective documentation.

## <font color=FD8D14> **Matrix Transposer (transpose.py)** </font>

This Python script provides a simple command-line tool for transposing a matrix stored in a CSV file. The script uses the `pandas` library to read the input matrix from a CSV file, transpose it, and save the transposed matrix as a new CSV file.

## Usage
```
python transpose.py <infile> <outfile>
```
* `<infile>`: Path to the input CSV file containing the matrix to be transposed.
* `<outfile>`: Path to the output CSV file to save the transposed matrix.

## Input
**Input CSV File** (`<infile>`)

The input CSV file should contain the matrix that the user wants to transpose. Each row in the CSV file represents a row of the matrix, and the elements in each row are separated by commas.

## Output
The transposed matrix will be saved as a CSV file specified by `<outfile>`. The rows of the original matrix become the columns in the transposed matrix, and vice versa.

## Example Usage
1. Transpose a matrix stored in input_matrix.csv and save the transposed matrix as transposed_matrix.csv:
    ```
    python transpose.py input_matrix.csv transposed_matrix.csv
    ```
## <font color=FD8D14>**Column Labels Annotator (add_col_labels.py)** </font>
This Python script provides a convenient command-line tool for annotating a CSV file by adding column names representing wavelength values. The script allows customization of wavelength bounds and step size. Additionally, it supports transposing the data if needed before annotation.

## Usage
```
python add_col_labels.py <infile> <outfile> [-b <start> <end> <step>] [-t]
```
* `<infile>`: Path to the input CSV file containing data to be annotated.
* `<outfile>`: Path to the output CSV file to save the annotated data.
* `-b <start> <end> <step>` or `--bounds <start> <end> <step>`: (Optional) Set custom wavelength bounds for column annotation. The default is a wavelength range of 400 to 700 with a step size of 10.
* `-t` or `--transpose`: (Optional) Transpose the data before annotation.

## Input
**Input CSV File (`<infile>`)**

The input CSV file should contain the data that the user wants to annotate. 

## Output
The annotated data will be saved as a CSV file specified by `<outfile>`. The columns in the annotated CSV file will be labeled with wavelength values based on the specified bounds and step size.

## Example Usage
1. Annotate data using default wavelength bounds and transpose the data:
    ```
    python add_col_labels.py input_data.csv annotated_data.csv 
    ```
## Additional Information
If needed, the input data can be transposed before annotation using the -t flag.
****
# 3. Visualize data 
The user can visualize data in the following ways:
* Plot
* Calcualte RGB values 
* Visualize color chart

## <font color=FD8D14>**Data Plotter (plot_data.py)** </font>
The "plot_data.py" script is a Python tool designed to create visualizations of numerical data from CSV files. The script utilizes the `matplotlib` library to generate plots and allows for customization of plot styles and configurations.

## Usage
```
python plot_data.py <infile> <outfile> [-i] [-p]
```
* `<infile>`: Path to the input CSV file containing data for plotting.
* `<outfile>`: Path to the output PDF file where the plot will be saved.
* `-i` or `--index`: (Optional) Ignore the first column of the provided reflectance data, which might include indices.
* `-p` or `--plot`: (Optional) Flag to display the generated plot.

## Input
**Input CSV File (`<infile>`)**

The input CSV file should contain the numerical data that the user wants to plot. Each row in the CSV file represents a data point, and the columns contain corresponding data values.

## Output
The script generates a plot based on the data in the input CSV file and saves it as a PDF file specified by `<outfile>`. If the `-p` flag is used, the plot will also be displayed on the screen.

## Example Usage
1. Plot data using default settings and display the plot:
    ```
    python plot_data.py input_data.csv output_plot.pdf -p
    ```
2. Plot data while ignoring the first column and save the plot as a PDF: 
    ```
    python plot_data.py input_data.csv output_plot.pdf -i
    ```

## <font color=FD8D14>**RGB Calculator (calc_rgb.py)** </font>
The "calc_rgb.py" script is a Python tool designed to calculate RGB values based on given reflectance data, light sources, and camera sensitivities or observer functions. The script takes input in CSV format and produces an output CSV file containing RGB values. The calculated RGB values can be used for various visualization and analysis purposes.

## Usage
```
python calc_rgb.py <reflectances> <light> <sensitivity> <outfile> [-i]
```
* `<reflectances>`: Path to the CSV file containing reflectance data.
* `<light>`: Path to the CSV file containing light source data.
* `<sensitivity>`: Path to the CSV file containing camera sensitivity or observer data.
* `<outfile>`: Path to the output CSV file where the RGB values will be saved.
* `-i` or `--index`: (Optional) Ignore the first column of the provided reflectance data, which might include indices.

## Input
**Reflectance Data (`<reflectances>`)**

The reflectance data CSV file should contain the spectral reflectance values. Each row represents a material or sample, and the columns represent the reflectance values at different wavelengths.

**Light Source Data (`<light>`)**

The light source data CSV file contains the spectral distribution of the light sources. Each row represents a light source, and the columns represent the light intensity values at different wavelengths.

**Sensitivity Data (`<sensitivity>`)**

The sensitivity data CSV file contains camera sensitivity or observer data. Each row represents a color channel or observer function, and the columns represent the sensitivity values at different wavelengths.

## Output
The script calculates RGB values based on the provided input data and saves the RGB values as a CSV file specified by `<outfile>`.

## Example Usage

1. Calculate RGB values using default settings:
    ```
    python calc_rgb.py reflectance_data.csv light_data.csv sensitivity_data.csv rgb_values.csv
    ```
2. Calculate RGB values while ignoring the first column of reflectance data:
    ```
    python calc_rgb.py reflectance_data.csv light_data.csv sensitivity_data.csv rgb_values.csv -i
    ```
## <font color=FD8D14>**Color Chart Visualizer (vis_chart.py)** </font>
The "vis_chart.py" script is a Python tool designed to visualize RGB color values stored in a CSV file as a color chart. The script utilizes the `cv2` library to generate the color chart and provides options for adjusting the appearance of the chart. The script includes normalization and enhancement of the image to make it more visually appealing.

## Usage 
```
python vis_chart.py <infile> <outfile> [-s <rows> <columns>] [-v <visual_exponent>] [-r <resize_factor>]
```
* `<infile>`: Path to the CSV file containing RGB values.
* `<outfile>`: Path to the output PNG file where the color chart will be saved.
* `-s <rows> <columns>`: (Optional) Specify the shape of the color chart (number of rows and columns). Default is 1 row and automatic column calculation.
* `-v <visual_exponent>`: (Optional) Adjust the coefficient for enhancing the image. Default is 2.2.
* `-r <resize_factor>`: (Optional) Resize the image by the specified factor. Default is no resizing (1).

## Input
**RGB Values (`<infile>`)**

The input CSV file should contain RGB values. Each row represents an RGB color, and the columns represent the red, green, and blue channels. 

## Output
The script generates a color chart based on the provided RGB values and saves it as a PNG file specified by `<outfile>`.

## Example Usage
1. Visualize RGB values using default settings:
    ```
    python vis_chart.py rgb_values.csv color_chart.png
    ```
2. Visualize RGB values with a 4x6 color chart and adjust visual exponent:
    ```
    python vis_chart.py rgb_values.csv color_chart.png -s 4 6 -v 2.5
    ```
3. Visualize RGB values and resize the image by a factor of 10:
    ```
    python vis_chart.py rgb_values.csv color_chart.png -r 10
    ```
****
# 4. Select Reflectances from the Data Base
## <font color=FD8D14>**Reflectance Selection (select_refls.py)** </font>
* `<reflectances>`: Path to the CSV file containing reflectance data.
* `<light>`: Path to the CSV file containing light source data.
* `<num_rows>`: Number of reflectance vectors to be selected.
* `<outfile>`: Path to the output CSV file where the selected reflectance vectors will be saved.
* `-m <method>`: (Optional) Select the method for selecting vectors. Default is "mincos".
* `--min_norm_2 <min_norm_2>`: (Optional) Set the minimum L2-norm for vector selection.
* `--min_norm_inf <min_norm_inf>`: (Optional) Set the minimum L-infinity norm for vector selection.
## Input
**Reflectance Data (`<reflectances>`)**

The input CSV file should contain reflectance data. Each row represents a reflectance vector, and the columns represent the reflectance values at different wavelengths.

**Light Data (`<light>`)**

The light data CSV file contains the spectral distribution of light sources. Each row represents a light source, and the columns represent the light intensity values at different wavelengths.

## Output
The script generates an output CSV file containing the selected reflectance vectors based on the specified method and criteria. The index indicates the position of the selected reflectance vector within the input file. 

**Fortmat of the output CSV file:**

Index |410 | 420 |430|440|...|690|700|
------|----|-----|---|---|---|---|---
 91 | R00 | R01 | R02 |R03| ... | R0(n-1)|R0(n)
 4 | R10 | R11 | R12 |R13| ... | R1(n-1)|R1(n)
 119 | R20 | R21 | R22 |R23| ... | R2(n-1)|R2(n)
 ... | ... | ... | ... |...| ... | ...|...
76 |R(num_rows)0 | R(num_rows)1 | R(num_rows)2 |R(num_rows)3| ... | R(num_rows)(n-1)|R(num_rows)(n)

## Example Usage
1. Select reflectance vectors using the default "mincos" method:
    ```
    python select_refls.py reflectance_data.csv light_data.csv 10 selected_refls.csv
    ```
2. Select reflectance vectors using the "mincos" method and custom norms:
    ```
    python select_refls.py reflectance_data.csv light_data.csv 31 selected_refls.csv --min_norm_2 0.2 --min_norm_inf 0.1
    ```

The script provides multiple criteria for vector selection and can be extended with additional methods in the future.
****
# 5. Evaluate Selected Reflectances 
## <font color=FD8D14>**Reflectance Analysis (evaluate.py)** </font>

The `evaluate.py` script is a tool designed to calculate various metrics and perform analyses on reflectance data obtained from a CSV file. It offers the flexibility to compute orthogonality defects, sequential orthogonality defects, and singular values for the provided reflectance data. Additionally, it allows users to visualize singular values by plotting them.

## Features
* Compute orthogonality defect of a matrix based on its columns.
* Calculate sequential orthogonality defects for the given reflectance data.
* Compute singular values using Singular Value Decomposition (SVD).
* Option to plot singular values for each row of the reflectance data.
* Ability to round the computed values to a specified number of digits.
* Save the computed metrics and results in a TOML file.

## Usage
Run the script with the required command-line arguments.
```
python evaluate.py reflectance_data.csv light_data.csv -o results.toml -i -s 4 -p 
```
* `<reflectances>`: Path to the CSV file containing reflectance data.
* `<light>`: Path to the CSV file containing light data.
* `-o`, `--outfile`: (Optional) Path to the TOML file where the computed metrics and results will be saved.
* `-i`, `--index`: (Optional) Ignore the first column of the provided reflectances data (if it includes indices).
* `-s`, `--sig_figs`: (Optional) Number of decimal places to round the computed values.
* `-p`, `--plot`: (Optional) Plot singular values for each row.

1. Review the printed results for orthogonality defects, sequential orthogonality defects, and singular values.

2. If specified, a plot of singular values will be displayed.

3. If specified, the computed metrics and results will be saved to the TOML file.
*** 
# 6. Sensitivity Reconstruction 
The Reflectance Noise Analysis script is designed to analyze the effects of noise on the accuracy of computed reflectance values. It takes into account ground truth data, reflectance values, and light data to simulate noise and calculate the resulting errors in computed reflectance values.

Ground truth data can be found here: <font color=FD8D14>data\sensitivity\ground_truth_db </font>

## Features
* Analyze the impact of noise on computed reflectance values.
* Calculate the error in computed reflectance values under varying noise intensities.
* Visualize the relationship between noise intensity and computed errors.

## Usage
Run the script with the required command-line arguments. The available options are as follows:
```
    python noise.py ground_truth.csv reflectance_data.csv light_data.csv -i
```
* `<ground_truth>`: Path to the CSV file containing the ground truth data.
* `<reflectances>`: Path to the CSV file containing the reflectance values.
* `<light>`: Path to the CSV file containing light data.
* `-i`, `--index`: Ignore the first column of the provided reflectances data (if it includes indices).

1. The script will simulate noise for different intensities and calculate the errors in computed reflectance values.

2. The resulting errors will be plotted, showing the relationship between noise intensity and computed errors.