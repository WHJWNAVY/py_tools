from PIL import Image
import datetime

def image_to_txt(imgName):
    timenow = datetime.datetime.now()
    timestr = timenow.strftime("%Y-%m-%d-%H-%M-%S")
    namestr = "{0}-{1}.txt".format(imgName, timestr)
    
    #Open tet file
    txt = open(namestr, "w+")
    
    #Open image file
    print("Open Image File [{0}]".format(imgName))
    try:
        img = Image.open(imgName)
    except:
        print("Error to Open [{0}]!!!".format(imgName))

    #Judge the image file format
    #if "RGB" in img.mode:
    if "RGB" == img.mode:
        print("Size{0},Format({1}),Color({2})".format(img.size, img.format, img.mode))
    else:
        print("Not a RGB image file!!!")
        img = img.convert("RGB")
        print("Convert to RGB Success!!!")

    width = img.size[0]
    height = img.size[1]

    zoom = 0

    #Resize large image
    if width >= height:
        maxsize = width
    else:
        maxsize = height
    if maxsize >= 400:
        zoom = maxsize / 400
        width = int(width / zoom)
        height = int(height / zoom)
        img = img.resize((width, height))
        print("Image Size too large, Resize to", img.size)
    
    #Convert to 2bit image
    img = img.convert("1")
    index = 0

    print("Start Process!")
    for w in range(width):
        index += 1
        print("#", end="")
        txt.write("/*")
        if index > 80:
            index = 0
            print("")

        for h in range(height):
            pixel = img.getpixel((w, h))
            if pixel != 0:
                txt.write("_")
            else:
                txt.write("@")
        txt.write("*/")
        txt.write("\n")
            

    print("\nProcess Done!")
    print("Save File As [{0}]".format(namestr))
    txt.close()
    print("Save Done!")

name = input("Please Input Image File Name:")
print("Start......")
try:
    image_to_txt(name)
except:
    print("Error!!!!!!")
print("Over......")

