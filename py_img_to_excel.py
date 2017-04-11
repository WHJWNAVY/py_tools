from openpyxl.workbook import Workbook
from openpyxl.styles import PatternFill, Color
from PIL import Image
import datetime

def dec_to_base26(d):
    s = ""
    m = 0
    while d > 0:
        m = d % 26
        if m == 0:
            m = 26
        s = "{0:c}{1:s}".format(m+64, s)
        d = (d - m) // 26
    return s

def base26_to_dec(s):
    d = 0
    j = 1
    st = s.upper()
    for x in range(0, len(st))[::-1]:
        c = ord(st[x])
        if c < 65 and c > 90:
            return 0
        d += (c - 64) * j
        j *= 26
    return d

def decxy_to_excelxy(x, y):
    return("{0:s}{1:d}".format(dec_to_base26(x), y))

def pixel_to_xrgbstr(pix):
    return ("00{0:02X}{1:02X}{2:02X}".format(pix[0], pix[1], pix[2]))

def image_to_excel(imgName):

    #Create excel workbook
    wb = Workbook()
    ws = wb.active

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
    index = 0

    print("Start Process!")
    for w in range(width):
        index += 1
        print("#", end="")
        if index > 80:
            index = 0
            print("")

        for h in range(height):
            pixel = img.getpixel((w, h))
            loc = decxy_to_excelxy(w+1, h+1)
            #print("LOC", loc)
            c = ws[loc]
            col = pixel_to_xrgbstr(pixel)
            #print("COL", col)
            cfill = PatternFill(fill_type="solid", start_color=col)
            c.fill = cfill
            ws.column_dimensions[dec_to_base26(w+1)].width = 1
            ws.row_dimensions[h+1].height = 6

    print("\nProcess Done!")
    timenow = datetime.datetime.now()
    timestr = timenow.strftime("%Y-%m-%d-%H-%M-%S")
    namestr = "{0}-{1}.xlsx".format(imgName, timestr)
    print("Save File As [{0}]".format(namestr))
    wb.save(namestr)
    print("Save Done!")

name = input("Please Input Image File Name:")
print("Start......")
try:
    image_to_excel(name)
except:
    print("Error!!!!!!")
print("Over......")


