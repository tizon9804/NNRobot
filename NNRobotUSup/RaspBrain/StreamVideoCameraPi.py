import io
import socket
import struct
import time
import picamera
while(True):
    # Connect a client socket to my_server:8000 (change my_server to the
    # hostname of your server) 190.158.131.76
    try:
        client_socket = socket.socket()
        client_socket.connect(('190.158.131.76', 8000))

        # Make a file-like object out of the connection
        connection = client_socket.makefile('wb')
        try:
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
                # camera.start_preview()
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
                    # Reset the stream for the next capture
                    stream.seek(0)
                    stream.truncate()
            # Write a length of zero to the stream to signal we're done
            connection.write(struct.pack('<L', 0))
        finally:
            connection.close()
            client_socket.close()
    except Exception as ex:
        print "trying..."
