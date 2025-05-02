from rich.console import Console
from textual_image.renderable import Image as SImage

console = Console()


def imgshow(image):
    console.print(SImage(image))
