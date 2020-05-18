from PIL import Image  # 导入Image库用与操作图片文件
import datetime


def image_to_txt(imgName, imgSize=0):
    # 获取当前时间,转换成字符串
    timenow = datetime.datetime.now()
    timestr = timenow.strftime("%Y-%m-%d-%H-%M-%S")
    # 生成的Txt文件用<原图片文件名+ 当前时间字符串+ ".txt"后缀>作为文件名
    namestr = "{0}-{1}.txt".format(imgName, timestr)

    # 打开或创建一个TxT文件文件
    txt = open(namestr, "w+")

    # 打开图片文件文件
    print("Open Image File [{0}]".format(imgName))
    try:
        img = Image.open(imgName)
    except:
        print("Error to Open [{0}]!!!".format(imgName))

    # 判断图片文件的格式, 这里必须为"RGB"格式, 如果不是"RGB"格式,
    # 则用convert函数转换成"RGB"格式.
    if "RGB" == img.mode:
        print("Size{0},Format({1}),Color({2})".format(
            img.size, img.format, img.mode))
    else:
        print("Not a RGB image file!!!")
        img = img.convert("RGB")
        print("Convert to RGB Success!!!")

    # 获取图片文件宽和高
    width = img.size[0]
    height = img.size[1]

    zoom = 0

    # 如果图片文件大于 400*400像素,则对图片进行缩放,缩放比例依照宽度和高度中的最大值
    PIC_MAXSIZE = imgSize

    if PIC_MAXSIZE != 0:
        if width >= height:
            maxsize = width
        else:
            maxsize = height
        if maxsize >= PIC_MAXSIZE:
            zoom = maxsize / PIC_MAXSIZE
            width = int(width / zoom)
            height = int(height / zoom)
            img = img.resize((width, height))
            print("Image Size too large, Resize to", img.size)

    # 把图片文件转换成纯黑白的图片
    img = img.convert("L")
    index = 0
    # img.save("{0}{1}".format(imgName, ".jpg"))

    # pixel_color = [" ", ".", ",", "-", ":", ";", "=", "c", "x", "g", "?", "%", "*", "#", "@", "C", "X", "G", "M"]
    pixel_color = [" ", "`", ",", "^", "\"", "|", ";", "?", "1", "7", "k", "%", "4", "&", "D", "H", "@", "N", "#", "M"]
    # pixel_color = ["  ", "__", "▁", "▂", "▃", "▅", "▆", "▇", "▉"]
    pixel_count = len(pixel_color) - 1

    print("Start Process!")

    for h in range(height):  # 遍历图片的高度[0, height)
        # 显示处理进度
        index += 1
        print("#", end="")
        txt.write("/*")
        if index >= 60:  # 大于60换行
            index = 0
            print("")

        for w in range(width):  # 遍历图片的宽度,[0, width)
            pixel = img.getpixel((w, h))  # 获取图片当前坐标点的像素值
            if pixel != 0:
                pixel = int((pixel_count * pixel) / 256)
            pixel = pixel_count - pixel
            # print("w=", w, "h=", h, "pixel=", pixel)
            txt.write(pixel_color[pixel])

        txt.write("*/")
        txt.write("\n")

    # 保存新生成的TXT文件
    print("\nProcess Done!")
    print("Save File As [{0}]".format(namestr))
    txt.close()
    print("Save Done!")


img_name = input("Please Input Image File Name:")
img_size = input("Please Input Max Image Size(Default 0):")
try:
    img_size = int(img_size)
except:
    img_size = 0
print("Start......")
try:
    image_to_txt(img_name, img_size)
except:
    print("Error!!!!!!")
print("Over......")
