import io
import socket
import struct
import cv2
import numpy as np

class VideStream:
    def __init__(self,bparm):
        # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
        # all interfaces)
        self.bparm = bparm
        self.isVideoActive = False

    def acceptVideo(self):
        print "open sockets port 8000"
        self.isVideoActive = False
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8000))
        print "listening"
        self.server_socket.listen(0)
        print  "Accept a single connection and make a file-like object out of it"
        self.connection = self.server_socket.accept()[0].makefile('rb')
        img = self.getImage()
        return img

    def getImage(self):
        try:
            connection = self.connection
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # convert image into numpy array
            data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
            # turn the array into a cv2 image
            img = cv2.imdecode(data, 1)
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            self.isVideoActive= True
            return img
        except Exception as ex:
            print "Network: finalizo streaming: " + str(ex)
            self.isVideoActive = False
            self.bparm.logicLife = False
            self.bparm.exploreLife =False
            self.bparm.senseLife = False
            connection.close()
            self.server_socket.close()
