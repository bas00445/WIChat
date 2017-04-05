import threading
import socket
import time


class ClientSocket(threading.Thread):
    def __init__(self, ip, port, name="Name", **kwargs):
        threading.Thread.__init__(self)
        self.tLock = threading.Lock()
        self.shutdown = False

        self.clientName = name
        self.clientMessage = ""

        self.ip = ip
        self.port = port
        self.targetServer = (ip, port)

    def connect(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(self.targetServer)
        self.soc.setblocking(0)

    def setText(self, message):
        self.clientMessage = message


    def run(self):
        while self.clientMessage != "q":
            string = self.clientName + ": " + self.clientMessage
            if self.clientMessage != "":
                self.soc.sendto(string.encode("utf-8"), self.targetServer)
            self.tLock.acquire()
            self.tLock.release()
            self.clientMessage = ""
            time.sleep(0.2)

    def close(self):
        self.shutdown = True
        self.recvThread.join()
        self.soc.close()
