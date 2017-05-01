import ftplib
import threading
import cv2
from socketIO_client import SocketIO, LoggingNamespace
from base64 import b64encode

class FtpSender:
    def __init__(self):
        self.connect()
        self.sending = False

    def connect(self):
        self.sock = SocketIO('104.198.238.71',80,LoggingNamespace)
        #self.sock = SocketIO('190.158.131.76', 3000, LoggingNamespace)
        self.isconnect = True
    def upload(self,img,name):
        if self.isconnect:
            if not self.sending:
                t = threading.Thread(target=self.uploadasync, args=(img, name))
                t.start()

        else:
            self.connect()

    def uploadasync(self,img,name):
        self.sending = True
        img = cv2.imencode('.jpeg', img)
        self.sock.emit(name, {'buffer': b64encode(img[1])})
        self.sending = False

























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
