from PIL import Image
from PIL import ImageDraw
import random
import collections

WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0


def main(width, height):
    flood = Image.new('RGB', (width, height), BLACK)
    # Create randomly generated walls
    for x in range(width):
        for y in range(height):
            flood.putpixel((x, y), BLACK if random.random() < 0.15 else WHITE)
    # Create borders
    for x in range(width):
        for y in range(height):
            if x in {0, width - 1} or y in {0, height - 1}:
                flood.putpixel((x, y), BLACK)

    # floodfill(50, 25, RED, flood)
    width, height = flood.size
    center = (int(0.5 * width), int(0.5 * height))
    color = (255, 255, 0, 255)
    ImageDraw.floodfill(flood, xy=center, value=color, thresh=0)
    flood.show()
    # # Save image
    # image.save('flood.png')


def floodFill(x,y, d,e,f, g,h,i, image):
    toFill = set()
    toFill.add((x,y))
    while not toFill.empty():
        (x,y) = toFill.pop()
        (a,b,c) == image.getpixel((x,y))
        if not (a,b,c) == (255, 255, 255):
            continue
        image.putpixel((x,y), (g,h,i))
        toFill.add((x-1,y))
        toFill.add((x+1,y))
        toFill.add((x,y-1))
        toFill.add((x,y+1))
    image.save("flood.png")

# def floodfill(x, y, color, image):
#     # if starting color is different from desired color
#     #     create a queue of pixels that need to be changed
#     #     while there are pixels that need their color changed
#     #         change the color of the pixel to what is desired
#     #         for each pixel surrounding the curren pixel
#     #             if the new pixel has the same color as the starting pixel
#     #                 record that its color needs to be changed
#     source = image.getpixel((x, y))
#     if source != color:
#         pixels = collections.deque([x, y])
#         while pixels:
#             place = pixels.popleft()
#             image.putpixel((x,y), color)
#             for x_offset in -1, 1:
#                 x_offset += x
#                 for y_offset in -1, 1:
#                     y_offset += y
#                     new_place = x_offset, y_offset
#                     if image.getpixel(new_place) == source:
#                         pixels.append(new_place)


if __name__ == '__main__':
    main(100, 50)
