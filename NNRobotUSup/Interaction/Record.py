import pyaudio
import wave
from sys import byteorder
from array import array
from struct import pack

class Record:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.THRESHOLD = 500
        self.RECORD_SECONDS = 5
        self.num_silent = 0
        self.num_noise = 0
        self.snd_started = False
        self.WAVE_OUTPUT_FILENAME = "voice.wav"
        self.audio = pyaudio.PyAudio()

    def record(self):
        # start Recording
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)
        print "recording..."
        frames = array('h')

        #for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
        while 1:
            snd_data = array('h', stream.read(self.CHUNK))
            if byteorder == 'big':
                snd_data.byteswap()
            frames.extend(snd_data)
            silent = self.is_silent(snd_data)
            print silent
            if silent and self.snd_started:
                self.num_silent += 1
            if not silent and self.snd_started:
                self.num_silent -= 1
                self.num_noise += 1
            elif not silent and not self.snd_started:
                self.snd_started = True
            if self.snd_started and self.num_silent > 100 and self.num_noise>100:
                print "stop"
                break
            if self.num_silent > 100 and self.num_noise < 20:
                self.num_noise = 0
                self.num_silent = 0
                frames = array('h')
                print 'reset #############################'

        print "finished recording"

        # stop Recording
        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        print "modifying wav"
        frames = self.normalize(frames)
        #frames = self.trim(frames)
        #frames = self.add_silence(frames,0.5)
        print "saving wav..."
        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(frames)
        waveFile.close()
        print "saved"

    def is_silent(self, snd_data):
        "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < self.THRESHOLD

    def trim(self,snd_data):
        "Trim the blank spots at the start and end"
        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i) > self.THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(self,snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        r = array('h', [0 for i in xrange(int(seconds * self.RATE))])
        r.extend(snd_data)
        r.extend([0 for i in xrange(int(seconds * self.RATE))])
        return r

    def normalize(self,snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i * times))
        return r