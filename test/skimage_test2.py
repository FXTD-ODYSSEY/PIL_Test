import matplotlib.pyplot as plt
from pathlib import Path
from skimage import measure, data, color,io

DIR = Path(__file__)

path = DIR.parent / "test.png"

#生成二值测试图像
img=color.rgb2gray(io.imread(path))

#检测所有图形的轮廓
contours = measure.find_contours(img, .4)

#绘制轮廓
fig, axes = plt.subplots(1,2,figsize=(8,8))
ax0, ax1= axes.ravel()
ax0.imshow(img,plt.cm.gray)
ax0.set_title('original image')

rows,cols=img.shape
ax1.axis([0,rows,cols,0])
for n, contour in enumerate(contours):
    ax1.plot(contour[:, 1], contour[:, 0], linewidth=2)
ax1.axis('image')
ax1.set_title('contours')
plt.show()
