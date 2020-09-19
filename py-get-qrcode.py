import qrcode
import datetime
import os,getpass

qrstr = input("Enter the string to be converted:")
print("Input :"+qrstr)
qrimg = qrcode.make(qrstr)
timenow = datetime.datetime.now()
timestr = timenow.strftime("%Y-%m-%d-%H-%M-%S")
qrname = "C:\\Users\\{0}\\Desktop\\{1}.png".format(getpass.getuser(), timestr)
print("Save as :", qrname)
qrimg.save(qrname)
print("Success!")