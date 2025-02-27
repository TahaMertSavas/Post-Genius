#--------------------------------------------(Library and Module)-------------------------------------------------------
from elevenlabs.client import ElevenLabs
from elevenlabs import play,save
import os
import base64
#-----------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------(API KEY)-----------------------------------------------------------
api_key1 = "ELEVENLABS API KEYINIZI GIRINIZ<->ENTER YOUR API KEY"
client = ElevenLabs(api_key= api_key1)
#-----------------------------------------------------------------------------------------------------------------------


#------------------------------------------------(CLASSES)--------------------------------------------------------------
class ELEVENLABS_CLASS(object):
    def __init__(self,voice_id,model_id,output_format):
        self.voice_id = voice_id
        self.model_id = model_id
        self.output_format = output_format
    def dubbing(self,audio_text):
        audio = client.text_to_speech.convert(
            text=audio_text,
            voice_id=self.voice_id,
            model_id=self.model_id,
            output_format=self.output_format,
        )
        return audio
#-----------------------------------------------------------------------------------------------------------------------


#--------------------------------------(ElevenLabs Voice ID List)-------------------------------------------------------
Aria = "9BWtsMINqrJLrRacOk9x"
Roger = "CwhRBWXzGAHq8TQ4Fs17"
Sarah = "EXAVITQu4vr4xnSDxMaL"
Laura = "FGY2WhTYpPnrIDTdsKH5"
Charlie = "IKne3meq5aSn9XLyUdCD"
George = "JBFqnCBsd6RMkjVDRZzb"
Callum = "N2lVS1w4EtoT3dr4eOWO"
River = "SAz9YHcvj6GT2YYXdXww"
Liam = "SAz9YHcvj6GT2YYXdXww"
Charlotte = "XB0fDUnXU5powFXDhCwa"
Alice = "XB0fDUnXU5powFXDhCwa"
Matilda = "XrExE9yKIg1WjnnlVkGX"
Will = "bIHbv24MWmeRgasZH58o"
Jessica = "cgSgspJ2msm6clMCkdW9"
Eric = "cjVigY5qzO86Huf0OWal"
Chris = "iP95p4xoKVk53GoZ742B"
Brian = "nPczCjzI2devNBz1zQrb"
Daniel = "onwK4e9ZLuTAKqWW03F9"
Lily = "pFZP5JQG7iQjIQuC4Bku"
Bill = "pqHfZKP75CvOlQylNhV4"
Doga = "IuRRIAcbQK5AQk1XevPj"
#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------(FUNCTIONS)-------------------------------------------------------------
def run(audio_text):
    narrator = ELEVENLABS_CLASS(Roger,"eleven_multilingual_v2","mp3_44100_128")
    audio_generator  = narrator.dubbing(audio_text)
    audio_data = b"".join(audio_generator)
    audio_b64 = base64.b64encode(audio_data).decode("utf-8")
    return audio_b64
#-----------------------------------------------------------------------------------------------------------------------

