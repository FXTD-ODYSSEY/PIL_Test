from PIL import Image
from PIL import Image
import random
import collections


def histeq(im, nbr_bins=256):
  data = im.flatten()
  imhist, bins = histogram(data, nbr_bins, normed=True)
  cdf = imhist.cumsum()
  cdf = 255 * cdf
  im2 = interp(im.flatten(), bins[:-1], cdf)
  return im2.reshape(im.shape)


def fn(filt):
  img1 = Image.open(dir + redbox1).transpose(Image.FLIP_TOP_BOTTOM)
  rgb2xyz = (
      1, 0, 0, 0,
      1, 0, 0, 0,
      1, 0, 0, 0)
  img1 = img1.convert("RGB", rgb2xyz)
  img1 = array(img1.convert('L'))
  img1 = histeq(img1)

  img1_f = 1 * (img1 > filt)

  return img1_f

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
