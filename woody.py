import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configure your Cloudinary credentials
cloudinary.config(
    cloud_name="dtb2lrzet",
    api_key="475625168932265",
    api_secret="QRZneD3fqb8G1vpNnMJ5JofE_MA"
)

# Example usage
if __name__ == "__main__":
    # Path to the image file
    image_path = "path/to/your/image.jpg"  # Replace with the actual file path

    # Optional parameters
    folder = "example_folder"  # Replace with desired folder name, or set to None
    public_id = "custom_image_name"  # Replace with desired public ID, or set to None
    transformation = {"width": 500, "height": 500, "crop": "limit"}  # Set transformation options, or set to None

    # Upload the image
    upload_image(image_path, folder=folder, public_id=public_id, transformation=transformation)
