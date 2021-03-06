# PIL 测试

> &emsp;&emsp;这次潜心研究PIL图片处理，其实也是为了完成某大厂提供的测试题     
> &emsp;&emsp;这个测试题需要我对图形三个通道进行相应的处理     
> &emsp;&emsp;前面两个通道好弄，因为 PIL 已经将相关的算法封装起来     
> &emsp;&emsp;只管调用就可以解决问题     
> 
> &emsp;&emsp;对我来说最难的是第三个通道的处理     
> &emsp;&emsp;需要更具第二个通道算出的边缘线找出每一个闭合的图形区间     
> &emsp;&emsp;然后分别对每一个区间的中心点采样y值，将y值转换为 UV 空间 0 - 1 的区间     
> &emsp;&emsp;这个闭合区域的颜色就取 y 值。     
> 
> &emsp;&emsp;这题的难度在与如何寻找到相关的闭合区间     
> &emsp;&emsp;这个PIL并没有提供相关的解决方案，因此不能白嫖了。     
> &emsp;&emsp;在网上查了很多，有很多是使用 OpenCV 的解决方案，但是并不能在这道测试题上使用     
> &emsp;&emsp;因为测试题规定只能使用 PIL | Pillow 库     
> 
> &emsp;&emsp;所以这个问题很有难度。     
> &emsp;&emsp;经过我多方的搜索之后，我后来发现 PIL 有个函数 ImageDraw.floodfill 可以实现绘图工具的油漆桶效果。     
> &emsp;&emsp;那仔细想想油漆桶是怎么见闭合图形填充满的，似乎答案就在其中。     
> 
> &emsp;&emsp;因此我从PIL找到里面代码来研究这个东西原理。     
> &emsp;&emsp;最后也没有让我失望。     
> 
> &emsp;&emsp;油漆桶的原理是通过计算一个像素四周颜色相似值进行扩散。     
> &emsp;&emsp;□□□□□□□     
> &emsp;&emsp;□□□■□□□     
> &emsp;&emsp;□□■◆■□□     
> &emsp;&emsp;□□□■□□□     
> &emsp;&emsp;□□□□□□□     
> &emsp;&emsp;中间的菱形就是目标像素点，而四周四个方块像素点就是进行颜色比较的像素     
> &emsp;&emsp;如果颜色符合相似的阈值，那么就会在这个基础上对符合条件的像素再次进行扩散采样     
> &emsp;&emsp;如果颜色阈值不符就会停止，由于边界线的颜色差异是比较高的，通过这个方法就可以让颜色填充在边际线的位置停止。     
> 
> &emsp;&emsp;不过这个填充也有缺陷，没有办法控制扩散的阈值，只要边界线上有一个像素的缺口，就会让两个区域合为一体。     
> &emsp;&emsp;不过也算是解决了获取封闭区域了。     
> &emsp;&emsp;后续计算中间值其实很简单，求获取的像素点的横坐标和纵坐标的平均值即可。     
> 　
> 　
