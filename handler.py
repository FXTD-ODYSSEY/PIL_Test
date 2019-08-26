from pathlib import Path
from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw
from copy import deepcopy
import matplotlib.pyplot as plt

DIR = Path(__file__)


def _color_diff(color1, color2):
    """
    Uses 1-norm distance to calculate difference between two values.
    """
    if isinstance(color2, tuple):
        return sum([abs(color1[i] - color2[i]) for i in range(0, len(color2))])
    else:
        return abs(color1 - color2)

def findBoundry(image, xy, value, border=None, thresh=0):
    pixel = image.load()
    x, y = xy
    try:
        background = pixel[x, y]
        if _color_diff(value, background) <= thresh:
            return  # seed point already has fill color
        pixel[x, y] = value
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = {(x, y)}
    # use a set to keep record of current and previous edge pixels
    # to reduce memory consumption
    full_edge = set()
    
    index = 0
    while edge:
        index += 1
        new_edge = set()
        for (x, y) in edge:  # 4 adjacent method
            for (s, t) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (s, t) in full_edge:
                    continue  # if already processed, skip
                try:
                    p = pixel[s, t]
                except (ValueError, IndexError):
                    pass
                else:
                    full_edge.add((s, t))
                    if border is None:
                        fill = _color_diff(p, background) <= thresh
                    else:
                        fill = p != value and p != border
                    if fill:
                        pixel[s, t] = value
                        new_edge.add((s, t))
        
        full_edge = edge  # discard pixels processed
        edge = new_edge
        # if index >= 300:
        #     break


def main():
    # help(ImageDraw.floodfill)
    path = DIR.parent / "test2.png"

    img = Image.open(path)  # 打开图片

    r, g, b, a = img.split()  # 分离通道

    # ! ------------------------------------------------

    # NOTE R 通道进行高斯模糊 半径 3 像素
    blur_r = r.filter(ImageFilter.GaussianBlur(radius=3))

    # ! ------------------------------------------------
    # NOTE G 通道计算边缘检测结果 使用阈值控制边缘 大于 0.5 取 1 否则取 0
    # mask = g.convert("L")
    edge_g = g.filter(ImageFilter.FIND_EDGES)
    width, height = edge_g.size
    thersold = .3
    # NOTE 处理像素点
    for h in range(height):
        for w in range(width):
            if edge_g.getpixel((w, h))/255 < thersold:
                edge_g.putpixel((w, h), 0)
            else:
                edge_g.putpixel((w, h), 1)

    # ! ------------------------------------------------

    center = (int(0.5 * width), int(0.5 * height))
    # yellow = 255
    # ImageDraw.floodfill(edge_g, xy=center, value=yellow)
    
    _edge_g = deepcopy(edge_g)
    # ImageDraw.floodfill(_edge_g, xy=center, value=255)
    findBoundry(_edge_g, xy=center, value=255, thresh=0)

    # ! ------------------------------------------------
    # NOTE 显示图片
    plt.figure('Img Library')  # 设置figure
    plt.title('origin')
    plt.imshow(_edge_g)
    plt.axis('off')

    plt.show()


if __name__ == "__main__":
    main()
