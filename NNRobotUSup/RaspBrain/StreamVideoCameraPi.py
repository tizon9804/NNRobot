import io
import socket
import time
import picamera
from PIL import Image
import numpy
import struct
import cv2
import NNRobotUSup.Network.FtpSender as ftp

ftpSender = ftp.FtpSender()

while(True):
    # Connect a client socket to my_server:8000 (change my_server to the
    # hostname of your server) 190.158.131.76
    try:
        client_socket = socket.socket()
        client_socket.connect(('190.158.131.76', 8000))

        # Make a file-like object out of the connection
        connection = client_socket.makefile('wb')
        try:
            print "Transmiting video Streaming..."
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)
                camera.framerate = 30
                # dark
                # camera.framerate = Fraction(1, 6)
                # camera.framerate = Fraction(1, 6)
                # camera.shutter_speed = 6#000000
                # camera.exposure_mode = 'off'
                camera.iso = 800
                # camera.image_effect = 'emboss'
                camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2017 GSC'
                #camera.start_preview()
                time.sleep(2)

                # Note the start time and construct a stream to hold image data
                # temporarily (we could write it directly to connection but in this
                # case we want to find out the size of each capture first to keep
                # our protocol simple)


                #start = time.time()
                stream = io.BytesIO()
                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                    # Write the length of the capture to the stream and flush to
                    # ensure it actually gets sent
                    connection.write(struct.pack('<L', stream.tell()))
                    connection.flush()
                    # Rewind the stream and send the image data over the wire
                    stream.seek(0)
                    connection.write(stream.read())
                    # convert image into numpy array
                    #data = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
                    # turn the array into a cv2 image
                    #img = cv2.imdecode(data, 1)
                    #ftpSender.upload2(img,'image_stream')
                    #cv2.imshow("Frame", img)
                    #key = cv2.waitKey(1) & 0xFF
                    # Reset the stream for the next capture
                    stream.seek(0)
                    stream.truncate()
            # Write a length of zero to the stream to signal we're done
            connection.write(struct.pack('<L', 0))
        except Exception,ex:
            print str(ex)
        finally:
            connection.close()
            client_socket.close()
            print "fail ##########"
    except Exception as ex:
        print "trying..."
