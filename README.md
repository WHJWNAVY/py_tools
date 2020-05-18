# Python-Image_to_excel
最近在学习Python，闲着无聊开发了两个小软件，用到了pillow、openpyxl、等第三方库。

## py_img_to_excel.py:
主要原理就是打开一幅图片，依次读取图片每个像素的RGB值，然后把该值作为Excel表格中
对应单元格的背景色。最后再把每个单元格设置为高度与宽度相等的小正方形。

> 示例
![原图](https://raw.githubusercontent.com/WHJWNAVY/myImage/master/PicGo20200518102246.png)
![转换](https://raw.githubusercontent.com/WHJWNAVY/myImage/master/PicGo20200518102410.png)
![结果](https://raw.githubusercontent.com/WHJWNAVY/myImage/master/PicGo20200518102449.png)

py_img_to_txt.py:
主要原理就是打开一幅图片，然后对图像二值化，再依次读取图片每个像素的值写入到文本
文件中。如果大于0则写入"@",否则写入"_"。
> 示例
![原图](https://raw.githubusercontent.com/WHJWNAVY/myImage/master/PicGo20200518102246.png)
![转换](https://raw.githubusercontent.com/WHJWNAVY/myImage/master/PicGo20200518103305.png)
![结果](https://raw.githubusercontent.com/WHJWNAVY/myImage/master/PicGo20200518103331.png)
