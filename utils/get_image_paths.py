from mimetypes import init, types_map
import os
from pathlib import Path
init()


def get_image_paths(target_dir: str) -> list[Path]:
    """

    :param target_dir:str: Absolute path in where to seek for image files
    :return:(list[Path]): Possibly empty list of paths
    """

    image_paths = []
    target_dir = Path(target_dir)
    files = os.listdir(target_dir)
    image_exts = [
        ext.strip(".")
        for ext in types_map
        if types_map[ext].split("/")[0] == "image"
    ]

    for file in files:
        if file.split(".")[-1] in image_exts:
            image_paths.append(target_dir / file)

    return image_paths
