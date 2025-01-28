import numpy as np
from scipy.interpolate import interp1d

def interpolate_missing_data_3d_spline(data_3d, missing_index):
    """
    Interpolate missing data in a 3D array using cubic spline interpolation for a specified missing index.

    Parameters:
        data_3d (numpy.ndarray): 3D array with shape (time, x, y) representing time series data.
        missing_index (int): Index along the time axis where data is missing.

    Returns:
        numpy.ndarray: 3D array with missing data interpolated for the specified index.
    """
    time_steps, x_dim, y_dim = data_3d.shape
    
    # Create a copy of the original data to store interpolated values
    interpolated_data = np.copy(data_3d)
    
    # Iterate over all spatial locations (x, y)
    for x in range(x_dim):
        for y in range(y_dim):
            # Extract the time series for the current (x, y) location
            time_series = data_3d[:, x, y]
            
            # Find valid indices (excluding the missing index)
            valid_indices = [i for i in range(time_steps) if i != missing_index]
            valid_time_points = np.array(valid_indices)
            valid_data_points = time_series[valid_time_points]
            
            # Check if there are enough valid data points to perform interpolation
            if len(valid_data_points) >= 2:
                # Create the cubic spline interpolator function
                interpolator = interp1d(valid_time_points, valid_data_points, kind='cubic', fill_value="extrapolate")
                
                # Interpolate missing data point
                interpolated_data[missing_index, x, y] = interpolator(missing_index)
            else:
                print(f"Not enough valid data to interpolate at position ({x}, {y}). Skipping...")
    
    return interpolated_data
