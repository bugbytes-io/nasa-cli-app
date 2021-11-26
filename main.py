import asyncio
from datetime import datetime
import typer
import requests
import httpx

from config import API_URL
from helpers import url_query_params, get_image, save_image_to_filesystem


app = typer.Typer()

default_date = typer.Argument(
    datetime.now().strftime('%Y-%m-%d'),
    formats=['%Y-%m-%d']
)

async def get_images(urls):
    async with httpx.AsyncClient() as client:
        tasks = []
        for url in urls:
            tasks.append(
                asyncio.create_task(get_image(client, url))
            )
        images = await asyncio.gather(*tasks)
        return images
        



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

    # extract URLs and titles from the JSON data
    urls = [d['url'] for d in data]
    titles = [d['title'] for d in data]

    # run async/concurrent get_images code and collect Image objects after completion
    images = asyncio.run(get_images(urls))

    # iterate over collected images, show, and optionally save to desktop.
    for i, image in enumerate(images):

        # show image on user's desktop
        image.show()

        # save image to filesystem if save flag is True
        if save:
            save_image_to_filesystem(image, titles[i])

        image.close()
    

if __name__ == '__main__':
    app()