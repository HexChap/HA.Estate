from dataclasses import dataclass
from typing import Mapping

from PIL import Image


@dataclass
class WatermarkPasteData:
    im: Image.Image
    box: tuple[int, int]
    mask: Image.Image

    def keys(self):
        return ["im", "box", "mask"]

    def __getitem__(self, key):
        return getattr(self, key)