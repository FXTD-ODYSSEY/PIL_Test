from pathlib import Path
from PIL import Image
from PIL import ImageFilter
import matplotlib.pyplot as plt

DIR = Path(__file__)


def main():
    path = DIR.parent / "test.png"

    img = Image.open(path)  # 打开图片

    r,g,b,a = img.split()  # 分离通道

    # ! ------------------------------------------------

    # NOTE R 通道进行高斯模糊 半径 3 像素
    blur_r = r.filter(ImageFilter.GaussianBlur(radius=3))

    # ! ------------------------------------------------
    # NOTE G 通道计算边缘检测结果 使用阈值控制边缘 大于 0.5 取 1 否则取 0
    # mask = g.convert("L")
    edge_g = g.filter(ImageFilter.FIND_EDGES)
    width,height = edge_g.size
    thersold = .5
    # NOTE 处理像素点
    for h in range(height):
        for w in range(width):
            if edge_g.getpixel((w, h))/255 < thersold:
                edge_g.putpixel((w,h),0)
            else:
                edge_g.putpixel((w,h),1)

    # ! ------------------------------------------------



    # ! ------------------------------------------------
    # NOTE 显示图片
    plt.figure('Img Library')  # 设置figure
    plt.title('origin')
    plt.imshow(edge_g)
    plt.axis('off')

    plt.show()


if __name__ == "__main__":
    main()
