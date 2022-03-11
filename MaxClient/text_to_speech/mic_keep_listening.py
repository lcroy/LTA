import speech_recognition as sr


def speech_to_text_google():
    # Set American English
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=48000, chunk_size=2048, device_index=0) as source:
        # Adjusts the energy threshold dynamically using audio from source (an AudioSource instance) to account for ambient noise.
        print("Please wait one second for calibrating microphone...")
        r.pause_threshold = 0.8
        r.dynamic_energy_threshold = True
        r.adjust_for_ambient_noise(source, duration=1)
        print("Ok, microphone is ready...")
        # p = vlc.MediaPlayer(self.hint_sound)
        # p.play()
        audio = r.listen(source, timeout=None)
        transcript = ""
        try:
            transcript = r.recognize_google(audio, language="en-US")
            print('You: ' + transcript)
        except:
            print('Max: I did not hear anything....')

    return transcript.lower()


while True:
    result = speech_to_text_google()

    print(result)