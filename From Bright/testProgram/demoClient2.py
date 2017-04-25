import socket
from time import sleep
from time import time


host = '192.168.1.34'
port = 5560

def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def sendPic(s, filePath, fileName):
    print(filePath, fileName)
    pic = open(filePath, 'rb')
    chunk = pic.read(1024)
    ### ส่งคำสั่ง store ให้ server พร้อม ชื่อไฟล์รูป
    s.send(str.encode("STORE " + fileName))
    t = time()
    while chunk:
        print("Sending Picture")
        s.send(chunk)
        chunk = pic.read(1024)
    pic.close()
    print("Done sending")
    print("Elapsed time = " + str(time() - t) + 's')
    s.close()
    return "Done sending"


def backup(filePath, fileName):
    s = setupSocket()
    response = sendPic(s, filePath, fileName)
    return response

def main():

    picPath = 'temp1/ow.jpg'
    picName = 'ow.jpg'
    backup(picPath, picName)

main()
