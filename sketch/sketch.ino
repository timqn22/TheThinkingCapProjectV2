#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino_RouterBridge.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
  Bridge.begin();
  Bridge.provide("show_listening", show_listening);
  Bridge.provide("show_message", show_message);
  
  Monitor.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    while (true) delay(100);
  }

  oled_showCentered("Say 'Hey Arduino'");
}

void loop() {}

void show_listening() {
  oled_showMessage("Listening...");
}

void show_message(String msg) {
  oled_showMessage(msg);
}