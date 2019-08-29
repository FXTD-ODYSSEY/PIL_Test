from pathlib import Path
from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw


if __name__ == '__main__':
    DIR = Path(__file__)
    path = DIR.parent / "test2.png"

    image = Image.open(path)
    width, height = image.size
    center = (int(0.5 * width), int(0.5 * height))
    yellow = (255, 255, 0, 255)
    ImageDraw.floodfill(image, xy=center, value=yellow)
    # image.save(output_img)
    image.show()
