import os
import xarray as xr
import logging

# Set up logging for tracking progress and issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Example paths (replace these with your actual paths)
NC_FILE_PATH = "example_data/GLDAS_NOAH025_M.A200201.021.nc4"  # Dummy input NetCDF file path
OUTPUT_FOLDER = "output_tiffs"  # Folder to save GeoTIFF files

# Configuration for processing
VARIABLE_NAME = "SoilMoi40_100cm_inst"  # Name of the variable to extract
YEARS = range(2002, 2003)  # Example range of years
MONTHS = range(1, 2)  # Example range of months (January to December)


def process_variable_to_tiff(nc_file_path, output_folder, variable_name, years, months):
    """
    Extracts a specified variable from a NetCDF file and saves it as GeoTIFF files
    for a given range of years and months.

    Parameters:
        nc_file_path (str): Path to the NetCDF file.
        output_folder (str): Directory to save the output GeoTIFF files.
        variable_name (str): Name of the variable to extract.
        years (range): Range of years to process (e.g., range(2002, 2019)).
        months (range): Range of months to process (e.g., range(1, 13)).

    Raises:
        ValueError: If the specified variable is not found in the NetCDF file.
    """
    # Check if the NetCDF file exists
    if not os.path.exists(nc_file_path):
        logging.error(f"NetCDF file not found at {nc_file_path}")
        return

    # Open the NetCDF file
    logging.info("Loading NetCDF file...")
    ds = xr.open_dataset(nc_file_path)

    # Check if the specified variable exists
    if variable_name not in ds.variables:
        logging.error(f"Variable '{variable_name}' not found in the NetCDF file.")
        return

    # Ensure the variable has a CRS assigned
    ds[variable_name] = ds[variable_name].rio.write_crs("EPSG:4326")

    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through the specified years and months
    for year in years:
        for month in months:
            date_str = f"{year}-{month:02d}"
            try:
                # Select data for the specific time
                logging.info(f"Processing data for {date_str}...")
                variable_data = ds[variable_name].sel(time=date_str, method="nearest")

                # Ensure spatial dimensions and CRS
                variable_data = variable_data.rio.set_spatial_dims("lon", "lat")
                variable_data = variable_data.rio.set_crs("EPSG:4326")

                # Output file path
                output_tif_path = os.path.join(
                    output_folder, f"{variable_name}_{year}_{month:02d}.tif"
                )

                # Save the data as a GeoTIFF file
                variable_data.rio.to_raster(output_tif_path)
                logging.info(f"GeoTIFF saved to {output_tif_path}")

            except KeyError:
                # Handle missing data for the specified time
                logging.warning(f"No data found for {date_str}. Skipping...")
                continue

    logging.info("Processing complete.")


if __name__ == "__main__":
    """
    Main script logic:
    - Calls the function to extract variable data and save it as GeoTIFF files.
    - Ensures proper configuration and dummy inputs for GitHub-readiness.
    """
    logging.info("Starting the NetCDF to GeoTIFF processing...")
    
    process_variable_to_tiff(
        nc_file_path=NC_FILE_PATH,
        output_folder=OUTPUT_FOLDER,
        variable_name=VARIABLE_NAME,
        years=YEARS,
        months=MONTHS
    )
    
    logging.info("Script execution finished.")
