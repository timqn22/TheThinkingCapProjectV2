from arduino.app_utils import App, Bridge
from gpt_prompter import gpt_prompter
from arduino.app_utils import *
from arduino.app_bricks.keyword_spotting import KeywordSpotting

def on_keyword_detected():
    """Callback function that handles a detected keyword."""
    Bridge.call("keyword_detected")

spotter = KeywordSpotting()
spotter.on_detect("hey_arduino", on_keyword_detected)

Bridge.provide("gpt_prompter", gpt_prompter)
App.run()