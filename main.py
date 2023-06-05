import asyncio
import time

from utils import get_image_paths
from editor import ImageEditor


async def main():
    editor = ImageEditor(
        get_image_paths(r"D:\.Development\.Python\.ActiveProjects\HA.Estate\data\in"),
        r"D:\.Development\.Python\.ActiveProjects\HA.Estate\data\out"
    )

    await editor.add_logo()

asyncio.run(main())
