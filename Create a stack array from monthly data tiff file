import rasterio
import numpy as np
import os

def read_tiff_to_array(tiff_path):
    """
    Read the first band of a TIFF file into a NumPy array.
    
    Parameters:
        tiff_path (str): Path to the TIFF file.
    
    Returns:
        np.ndarray: 2D array of the TIFF file's first band.
    """
    print(f"Attempting to read file: {tiff_path}")
    with rasterio.open(tiff_path) as src:
        return src.read(1)

def get_shape_of_first_tiff(tiff_files, tiff_directory):
    """
    Determine the shape of arrays from the first available TIFF file.
    
    Parameters:
        tiff_files (list): List of TIFF filenames.
        tiff_directory (str): Directory containing TIFF files.
    
    Returns:
        tuple: Shape of the first valid TIFF array.
    """
    for file in tiff_files:
        file_path = os.path.join(tiff_directory, file)
        try:
            with rasterio.open(file_path) as src:
                return src.read(1).shape
        except rasterio.errors.RasterioIOError as e:
            print(f"Error reading file {file_path}: {e}")
            continue
    raise FileNotFoundError("No valid TIFF files found to determine array shape")

def generate_expected_filenames(start_year, end_year):
    """
    Generate a list of expected TIFF filenames for a range of years.
    
    Parameters:
        start_year (int): Starting year.
        end_year (int): Ending year.
    
    Returns:
        list: List of expected filenames.
    """
    return [
        f"clipped_final_img_{year}_{month:02d}.tif"
        for year in range(start_year, end_year + 1)
        for month in range(1, 13)
    ]

def stack_tiff_files_with_nans(expected_files, tiff_files, array_shape, tiff_directory):
    """
    Stack TIFF files into a 3D array with NaNs for missing months.
    
    Parameters:
        expected_files (list): List of expected filenames.
        tiff_files (list): List of actual filenames.
        array_shape (tuple): Shape of each 2D array.
        tiff_directory (str): Directory containing TIFF files.
    
    Returns:
        np.ndarray: 3D array with TIFF data and NaNs for missing months.
    """
    # Create an empty 3D array filled with NaNs
    stacked_array = np.full((*array_shape, len(expected_files)), np.nan)
    
    # Create a set of actual filenames for quick lookup
    actual_files_set = set(tiff_files)
    
    for index, filename in enumerate(expected_files):
        file_path = os.path.join(tiff_directory, filename)
        if filename in actual_files_set:
            try:
                array = read_tiff_to_array(file_path)
                stacked_array[..., index] = array  # Add the data to the stack
            except rasterio.errors.RasterioIOError as e:
                print(f"Error reading file {file_path}: {e}")
        else:
            print(f"Missing file: {filename}")
    
    return stacked_array

if __name__ == "__main__":
    # Parameters
    tiff_directory = '/home/prahlada/GWSA_clipped_Output'
    start_year = 2003
    end_year = 2021

    # List of actual TIFF files in the directory
    tiff_files = sorted([file for file in os.listdir(tiff_directory) if file.endswith('.tif')])

    # Generate the list of expected filenames
    expected_files = generate_expected_filenames(start_year, end_year)

    # Determine the shape of each 2D array
    array_shape = get_shape_of_first_tiff(tiff_files, tiff_directory)

    # Stack the TIFF files into a 3D array with NaNs for missing months
    tiff_3d_array_with_nans = stack_tiff_files_with_nans(expected_files, tiff_files, array_shape, tiff_directory)

    # Print the shape of the resulting 3D array
    print(f"3D array shape: {tiff_3d_array_with_nans.shape}")
