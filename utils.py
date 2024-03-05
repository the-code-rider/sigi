import io
import base64
from PIL import Image



def base64_to_image(base64_image):
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))

    return image
