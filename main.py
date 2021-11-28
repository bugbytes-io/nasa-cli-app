from io import BytesIO
import os
import typer
import requests
from datetime import datetime
from config import API_URL, IMAGE_DIR
from PIL import Image

app = typer.Typer()

default_date = typer.Argument(
    datetime.now().strftime('%Y-%m-%d'),
    formats=['%Y-%m-%d']
)

@app.command()
def fetch_image(date: datetime = default_date, save: bool = False):
    print("Sending API request...")
    dt = str(date.date())

    # add the 'date' query parameter to the NASA API call
    url_for_date = f"{API_URL}&date={dt}"
    response = requests.get(url_for_date)

    # raise error if request fails
    response.raise_for_status()

    # extract url and title from JSON response
    data = response.json()

    if data['media_type'] != 'image':
        print(f"No image available for {data['date']}")
        return

    url = data['url']
    title = data['title']

    # fetch the Image from the url, and create PIL.Image object
    print("Fetching Image...")
    image_response = requests.get(url)
    image = Image.open(BytesIO(image_response.content))

    # show image on user's desktop
    image.show()

    # save image to filesystem if save flag is True
    if save:
        if not IMAGE_DIR.exists():
            os.mkdir(IMAGE_DIR)
        image_name = f"{title}.{image.format}"
        image.save(IMAGE_DIR / image_name, image.format)

    image.close()
    

if __name__ == '__main__':
    app()