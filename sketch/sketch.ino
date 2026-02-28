#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino_RouterBridge.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);
String inputBuffer = "";

void setup() {
  Monitor.begin();
  Bridge.begin();
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    while (true) delay(100);
  }
  oled_showMessage("Ready!");
}

void loop() {
  while (Monitor.available()) {
    char ch = (char)Monitor.read();
    if (ch == '\n' || ch == '\r') {
      inputBuffer.trim();
      if (inputBuffer.length() > 0) {
        // send prompt to Python via Monitor
        Monitor.println(inputBuffer);
        oled_showMessage("Asking GPT...");
        String response;
        Bridge.call("gpt_prompter", inputBuffer).result(response);
        oled_showMessage(response);
      }
    } else {
      inputBuffer += ch;
    }
  }
  delay(10);
}