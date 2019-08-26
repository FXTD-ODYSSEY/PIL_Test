from PIL import Image
import matplotlib.pyplot as plt

path = r""
img = Image.open(path)         #打开图片

gray = img.convert('L')                 #转化灰度图

r,g,b = img.split()                     #分离三通道

pic = Image.merge('RGB',(r,g,b))        #合并三通道


plt.figure('pokemon')                   #设置figure

plt.subplot(2,3,1)                      #图一
plt.title('origin')
plt.imshow(img)
plt.axis('off')

plt.subplot(2,3,2),                     #图二
plt.title('gray')
plt.imshow(gray,cmap='gray')
plt.axis('off')

plt.subplot(2,3,3)                      #图三
plt.title('merge')
plt.imshow(pic)
plt.axis('off')

plt.subplot(2,3,4)                      #图四                         
plt.title('r')  
plt.imshow(r,cmap='gray')                                   
plt.axis('off')

plt.subplot(2,3,5)                      #图五
plt.title('g')
plt.imshow(g,cmap='gray')                           
plt.axis('off')

plt.subplot(2,3,6)                      #图六
plt.title('b')
plt.imshow(b,cmap='gray')                                       
plt.axis('off')

plt.show()

