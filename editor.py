import asyncio
import os.path
from io import BytesIO
from pathlib import Path

import aiofiles
from PIL import Image

from utils.types import WatermarkPasteData


class ImageEditor:
    def __init__(
            self,
            in_paths: list[Path],
            out_path: Path | str
    ):
        self.images: list[Image] = [Image.open(path) for path in in_paths]
        self.output_path: Path = Path(out_path)

        self.watermark: Image.Image = Image.open(Path("data") / "logo.png")

    async def add_logo(self):
        async with asyncio.TaskGroup() as tg:
            for image in self.images:
                image.paste(**self._prepare_watermark(image))
                tg.create_task(self._save_image(image))

    async def rename_images(self, new_name: str = ""):
        async with asyncio.TaskGroup() as tg:
            for i, image in enumerate(self.images):
                image_dir = Path(image.filename).parent
                _, image_ext = os.path.splitext(image.filename)

                image.filename = image_dir / f"{new_name}{i}{image_ext}"
                tg.create_task(self._save_image(image))

    def _prepare_watermark(self, image: Image.Image) -> WatermarkPasteData:
        transparency_percent = 65

        watermark_width = self._calc_watermark_width(image)
        mask = self.watermark.split()[3].point(lambda i: i * transparency_percent / 100.)

        watermark = self._resize_with_proportion(self.watermark, watermark_width)
        mask = self._resize_with_proportion(mask, watermark_width)

        x = int((image.size[0] / 2) - (watermark.size[0] / 2))
        y = int((image.size[1] / 2) - (watermark.size[1] / 2))

        return WatermarkPasteData(
            im=watermark,
            box=(x, y),
            mask=mask
        )

    @staticmethod
    def _resize_with_proportion(watermark: Image.Image, base_width: int):
        ratio = (base_width / float(watermark.size[0]))
        height = int((float(watermark.size[1]) * float(ratio)))
        return watermark.resize((base_width, height), Image.ANTIALIAS)

    @staticmethod
    def _calc_watermark_width(image: Image.Image):
        """
        Calculates watermark's width according to the image it will be applied to.

        :param image: target image
        :return:int: calculated width
        """

        # FIXME: Search for better algorithm?
        return int(image.size[0] * (0.20 if image.size[0] > image.size[1] else 0.40))

    async def _save_image(self, image: Image.Image):
        """
        Asynchronously saves images.

        :param image: Image to save
        :return:
        """

        image.save(buf := BytesIO(), format="JPEG")
        path = self.output_path / Path(image.filename).name

        async with aiofiles.open(path, "wb") as file:
            await file.write(buf.getbuffer())
