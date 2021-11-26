from io import BytesIO
import os
from typing import Dict
from PIL import Image
from config import IMAGE_DIR


def url_query_params(datetime, start, end) -> Dict:
    """ Generates correct URL query parameters based on CLI arguments """
    if start:
        params = {'start_date': str(start.date())}
        if end:
            params['end_date'] = str(end.date())
        return params
    else:
        return {'date': str(datetime.date())}

async def get_image(client, url: str) -> Image:
    """ Makes API request to Image endpoint, and converts/returns Pillow Image """
    image_response = await client.get(url)
    image = Image.open(BytesIO(image_response.content))
    return image

def save_image_to_filesystem(image: Image, title: str):
    if not IMAGE_DIR.exists():
        os.mkdir(IMAGE_DIR)
    image_name = f"{title}.{image.format}"
    image.save(IMAGE_DIR / image_name, image.format)