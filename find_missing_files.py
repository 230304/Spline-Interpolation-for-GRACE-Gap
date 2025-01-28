import os

def generate_expected_filenames(start_year, end_year):
    """
    Generate a list of expected filenames for a range of years.
    
    Parameters:
        start_year (int): The starting year.
        end_year (int): The ending year.
    
    Returns:
        list: A list of expected TIFF filenames.
    """
    expected_files = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            filename = f"clipped_final_img_{year}_{month:02d}.tif"
            expected_files.append(filename)
    return expected_files

def get_actual_filenames(directory):
    """
    Retrieve a list of TIFF files from the specified directory.
    
    Parameters:
        directory (str): The path to the directory containing TIFF files.
    
    Returns:
        list: A list of actual TIFF filenames in the directory.
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    return [file for file in os.listdir(directory) if file.endswith('.tif')]

def find_missing_files(expected_files, actual_files):
    """
    Compare expected and actual filenames to find missing files.
    
    Parameters:
        expected_files (list): List of expected filenames.
        actual_files (list): List of actual filenames.
    
    Returns:
        list: Sorted list of missing filenames.
    """
    missing_files = set(expected_files) - set(actual_files)
    return sorted(missing_files)

def save_missing_files(missing_files, output_file):
    """
    Save the list of missing files to a text file.
    
    Parameters:
        missing_files (list): List of missing filenames.
        output_file (str): Path to the output text file.
    """
    with open(output_file, 'w') as f:
        for file in missing_files:
            f.write(file + '\n')
    print(f"Missing files saved to {output_file}")

if __name__ == "__main__":
    # Parameters
    tiff_directory = '/home/prahlada/GWSA_clipped_Output'
    output_file = 'missing_files.txt'
    start_year = 2003
    end_year = 2021

    try:
        # Generate the list of expected file names
        expected_files = generate_expected_filenames(start_year, end_year)

        # Get the list of actual file names
        actual_files = get_actual_filenames(tiff_directory)

        # Find missing files
        missing_files = find_missing_files(expected_files, actual_files)

        if missing_files:
            print("Missing files:")
            for file in missing_files:
                print(file)
            save_missing_files(missing_files, output_file)
        else:
            print("No missing files found!")
    except Exception as e:
        print(f"Error: {e}")
