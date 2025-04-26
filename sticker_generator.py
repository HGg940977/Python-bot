from PIL import Image
import io

class StickerGenerator:
    @staticmethod
    def process_image(image_data):
        """
        Process the input image to meet Telegram sticker requirements
        """
        # Open the image from bytes
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGBA if needed
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Resize image to fit Telegram requirements while maintaining aspect ratio
        image.thumbnail((512, 512), Image.Resampling.LANCZOS)
        
        # Create a new image with white background
        new_image = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
        
        # Calculate position to center the image
        x = (512 - image.width) // 2
        y = (512 - image.height) // 2
        
        # Paste the resized image onto the background
        new_image.paste(image, (x, y), image)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        new_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()