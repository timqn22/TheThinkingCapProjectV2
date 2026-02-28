from arduino.app_utils import App, Bridge
from gpt_prompter import gpt_prompter

def loop():
    pass

Bridge.provide("gpt_prompter", gpt_prompter)
App.run(user_loop=loop)