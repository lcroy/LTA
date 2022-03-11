import speech_recognition as sr
import boto3
import playsound
import time
# from pygame import *
from configure import Config
from time import strftime
import azure.cognitiveservices.speech as speechsdk
import subprocess

cfg = Config()

## Google service to recognize the voice and transfer to text
def speech_to_text():
    # Set American English
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=cfg.sample_rate, chunk_size=cfg.chunk_size, device_index=0) as source:
        # Adjusts the energy threshold dynamically using audio from source (an AudioSource instance) to account for ambient noise.
        print("Please wait one second for calibrating microphone...")
        r.pause_threshold = 0.8
        r.dynamic_energy_threshold = True
        r.adjust_for_ambient_noise(source, duration=1)
        print("Ok, microphone is ready...")
        # p = vlc.MediaPlayer(self.hint_sound)
        # p.play()
        playsound.playsound(cfg.hint_sound, True)
        audio = r.listen(source, timeout=None)
        # with open(os.getcwd()+ '\sound_classification\speakervoice\speaker.wav','wb') as f:
        #     f.write(audio.get_wav_data())
        voice_to_text = ""
        try:
            voice_to_text = r.recognize_google(audio, language="en-US")
            print('You: ' + voice_to_text)
        except:
            print('BotX: I did not hear anything....')

    return voice_to_text.lower()


def generate_botx_res_mp3(cfg, text):
    poly = boto3.client('polly')
    response = poly.synthesize_speech(OutputFormat='mp3', Text=text, VoiceId='Matthew')
    body = response['AudioStream'].read()
    now = strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    file_name = cfg.voice_path + now + r"speakervoice.mp3"
    try:
        f = open(file_name, "wb+")
        f.write(body)
    except IOError:
        print("Sorry, I can not create the voice file")
    else:
        f.close()

    return file_name


## Amazon text to speech in normal case
def text_to_speech(cfg, text):
    print('BotX: ' + text)
    # generate the response mp3
    mp3_file_path = generate_botx_res_mp3(cfg, text)
    playsound.playsound(mp3_file_path)
    # p = vlc.MediaPlayer(mp3_file_path)
    # p.play()

def text_to_speech_microsoft(cfg, text):
    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    speech_key, service_region = "", ""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    print("Max: " + text)
    p_typing_audio = subprocess.Popen(["python", cfg.typing_audio])
    result = speech_synthesizer.speak_text(text)
    p_typing_audio.terminate()


def speech_to_text_microsoft():
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_config = speechsdk.SpeechConfig(subscription="", region="")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    result = ''

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        nonlocal result
        result = evt.result.text
        # Stop continuous speech recognition
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True
        print("User: " + result)

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognized.connect(lambda evt: stop_cb(evt) if evt.result.text != "" else print("Max: I did not hear anything..."))

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.1)

    return result.lower()
