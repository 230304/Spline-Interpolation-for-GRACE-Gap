# Spline Interpolation for GRACE Gap

## Overview
This repository contains code and workflows for filling gaps in **GRACE satellite data** using **Spline Interpolation**. Due to the transition between GRACE and GRACE-FO missions, there exists a **10-month data gap** that needs to be addressed for continuous hydrological analysis. This project applies spline-based interpolation to estimate missing Total Water Storage Anomalies (TWSA) values, ensuring a seamless time-series dataset.

## Key Achievements
- **Preprocessing GRACE Data**: Converted and structured NetCDF files into a usable format (TIFF and arrays).
- **Handling Missing Data**: Identified and separated missing months in the dataset.
- **Interpolation via Splines**: Applied **cubic spline interpolation** to reconstruct missing values with high accuracy.
- **Optimized Geospatial Data Handling**: Processed large-scale satellite datasets efficiently.

## How to Use This Repository
This repository provides a structured approach for processing GRACE data, detecting missing values, and applying spline interpolation. The scripts perform the following tasks:

### 1. Data Conversion & Preprocessing
#### `netcdf_to_tiff.py`
- Converts **NetCDF** data to **GeoTIFF** format for easier spatial processing.
- Extracts relevant geophysical parameters from raw GRACE datasets.
- Output: TIFF files ready for geospatial analysis.

#### `combining_two_tiffs.py`
- Merges multiple TIFF files into a unified dataset.
- Used in an early approach to process spatial data before shifting to array-based methods.

#### `reorient_and_crop_tiffs.py`
- Reorients and crops TIFF files to match the study region’s extent.
- Primarily useful for refining geospatial datasets.

### 2. Identifying and Structuring Missing Data
#### `find_missing_files.py`
- Scans the dataset to detect missing GRACE monthly data files.
- Generates a structured list of missing time indices.

#### `create_stack_array_of_monthly_data.py`
- Constructs a **stacked array** representing GRACE TWSA values over time.
- Helps in preparing data for interpolation.

#### `separate_stack_arrays_for_all_months.py`
- Segregates monthly data stacks into individual month-wise arrays.
- Facilitates interpolation for specific missing months.

### 3. Performing Spline Interpolation
#### `spline_interpolation.py`
- Applies **Cubic Spline Interpolation** to estimate missing GRACE data.
- Uses available time-series data to interpolate missing values.
- Output: Reconstructed dataset with continuous monthly values.

## Requirements
Ensure you have the following dependencies installed before running the scripts:
```bash
pip install numpy pandas rasterio netCDF4 scipy matplotlib
```

## Running the Scripts
1. **Prepare the Data**
   - Convert NetCDF to TIFF: `netcdf_to_tiff.py`
   - Process and refine data: `reorient_and_crop_tiffs.py`
   - Detect missing months: `find_missing_files.py`

2. **Structure Data for Interpolation**
   - Create stacked arrays: `create_stack_array_of_monthly_data.py`
   - Separate monthly data: `separate_stack_arrays_for_all_months.py`

3. **Interpolate Missing Data**
   - Run `spline_interpolation.py` to fill the GRACE gap.

## Future Work
- **Validation with External Datasets**: Compare interpolated results with independent hydrological datasets.
- **Integration with ML Models**: Combine with machine learning approaches for enhanced predictions.
- **Global Application**: Extend methodology to other regions affected by GRACE data gaps.

For any questions or contributions, feel free to reach out!

