import typer
from datetime import datetime

app = typer.Typer()

@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")

default_date = typer.Argument(
    datetime.now().strftime('%Y-%m-%d'),
    formats=['%Y-%m-%d']
)

@app.command()
def day_of_week(date: datetime = default_date):
    typer.echo(date.strftime('%A'))

if __name__ == '__main__':
    app()