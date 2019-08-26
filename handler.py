from pathlib import Path
from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw
from copy import deepcopy
import matplotlib.pyplot as plt
from itertools import product
from itertools import combinations
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

def findBoundry(image, xy, value, border=None, thresh=.1):
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
    bound = set()
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
                        # Note 颜色相符符合填充条件
                        pixel[s, t] = value
                        new_edge.add((s, t))
                    else:
                        if (s,t) in bound:
                            continue
                        bound.add((s,t))
                
                        # Note 颜色不相符说明当前方块为边界方块
                        p = pixel[s, t]

                        l_flag = False
                        r_flag = False
                        d_flag = False
                        u_flag = False
                        for a, b in product(_listed(s), _listed(t)):
                            # i
                            
                            # NOTE 如果为True说明是边界线 如果不是则是空白
                            try:
                                check = _color_diff(p, pixel[a,b]) <= thresh or _color_diff(200, pixel[a,b]) <= thresh
                            except:
                                # import traceback
                                # traceback.print_exc()
                                # pixel[s, t] = 200
                                continue
                            if check:
                                if a < s and not l_flag:
                                    l_flag = True
                                if a > s and not r_flag:
                                    r_flag = True
                                if b < t and not u_flag:
                                    u_flag = True
                                if b > t and not d_flag:
                                    d_flag = True
                        
                        # NOTE 找出不连续点的情况
                        if not ((l_flag and r_flag) or (d_flag and u_flag)):
                            pixel[s, t] = 200

                        
        
        full_edge = edge  # discard pixels processed
        edge = new_edge
        # if index >= 300:
        #     break


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
    _edge_g.save(output)

if __name__ == "__main__":
    main()
