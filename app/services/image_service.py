import os
import secrets
from fastapi import UploadFile

class ImageService:
    def __init__(self, static_dir: str = "static/images"):
        self.static_dir = static_dir
        os.makedirs(self.static_dir, exist_ok=True)

    async def save_image(self, image: UploadFile) -> tuple[bytes, str]:
        """
        Save uploaded image to static directory and return bytes and file path.
        """
        image_bytes = await image.read()
        
        filename = f"{secrets.token_hex(8)}_{image.filename}"
        filepath = os.path.join(self.static_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(image_bytes)
            
        return image_bytes, filepath
