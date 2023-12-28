# utils/image_utils.py
import os

def save_uploaded_image(uploaded_image):
    if uploaded_image:
        # Save the uploaded image to a temporary location
        # You may want to customize this based on your application's needs
        image_path = f"uploads/{uploaded_image.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_image.read())
        return image_path
