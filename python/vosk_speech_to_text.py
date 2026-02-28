import pyaudio
import time
from vosk import Model, KaldiRecognizer
import os
import json

def vosk_speech_to_text(model_path, timeout):
    if not os.path.exists(model_path):
        print(f"Error: model path '{model_path}' doesn't exist")
        exit()

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    last_talk_time = time.time()
    text_list = []

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8192)
    stream.start_stream()

    print("Vosk is listening...")

    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result["text"]
                if text.strip():
                    print(f"User said: {text}")
                    text_list.append(text)
                    last_talk_time = time.time()
            
            if time.time() - last_talk_time > timeout:
                print(f"No speech detected for {timeout} seconds")
                print("Vosk is stopping...")
                break

    except KeyboardInterrupt:
        print("Force stop with keyboard interruption")
        
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    return " ".join(text_list)