import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def process_tiff_image(tiff_path, output_path, crop_rows=120):
    """
    Processes a TIFF image to reorient (flip spatially) and crop it.
    
    Parameters:
        tiff_path (str): Path to the input TIFF file.
        output_path (str): Path to save the processed TIFF file.
        crop_rows (int): Number of rows to remove from the bottom of the image.
    
    Returns:
        None
    """
    if not os.path.exists(tiff_path):
        raise FileNotFoundError(f"Input TIFF file not found at {tiff_path}")
    
    # Load the TIFF image
    image = Image.open(tiff_path)
    print(f"Original image mode: {image.mode}, size: {image.size}")

    # Convert the image to a numpy array with floating-point values
    image_array = np.array(image)
    print(f"Image array shape: {image_array.shape}, dtype: {image_array.dtype}")

    # Crop the bottom rows
    cropped_array = image_array[:-crop_rows, :]
    print(f"Image array shape after cropping: {cropped_array.shape}")

    # Invert the image values
    min_val = np.min(cropped_array)
    max_val = np.max(cropped_array)
    inverted_array = -min_val + cropped_array
    print(f"Original array range: {min_val} to {max_val}")
    print(f"Inverted array range: {np.min(inverted_array)} to {np.max(inverted_array)}")

    # Get image dimensions
    height, width = inverted_array.shape

    # Split the image into two halves
    left_half = inverted_array[:, :width // 2]
    right_half = inverted_array[:, width // 2:]

    # Swap the halves to reorient the image
    reoriented_array = np.hstack((right_half, left_half))
    print(f"Reoriented array shape: {reoriented_array.shape}")

    # Convert the reoriented array back to an image
    reoriented_image = Image.fromarray(reoriented_array, mode='F')

    # Save the processed image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    reoriented_image.save(output_path)
    print(f"Reoriented image saved at {output_path}")

    # Display the reoriented image for verification
    plt.imshow(reoriented_array, cmap='gray')
    plt.title('Reoriented Image')
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    """
    Main script logic:
    - Modify the file paths and parameters as needed.
    """
    # Input and output paths (update these paths as per your system)
    input_tiff_path = "/home/prahlada/GRACE WORK/DATA/RAW/GRACE_DATA_Absolute/TWS_absolut/TWSA_200204_cm_CSR_0.25_MASCON_LM.tif"
    output_tiff_path = "/home/prahlada/GRACE WORK/DATA/EXTRACTED DATA/reoriented_file.tif"

    # Process the TIFF image
    process_tiff_image(tiff_path=input_tiff_path, output_path=output_tiff_path, crop_rows=120)
