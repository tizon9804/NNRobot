from watson_developer_cloud import TextToSpeechV1
import json
from os.path import join, dirname

class TextToSpeak:

    def __init__(self):
        self.text_to_speech = TextToSpeechV1(
            username='73733765-1757-4708-84a0-16080cd5e68b',
            password='xskqh32nKuUf',
            x_watson_learning_opt_out=True)  # Optional flag
        print "converter text speak initialize"

    def generateSpeak(self,text):
        print(json.dumps(self.text_to_speech.voices(), indent=2))
        output = './output_resp.wav'
        with open(join(dirname(__file__), output),
                  'wb') as audio_file:
            audio_file.write(
                self.text_to_speech.synthesize(text, accept='audio/wav',
                                          voice="es-LA_SofiaVoice"))
        print(
            json.dumps(self.text_to_speech.pronunciation(
                'Watson', pronunciation_format='spr'), indent=2))
        return output
