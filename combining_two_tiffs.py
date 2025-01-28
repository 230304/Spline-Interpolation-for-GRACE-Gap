import tifffile
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

def read_and_resize_image(image_path, resize=False, new_size=(1440, 600)):
    """
    Reads a TIFF image and optionally resizes it.

    Parameters:
        image_path (str): Path to the TIFF image.
        resize (bool): Whether to resize the image.
        new_size (tuple): Target size for resizing (width, height).

    Returns:
        np.ndarray: The processed image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    print(f"Reading image from {image_path}...")
    image = tifffile.imread(image_path)
    if resize:
        print(f"Resizing image to {new_size}...")
        image = cv2.resize(image, new_size)
    return image

def normalize_image(image):
    """
    Normalizes an image to the range [0, 255] and converts it to uint8.

    Parameters:
        image (np.ndarray): Input image.

    Returns:
        np.ndarray: Normalized image.
    """
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

def combine_images(img1, img2, alpha=0.5, beta=0.5, gamma=0):
    """
    Combines two images using weighted addition.

    Parameters:
        img1 (np.ndarray): First image.
        img2 (np.ndarray): Second image.
        alpha (float): Weight of the first image.
        beta (float): Weight of the second image.
        gamma (float): Scalar added to each sum.

    Returns:
        np.ndarray: Combined image.
    """
    return cv2.addWeighted(img1, alpha, img2, beta, gamma)

def visualize_images(img1, img2, combined_img):
    """
    Visualizes the input and combined images using matplotlib.

    Parameters:
        img1 (np.ndarray): First image.
        img2 (np.ndarray): Second image.
        combined_img (np.ndarray): Combined image.
    """
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.imshow(img1, cmap='gray')
    plt.title("Image 1")
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(img2, cmap='gray')
    plt.title("Image 2")
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(combined_img, cmap='gray')
    plt.title("Combined Image")
    plt.axis('off')

    plt.show()

# Main script
if __name__ == "__main__":
    # File paths
    tif1_img_path = "/path/to/image1.tif"
    tif2_img_path = "/path/to/image2.tif"

    try:
        # Read and resize images
        resize_for_testing = True
        tif1_img = read_and_resize_image(tif1_img_path, resize=resize_for_testing)
        tif2_img = read_and_resize_image(tif2_img_path, resize=resize_for_testing)

        print(f"Image 1 shape: {tif1_img.shape}")
        print(f"Image 2 shape: {tif2_img.shape}")

        if tif1_img.shape != tif2_img.shape:
            raise ValueError("Error: Images are not the same size!")

        # Normalize images
        tif1_img = normalize_image(tif1_img)
        tif2_img = normalize_image(tif2_img)

        # Combine images
        combined_img = combine_images(tif1_img, tif2_img)

        # Save the combined image
        combined_img_path = "combined_image.tif"
        print(f"Saving combined image to {combined_img_path}...")
        cv2.imwrite(combined_img_path, combined_img)

        # Visualize images
        visualize_images(tif1_img, tif2_img, combined_img)

        print("Processing complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
