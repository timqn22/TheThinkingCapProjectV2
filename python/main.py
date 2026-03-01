from arduino.app_utils import App, Bridge
from arduino.app_utils import *
from gpt_prompter import gpt_prompter
import json
import time
import os
import subprocess
from vosk import Model, KaldiRecognizer


# Declare constant variables
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "vosk-model-small-en-us-0.15")
TIMEOUT = 5
WAKE_WORD = "jarvis"


# Load voice to text model
model = Model(MODEL_PATH)
process = subprocess.Popen(
    ["arecord", "-D", "plughw:CARD=B100,DEV=0", "-f", "S16_LE", "-r", "16000", "-c", "1", "-t", "raw"],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL
)
wake_recognizer = KaldiRecognizer(model, 16000)


print("Waiting for 'Hey Jarvis'...")


# Main Loop
def loop():
    data = process.stdout.read(4096)
   
    if not data:
        return

    # Check for trigger phrase
    if wake_recognizer.AcceptWaveform(data):
        result = json.loads(wake_recognizer.Result())
        text = result.get("text", "")
        
        if WAKE_WORD in text.lower():
            print("Wake word detected!")
            
            Bridge.call("show_listening")
            
            cmd_recognizer = KaldiRecognizer(model, 16000)
            text_list = []
            last_talk_time = time.time()

            # Check for user query
            while True:
                data = process.stdout.read(4096)
                
                if not data:
                    break
                    
                if cmd_recognizer.AcceptWaveform(data):
                    result = json.loads(cmd_recognizer.Result())
                    cmd_text = result.get("text", "")
                    print(f"Recorded response: {cmd_text}")
                    
                    if cmd_text.strip():
                        text_list.append(cmd_text)
                        last_talk_time = time.time()-3
                     
                if time.time() - last_talk_time > TIMEOUT:
                    print("Timed out")
                    break

            command = " ".join(text_list)
            
            if command.strip():
                Bridge.call("show_message", "Asking GPT...")
                
                response = gpt_prompter(command) # Send prompt to openai api script
                response = response.encode("ascii", "ignore").decode("ascii")
                print(response)
                
                try:
                    Bridge.call("show_message", response, timeout=60)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                Bridge.call("show_message", "Didn't catch that.")
        

            print("Waiting for 'Hey Jarvis'...")


App.run(user_loop=loop)