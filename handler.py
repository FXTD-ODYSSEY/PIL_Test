from PIL import Image
from PIL import ImageFilter
from pathlib import Path
from itertools import product
import random
import os



def _color_diff(color1, color2):
    """_color_diff 判断颜色差异
    
    根据欧拉距离判断颜色差异

    Arguments:
        color1 {tuple} -- 颜色值
        color2 {tuple} -- 颜色值
    
    Returns:
        float -- 颜色相似程度
    """
    
    if isinstance(color2, tuple):
        return sum([abs(color1[i] - color2[i]) for i in range(0, len(color2))])
    else:
        return abs(color1 - color2)

def _listed(num,region=1,step=1):
    """_listed 数字展开成数组

    _listed(3,2)    返回 [1,2,3,4,5]
    _listed(10,3,2) 返回 [4,6,8,10,12,14,16]

    
    Arguments:
        num {int} -- 延展的数字
    
    Keyword Arguments:
        region {int} -- 延展的数字的个数 (default: {1})
        step {int} -- 延展的步长 (default: {1})
    
    Raises:
        RuntimeError: 如果 region 或 step 小于零则报错
    
    Returns:
        list -- 返回延展数组
    """
    if region < 0 or step <0: raise RuntimeError()
    return range(num-region*step, num+1+region*step, step)

def getBoundry(image,total=None,done=None,thresh=.1):
    """getBoundry 寻找边界
    
    这里基于油漆桶的实现方法查找到物体边界
    油漆桶的原理是对任意一个像素点不断扩散范围，
    直到找到像素差异很大的颜值，这个颜色值会标记为边界

    Arguments:
        image {Image} -- PIL 获取的图片对象
    
    Keyword Arguments:
        total {list} -- 总像素 (default: {None})
        done {list} -- 完成的像素 (default: {None})
        thresh {float} -- 相似阈值 (default: {.1})
    
    Returns:
        list -- 完成的像素
    """
    if not total:
        width, height = image.size
        total = set([(w,h) for w,h in product(range(width),range(height))])

    pixel = image.load()
    
    # NOTE 说明目标点为边界线
    handle = total - done
    print ("handle",len(handle))
    if not handle:
        return set()
    # NOTE 提取元素
    for x, y in handle:break
    background = pixel[x, y]
    edge = {(x, y)}

    full_edge = {(x, y)}
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

def getAllBoundry(image,total=None,done=None, thresh=.1):
    """getAllBoundry 通过while循环查询图片所有的 Boundry 边界
    
    Arguments:
        image {Image} -- PIL 获取的图片对象
    
    Keyword Arguments:
        total {list} -- 总像素 (default: {None})
        done {list} -- 完成的像素 (default: {None})
        thresh {float} -- 相似阈值 (default: {.1})
    
    Returns:
        list -- 每一个区域的像素集合
    """
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


def findCenterPoint(data):
    """findCenterPoint 更具给定的像素数据寻找中心点
    
    Arguments:
        data {set} -- 像素数据
    
    Returns:
        tuple -- 中心点 x,y
    """
    # ! 找到中心点
    x_total = y_total= 0
    count = len(data)
    for x,y in data:
        x_total += x
        y_total += y
    x = round(x_total/count)
    y = round(y_total/count)
    return x,y

def fillColor(image,data):
    """fillColor 颜色填充
    
    根据中心点的像素值，对区域范围进行颜色填充
    
    Arguments:
        image {Image} -- PIL 获取的图片对象
        data {set} -- 像素数据
    """
    pixel = image.load()
    _,height = image.size
    _,y = findCenterPoint(data)
    color = round(y/height * 255)
    for x,y in data:
        pixel[x,y] = color


def imgHandler(path):

    img = Image.open(path)  # 打开图片

    r, g, b, a = img.split()  # 分离通道

    # ! ------------------------------------------------

    # NOTE R 通道进行高斯模糊 半径 3 像素
    r = r.filter(ImageFilter.GaussianBlur(radius=3))

    # ! ------------------------------------------------
    # NOTE G 通道计算边缘检测结果 使用阈值控制边缘 大于 0.5 取 1 否则取 0
    g = g.filter(ImageFilter.EDGE_ENHANCE).filter(ImageFilter.FIND_EDGES)
    width, height = g.size
    thersold = .5
    # NOTE 处理像素点
    for h in range(height):
        for w in range(width):
            if g.getpixel((w, h))/255 < thersold:
                g.putpixel((w, h), 0)
            else:
                g.putpixel((w, h), 255)

    # ! ------------------------------------------------

    for data in getAllBoundry(g, thresh=0.1):
        fillColor(b,data)

    # ! ------------------------------------------------
    
    pic = Image.merge('RGBA',(r,g,b,a))        #合并三通道
    
    # ! ------------------------------------------------

    return r,g,b,pic

def main():

    # NOTE 获取当前脚本的路径
    p = Path(__file__)
    output_r   = p.parent / "F_r" 
    output_g   = p.parent / "F_g" 
    output_b   = p.parent / "F_b" 
    output_pic = p.parent / "F_n" 
    if not os.path.exists(output_r   ): os.mkdir(output_r   )
    if not os.path.exists(output_g   ): os.mkdir(output_g   )
    if not os.path.exists(output_b   ): os.mkdir(output_b   )
    if not os.path.exists(output_pic ): os.mkdir(output_pic )

    # NOTE 遍历当前脚本所处的目录
    for folder in p.parent.iterdir():
        # NOTE 如果为 F 目录
        if folder.is_dir() and folder.stem == "F":
            for image in folder.iterdir():
                # NOTE 判断目录的后缀是否为 png 的图片
                if image.is_file() and image.suffix == ".png":
                    print (image.name)
                    r,g,b,pic = imgHandler(image)
                    r.save(output_r     / image.name)
                    g.save(output_g     / image.name)
                    b.save(output_b     / image.name)
                    pic.save(output_pic / image.name)
    
    # ! 单帧测试
    # name = "test (18).png"
    # r,g,b,pic = imgHandler(p.parent / "F"/ name)
    # r.save(output_r   / name)
    # g.save(output_g   / name)
    # b.save(output_b   / name)
    # pic.save(output_pic / name)



if __name__ == "__main__":
    main()
