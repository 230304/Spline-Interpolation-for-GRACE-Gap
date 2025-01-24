import rasterio
import numpy as np
import os

# Example TIFF path (to guide new users)
DUMMY_DIRECTORY = "data/example_tiffs/"  
DUMMY_MISSING_FILES = [
    "clipped_final_img_2017_08.tif", 
    "clipped_final_img_2018_01.tif"
]

def read_tiff_to_array(tiff_path):
    """
    Reads a single TIFF file and returns its first band as a NumPy array.

    Parameters:
        tiff_path (str): Path to the TIFF file.

    Returns:
        np.ndarray: 2D NumPy array from the TIFF file.
    """
    with rasterio.open(tiff_path) as src:
        return src.read(1)  # Read the first band

def get_shape_of_first_tiff(tiff_files, tiff_directory):
    """
    Determines the shape of the first valid TIFF file in the directory.

    Parameters:
        tiff_files (list): List of available TIFF filenames.
        tiff_directory (str): Directory containing TIFF files.

    Returns:
        tuple: Shape of the first valid TIFF file as (rows, cols).
    
    Raises:
        FileNotFoundError: If no valid TIFF files are found.
    """
    for file in tiff_files:
        file_path = os.path.join(tiff_directory, file)
        try:
            with rasterio.open(file_path) as src:
                return src.read(1).shape  # Return shape of the first band
        except rasterio.errors.RasterioIOError as e:
            print(f"Error reading file {file_path}: {e}")
    raise FileNotFoundError("No valid TIFF files found to determine array shape.")

def create_monthly_3d_arrays(tiff_files, missing_files, start_year, end_year, tiff_directory):
    """
    Creates 3D NumPy arrays for each month across a range of years, with NaNs for missing data.

    Parameters:
        tiff_files (list): List of available TIFF filenames.
        missing_files (list): List of missing TIFF filenames.
        start_year (int): Start year for the data (e.g., 2003).
        end_year (int): End year for the data (e.g., 2021).
        tiff_directory (str): Directory containing the TIFF files.

    Returns:
        dict: Dictionary of 3D NumPy arrays (one per month) with shape (rows, cols, years).
    """
    # Get the shape of a single TIFF array
    array_shape = get_shape_of_first_tiff(tiff_files, tiff_directory)
    
    # Calculate the total number of years
    total_years = end_year - start_year + 1
    
    # Initialize 3D arrays for each month (filled with NaNs)
    monthly_arrays = {month: np.full((*array_shape, total_years), np.nan) for month in range(1, 13)}
    
    # Create a quick-lookup set for missing files
    missing_files_set = set(missing_files)
    
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            filename = f"clipped_final_img_{year}_{month:02d}.tif"
            file_path = os.path.join(tiff_directory, filename)
            year_index = year - start_year  # Year index in the 3D array
            
            # Handle missing files
            if filename in missing_files_set:
                print(f"Skipping missing file: {filename}")
                continue
            
            if filename in tiff_files and os.path.exists(file_path):
                try:
                    array = read_tiff_to_array(file_path)
                    monthly_arrays[month][..., year_index] = array  # Assign to correct position
                except rasterio.errors.RasterioIOError as e:
                    print(f"Error reading file {file_path}: {e}")
            else:
                print(f"File not found: {file_path}")
    
    return monthly_arrays

if __name__ == "__main__":
    # Example usage with dummy inputs
    tiff_directory = DUMMY_DIRECTORY  # Replace with your actual directory
    tiff_files = sorted([file for file in os.listdir(tiff_directory) if file.endswith(".tif")])

    # Specify start and end years
    start_year = 2003
    end_year = 2021

    # Create 3D arrays for each month
    monthly_3d_arrays = create_monthly_3d_arrays(
        tiff_files=tiff_files,
        missing_files=DUMMY_MISSING_FILES,
        start_year=start_year,
        end_year=end_year,
        tiff_directory=tiff_directory,
    )

    # Print shapes of generated 3D arrays
    for month in range(1, 13):
        print(f"Shape of 3D array for month {month:02d}: {monthly_3d_arrays[month].shape}")
