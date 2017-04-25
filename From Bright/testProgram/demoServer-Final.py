import socket


host = ''
port = 5560

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    return s

def setupConnection():
    s.listen(1) # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

### store file เก็บใน tempPath ของเครื่อง
def storeFile(filePath):
    picFile = open(filePath, 'wb')
    print("Opened the file.")
    pic = conn.recv(1024)
    while pic:
        print("Receiving picture still.")
        picFile.write(pic)
        pic = conn.recv(1024)
    picFile.close()

def dataTransfer(conn):
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        data = conn.recv(1024) # receive the data
        data = data.decode('utf-8')
        
        
        # Split the data such that you separate the command
        # from the rest of the data.
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        
        
        tempFile = 'temp2/'  ### temp folder

                    
        ### รับคำสั่งจาก client ให้ store file โดย dataMessage[1] = ชื่อไฟล์รูป
        if command == 'STORE':
            print("Store command received. Time to save a picture")
            print(dataMessage[1])
            #t = datetime().strftime('%Y-%m-%d_%H:%M:%S')
            filePath = tempFile + dataMessage[1]
            print(filePath)
            storeFile(filePath)
            print("FINISHED STORING FILE")
            break
        

        # Send the reply back to the client
        conn.sendall(str.encode(reply))
        print("Data has been sent!")
    conn.close()
        

s = setupServer()

while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        break
