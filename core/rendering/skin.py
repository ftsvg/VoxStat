from PIL import Image, UnidentifiedImageError
from io import BytesIO

from core.api import fetch_skin_model


async def render_skin(
    image: Image.Image,
    uuid: str,
    position: tuple[int, int],
    size: tuple[int, int],
    style: str = 'full'
) -> None:
    try:
        skin_data = await fetch_skin_model(uuid, style)
        skin_model = BytesIO(skin_data)
        skin = Image.open(skin_model).convert("RGBA").resize(size)

        image.paste(skin, position, mask=skin.split()[3])
    except (UnidentifiedImageError, Exception) as error:
        print("render_skin error:", error)