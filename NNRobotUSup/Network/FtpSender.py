import ftplib
import threading
import cv2
from socketIO_client import SocketIO, LoggingNamespace
from base64 import b64encode
import socket

class FtpSender:
    def __init__(self):
        self.connect()
        self.sending = 60

    def connect(self):
        self.sock = SocketIO('104.198.238.71',80,LoggingNamespace)
        #self.sock = SocketIO('190.158.131.76', 3000, LoggingNamespace)
        #self.sockUdp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #self.UDP_IP = '104.198.238.71'
        #self.UDP_PORT = 5000
        self.isconnect = True

    def upload(self,img,name):
        if self.isconnect:
            self.sending += 1
            if self.sending > 50:
                self.sending = 0
                t = threading.Thread(target=self.uploadasync, args=(img, name))
                t.start()
        else:
            self.connect()



    def uploadasync(self,img,name):
        img = cv2.imencode('.jpeg', img)
        self.sock.emit(name, {'buffer': b64encode(img[1])})



    def uploadasyncUDP(self, img, name):
        img = cv2.imencode('.jpeg', img)
        self.sockUdp.sendto(b64encode(img[1]), (self.UDP_IP, self.UDP_PORT))


























    def codigonousadoperosirbeFTP(self):
        session = ftplib.FTP('104.198.238.71', 'gerencia', 'S-k-a-t-e9804')
        print session.pwd()
        session.cwd('/var/www/NNRobot/VaNN/public/stream')
        print session.pwd()
        session.set_pasv(False)
        self.session = session
        self.isconnect = True
        if self.isconnect:
            threading._sleep(2)
            t= threading.Thread(target=self.uploadasync,args=(urlFile,name))
            t.start()
        else:
            self.connect()
        try:
            file = open(urlFile,'rb')                  # file to send
            #print "sending...",file
            self.session.storbinary('STOR ' + name,file)     # send the file
            #print "sended."
        except Exception,ex:
            self.isconnect=False
            print "Error ftp",str(ex)                                       # close file and FTP
