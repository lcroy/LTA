import time as ti

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from pygame import *
import pygame

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "f6bd8f851e48430ea0ea46bb47fad10a", "northeurope"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
audio_config = AudioOutputConfig(filename=r"C:\Users\lcroy\PycharmProjects\MaxClient\voice_audio\audio.mp3")
speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
synthesizer.speak_text_async("Today we have two exciting updates to share: our latest product, and our latest funding round!")
#
#
# # user-friendly music starts...
# pygame.init()
# pygame.mixer.init()
# sounda = pygame.mixer.Sound(r"C:\Users\lcroy\PycharmProjects\MaxClient\voice_audio\audio.wav")
#
# sounda.play()
# ti.sleep(20)
#
#
# # Creates a speech synthesizer using the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
# #
# # # Receives a text from console input.
# # # print("Type some text that you want to speak...")
# # # text = input()
# #
# # text = "Today we have two exciting updates to share: our latest product, and our latest funding round!"
# #
# # # Synthesizes the received text to speech.
# # # The synthesized speech is expected to be heard on the speaker with this line executed.
result = speech_synthesizer.speak_text_async(text).get()
# #
# # result = speech_synthesizer.speak_text_async("Customizing audio output format.").get()
# # stream = AudioDataStream(result)
# # stream.save_to_wav_file(r"C:\Users\lcroy\PycharmProjects\MaxClient\voice_audio\audio.wav")
#
#
# # # Checks result.
# # if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
# #     print("Speech synthesized to speaker for text [{}]".format(text))
# # elif result.reason == speechsdk.ResultReason.Canceled:
# #     cancellation_details = result.cancellation_details
# #     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
# #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
# #         if cancellation_details.error_details:
# #             print("Error details: {}".format(cancellation_details.error_details))
# #     print("Did you update the subscription info?")
# # </code>
import wave

import pygame.mixer
from time import sleep

file_path = r"C:\Users\lcroy\PycharmProjects\MaxClient\voice_audio\audio.wav"

file_wav = wave.open(file_path)
frequency = file_wav.getframerate()
pygame.mixer.init(frequency=frequency)
pygame.mixer.music.load(file_path)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    sleep(1)