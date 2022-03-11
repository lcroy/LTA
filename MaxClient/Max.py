import speech_recognition as sr
import random
import boto3
import playsound
import pyttsx3
import azure.cognitiveservices.speech as speechsdk
import time
import requests
import pygame
import subprocess

# from pygame import *
# import vlc
from configure import Config
# from robot_control_agent.robot_service_execution.mir.control_MiR import call_mir
# from main.webot.control_Franka import call_franka
from update_conversation import *
from robot_control_agent.call_other_service import call_other_service
from robot_control_agent.robot_service_execution.mir.control_MiR import call_mir

class Max:

    def __init__(self, cfg):
        self.sample_rate = cfg.sample_rate
        self.chunk_size = cfg.chunk_size
        self.hint_sound = cfg.hint_sound
        self.voice = cfg.voice_id
        self.converter = pyttsx3.init()
        self.converter.setProperty('rate', 150)
        self.converter.setProperty('volume', 0.7)
        self.host = cfg.max_server_host
        self.headers = {'Content-Type': 'application/json', 'Accept-Language': 'en_US'}

    # Google service to recognize the speech
    def speech_to_text_google(self):
        # Set American English
        r = sr.Recognizer()
        with sr.Microphone(sample_rate=self.sample_rate, chunk_size=self.chunk_size, device_index=0) as source:
            # Adjusts the energy threshold dynamically using audio from source (an AudioSource instance) to account for ambient noise.
            print("Please wait one second for calibrating microphone...")
            r.pause_threshold = 0.8
            r.dynamic_energy_threshold = True
            r.adjust_for_ambient_noise(source, duration=1)
            print("Ok, microphone is ready...")
            # p = vlc.MediaPlayer(self.hint_sound)
            # p.play()
            playsound.playsound(self.hint_sound, True)
            audio = r.listen(source, timeout = None)
            transcript = ""
            try:
                transcript = r.recognize_google(audio, language="en-US")
                print('You: ' + transcript)
            except:
                print('Max: I did not hear anything....')

        return transcript.lower()

    # Microsoft service to recognize speech
    def speech_to_text_microsoft(self):
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

    # Text to Speech - generate audio file
    def generate_botx_res_mp3(self, cfg, text):
        poly = boto3.client('polly')
        response = poly.synthesize_speech(OutputFormat='mp3', Text=text, VoiceId=self.voice)
        body = response['AudioStream'].read()
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        file_name = cfg.voice_path + now + r"speakervoice.mp3"
        try:
            f = open(file_name, "wb+")
            f.write(body)
        except IOError:
            print("Sorry, I can not create the audio file")
        else:
            f.close()

        return file_name

    # Text to Speech - Amazon Polly service
    def text_to_speech(self, cfg, text):
        print('Max: ' + text)
        # generate the response mp3
        mp3_file_path = self.generate_botx_res_mp3(cfg, text)
        playsound.playsound(mp3_file_path)
        # p = vlc.MediaPlayer(mp3_file_path)
        # p.play()

    def text_to_speech_local(self, text):
        print('BotX: ' + text)
        self.converter.say(text)
        self.converter.runAndWait()

    def text_to_speech_microsoft(self, cfg, text):
        # Creates an instance of a speech config with specified subscription key and service region.
        # Replace with your own subscription key and service region (e.g., "westus").
        speech_key, service_region = "", "northeurope"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"

        # Creates a speech synthesizer using the default speaker as audio output.
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        print("Max: " + text)
        p_typing_audio = subprocess.Popen(["python", cfg.typing_audio_script])
        result = speech_synthesizer.speak_text(text)
        p_typing_audio.terminate()


    # with attention
    # def text_to_speech_attention(self, cfg, text, type):
    #     print('BotX: ' + text)
    #     # generate the response mp3
    #     mp3_file_path = self.generate_botx_res_mp3(cfg, text)
    #     if type == 'no_attention':
    #         playsound.playsound(mp3_file_path)
    #         # p = vlc.MediaPlayer(mp3_file_path)
    #         # p.play()
    #     else:
    #         pause_flag = 0
    #         mixer.init()
    #         mixer.music.load(mp3_file_path)
    #         mixer.music.play()
    #         # check if BotX is still talking
    #         while pygame.mixer.music.get_busy():
    #             # read the head position from json file
    #             with portalocker.Lock(cfg.HPR_json_path, 'r', timeout=5) as fh:
    #                 data = json.load(fh)
    #                 fh.flush()
    #             # if the speaker is not focus on the camera, then it stop talking
    #             if ((data['x'] >= 15) or (data['x'] <= -15) or (data['y'] >= 15) or (
    #                     data['y'] <= -15) or (
    #                     data['z'] >= 15) or (data['z'] <= -15)):
    #                 mixer.music.pause()
    #                 # if pause_flag == 0:
    #                 #     playsound.playsound(cfg.voice_attention_path, True)
    #                 pause_flag = 1
    #             # if the speaker's attention is back, then it continues talking
    #             else:
    #                 if pause_flag == 1:
    #                     mixer.music.unpause()
    #                     pause_flag = 0
    #         mixer.music.stop()


    # Call botx service
    def get_response(self, text, requested_service, client_slot_result):
        parameters = {'message':text, 'requested_service': requested_service, 'client_slot_result':client_slot_result}
        result = requests.get(self.host + 'get_service/', params=parameters, headers=self.headers)

        return result.json()

    def get_file(self):
        result = requests.get(self.host + 'download', headers=self.headers)

        return result.json()

    def call_max(self, cfg):
        # new a configure file
        cfg = Config()
        update_user(cfg, "...")
        update_service(cfg, "home")
        update_max(cfg, "Waiting operator's command...")
        #read response template from json file
        with open(cfg.response_template) as json_file:
            response_template = json.load(json_file)
        while True:
            # 1. check the trigger word
            print("You may talk to Max now...")
            text = self.speech_to_text_microsoft().casefold()
            # if it detects speech...
            if len(text) > 0:
                update_user(cfg, text)
            # if system detects the trigger word - Max
            if any(key in text.casefold() for key in cfg.trigger_word_max):
                text = text.replace("Macs", "Max")
                text = random.choice(response_template['init_speak'])
                update_max(cfg, text)
                self.text_to_speech_microsoft(cfg, text)
                while True:
                    # 2. wait for human command
                    text = self.speech_to_text_microsoft().casefold()
                    # BotX does heard something not some random noise
                    if len(text) > 0:
                        # call mir service
                        if any(key in text.casefold() for key in cfg.trigger_word_mir):
                            text = text.replace(str(["mia","Mia"]), "MiR")
                            update_user(cfg, text)
                            update_mir(cfg, "Unknow...", "Unknow...", "Waiting...")
                            call_mir(self, cfg, 'mir', response_template)
                            continue

                        # call franka service
                        if any(key in text.casefold() for key in cfg.trigger_word_franka):
                            text = text.replace(str(["franka", "franca", "frankia", "frank"]), "Franka")
                            update_user(cfg, text)
                            update_franka(cfg, "Unknow...", "Unknow...", "Waiting...")
                            # call_franka(self.cfg)
                            continue

                        # call swarm service
                        if any(key in text.casefold() for key in cfg.trigger_word_swarm):
                            update_user(cfg, text)
                            update_swarm(cfg, "Unknow...", "Unknow...", "Waiting...")
                            # call_swarm(self.cfg)
                            continue

                        # call other service (remember if you are asking other service not registered in Max client,
                        # then it will ask you to confirm and checking the server side)
                        update_user(cfg, text)
                        call_other_service(self, cfg, text, response_template)
                        continue



