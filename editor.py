from io import BytesIO
from pathlib import Path

import aiofiles
from PIL import Image, ImageOps


class ImageEditor:
    def __init__(
            self,
            in_paths: list[Path],
            out_path: Path | str
    ):
        self.images = [Image.open(path) for path in in_paths]
        self.output_path: Path = Path(out_path)

    async def add_logo(self):
        pass

    def rename_images(self):
        pass

    def compress_images(self):
        pass

    @staticmethod
    def _resize_with_proportion():
        pass

    @staticmethod
    def _calc_logo_width():
        pass

    async def _save_image(self, image: Image.Image):
        image.save(buf := BytesIO(), format="JPEG")
        path = self.output_path / Path(image.filename).name

        async with aiofiles.open(path, "wb") as file:
            await file.write(buf.getbuffer())
