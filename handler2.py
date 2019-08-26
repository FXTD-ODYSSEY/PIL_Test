from pathlib import Path
from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw
from copy import deepcopy
import matplotlib.pyplot as plt
from itertools import product
from itertools import combinations
import random
from skimage import measure, draw

DIR = Path(__file__)


def _color_diff(color1, color2):
    """
    Uses 1-norm distance to calculate difference between two values.
    """
    if isinstance(color2, tuple):
        return sum([abs(color1[i] - color2[i]) for i in range(0, len(color2))])
    else:
        return abs(color1 - color2)

def _listed(num,region=1,step=1):
    if region < 0 or step <0: raise RuntimeError()
    return range(num-region*step, num+1+region*step, step)

def getBoundry(image,total=None,done=None, thresh=.1):
    # image = deepcopy(image)

    if not total:
        width, height = image.size
        total = set([(w,h) for w,h in product(range(width),range(height))])

    pixel = image.load()
    
    # NOTE 说明目标点为边界线
    handle = list(total - done)
    if not handle:
        return set()
    xy = handle[random.randint(0,len(handle)-1)]
    x, y = xy
    background = pixel[x, y]

    edge = {(x, y)}

    full_edge = set()
    while edge:
        new_edge = set()
        for (x, y) in edge:  # 4 adjacent method
            for (s, t) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (s, t) in full_edge or s < 0 or t < 0:
                    continue  # if already processed, skip
                try:
                    p = pixel[s, t]
                except (ValueError, IndexError):
                    pass
                else:
                    full_edge.add((s, t))
                    fill = _color_diff(p, background) <= thresh

                    if fill:
                        # Note 颜色相符符合填充条件
                        # pixel[s, t] = value
                        new_edge.add((s, t))
                        
        edge = new_edge

    # ! 填充颜色
    # for s,t in full_edge:
    #     pixel[s, t] = 255
    return full_edge

def getAllBoundry(image, xy=(0,0),total=None,done=None, thresh=.1):

    if not total:
        width, height = image.size
        total = set([(w,h) for w,h in product(range(width),range(height))])

    done = set()
    result = []
    while total != done:
        data = getBoundry(image,total,done,thresh)
        result.append(data)
        done.update(data)
    
    # ! 添加颜色看看是否全部运行了
    # pixel = image.load()
    # for s,t in done:
    #     pixel[s, t] = 255

    return result


def findCenterPoint():
    pass
    # ! 找到中心点
    # s_total = t_total= 0
    # count = len(full_edge)
    # for s,t in full_edge:
    #     s_total += s
    #     t_total += t
    # s = round(s_total/count)
    # t = round(t_total/count)
    # print (s,t)
    # pixel[s,t] = 100
    


def main():
    # help(ImageDraw.floodfill)
    path = DIR.parent / "test.png"
    output = DIR.parent / "output.png"

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
    thersold = .5
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
    
    getAllBoundry(edge_g, xy=center, thresh=0)

    # ! ------------------------------------------------
    # NOTE 显示图片
    plt.figure('Img Library')  # 设置figure
    plt.title('origin')
    plt.imshow(edge_g)
    plt.axis('off')

    plt.show()
    edge_g.save(output)

if __name__ == "__main__":
    main()
