from datetime import datetime
import typer
import requests

from config import API_URL
from helpers import url_query_params, get_image, save_image_to_filesystem


app = typer.Typer()

default_date = typer.Argument(
    datetime.now().strftime('%Y-%m-%d'),
    formats=['%Y-%m-%d']
)

@app.command()
def fetch_image(
    date: datetime = default_date, 
    save: bool = False,
    start: datetime = typer.Option(None),
    end: datetime = typer.Option(None),
):
    print("Sending API request...")
    query_params = url_query_params(date, start, end)

    # add the 'date' query parameter to the NASA API call
    response = requests.get(API_URL, params=query_params)

    # raise error if request fails
    response.raise_for_status()

    # extract url and title from JSON response
    data = response.json()

    # if the response data is a dict, convert to single-element list for convenience
    if isinstance(data, dict):
        data = [data]

    for resp in data:
        if resp['media_type'] != 'image':
            print(f"No image available for {resp['date']}")
            continue
        
        url = resp['url']
        title = resp['title']

        # fetch the Image from the url, and create PIL.Image object
        print("Fetching Image...")
        image = get_image(url)

        # show image on user's desktop
        image.show()

        # save image to filesystem if save flag is True
        if save:
            save_image_to_filesystem(image, title)

        image.close()
    

if __name__ == '__main__':
    app()