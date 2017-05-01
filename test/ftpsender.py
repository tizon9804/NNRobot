import ftplib
class FtpSender:
    def __init__(self):
        session = ftplib.FTP('104.198.238.71','gerencia','S-k-a-t-e9804')
        print session.pwd()
        session.cwd('/var/www/NNRobot/VaNN/public/stream')
        print session.pwd()
        session.set_pasv(False)
        self.session = session

    def upload(self,urlFile,name):
        try:
            file = open(urlFile,'rb')                  # file to send
            print "sending..."
            self.session.storbinary('STOR ' + name, file)     # send the file
            print "sended."
        except Exception,ex:
            file.close()                                    # close file and FTP
            self.session.quit()