import subprocess
import json
import time
from vosk import Model, KaldiRecognizer


def vosk_speech_to_text(model_path, timeout):
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    
    process = subprocess.Popen(
        ["arecord", "-D", "plughw:CARD=B100,DEV=0", "-f", "S16_LE", "-r", "16000", "-c", "1", "-t", "raw"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print("Vosk is listening...")
    text_list = []
    last_talk_time = time.time()

    try:
        while True:
            print(last_talk_time)
            data = process.stdout.read(4096)
            if not data:
                break
            
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
        
                if text.strip():
                    print(f"User said: {text}")
                    text_list.append(text)
                    last_talk_time = time.time()
            
            if time.time() - last_talk_time > timeout:
                print(f"No speech for {timeout}s, stopping.")
                break

    finally:
        process.terminate()

    return " ".join(text_list)