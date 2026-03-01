from arduino.app_utils import App, Bridge
from arduino.app_utils import *
from gpt_prompter import gpt_prompter
import json
import time
import os
import subprocess
from vosk import Model, KaldiRecognizer

#Load voice to text model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "vosk-model-small-en-us-0.15")
TIMEOUT = 5
WAKE_WORD = "potato"

model = Model(MODEL_PATH)
process = subprocess.Popen(
    ["arecord", "-D", "plughw:CARD=B100,DEV=0", "-f", "S16_LE", "-r", "16000", "-c", "1", "-t", "raw"],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL
)
wake_recognizer = KaldiRecognizer(model, 16000)

print("Waiting for 'Hey Arduino'...")

def loop():
    data = process.stdout.read(4096)
   
    if not data:
        return
        
    if wake_recognizer.AcceptWaveform(data):
        result = json.loads(wake_recognizer.Result())
        text = result.get("text", "")
        
        if WAKE_WORD in text.lower():
            print("Wake word detected!")
            
            Bridge.call("show_listening")
            
            cmd_recognizer = KaldiRecognizer(model, 16000)
            text_list = []
            last_talk_time = time.time()
            
            while True:
                data = process.stdout.read(4096)
                
                if not data:
                    print("Error with data fater wake")
                    break
                    
                if cmd_recognizer.AcceptWaveform(data):
                    result = json.loads(cmd_recognizer.Result())
                    cmd_text = result.get("text", "")
                    print(cmd_text)
                    if cmd_text.strip():
                        text_list.append(cmd_text)
                        last_talk_time = time.time()
                        print(last_talk_time)
                print(time.time() - last_talk_time)        
                if time.time() - last_talk_time > TIMEOUT:
                    print("Timed out")
                    print(time.time())
                    print(last_talk_time)
                    break

            command = " ".join(text_list)
            print(command)
            if command.strip():
                Bridge.call("show_message", "Asking GPT...")
                response = gpt_prompter(command)
                print(response)
                response = response[:168]  # ~8 lines x 21 chars on OLED
                response = response.encode('ascii', errors='replace').decode('ascii')
                print(response)
                try:
                    Bridge.call("show_message", response, timeout=60)
                except Exception as e:
                    Bridge.call("show_message", "Something went wrong :(")
            else:
                Bridge.call("show_message", "Didn't catch that.")
        

            print("Waiting for 'Hey Arduino'...")

App.run(user_loop=loop)