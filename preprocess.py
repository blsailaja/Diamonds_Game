import os
from PIL import Image

# Path to the images folder
folder_path = "images/"

# Iterate over all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".png"):
        file_path = os.path.join(folder_path, file_name)
        # Open the image
        img = Image.open(file_path)
        # Remove the color profile
        img = img.convert("RGB").convert("P", palette=Image.ADAPTIVE)
        img.save(file_path)
        print("Preprocessed:", file_name)
