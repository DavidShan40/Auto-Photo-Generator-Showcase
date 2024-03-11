import cv2
import os
from datetime import datetime

# Define the path to your folder containing the images

#folder_path = 'new_images/2024-02-19'  # Example: '/path/to/your/images'
cover_dir = "new_images"
today_date = datetime.now().strftime("%Y-%m-%d")
folder_path = os.path.join(cover_dir, today_date)
scale_factor = 2  # Define your scale factor

# Get all image files in the folder with common image extensions
image_files =  [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
print(image_files)

for image_path in image_files:
    # Load the image
    image = cv2.imread(image_path)

    # Calculate the new dimensions
    new_width = int(image.shape[1] * scale_factor)
    new_height = int(image.shape[0] * scale_factor)
    new_dim = (new_width, new_height)
    print(new_dim)
    # Upscale the image
    upscaled_image = cv2.resize(image, new_dim, interpolation=cv2.INTER_CUBIC)

    # Save the upscaled image, replacing the original
    cv2.imwrite(image_path, upscaled_image)

print("Upscaling completed for all images in the folder.")
