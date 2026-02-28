void oled_showMessage(String msg) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.setTextWrap(true);
  display.print(msg);
  display.display();
}

void oled_showCentered(String msg) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setTextWrap(true);

  // Center vertically (approx)
  int lineHeight = 8;
  int lines = 1;
  for (char c : msg) if (c == '\n') lines++;
  int y = (64 - lines * lineHeight) / 2;

  display.setCursor(0, y);
  display.print(msg);
  display.display();
}

void oled_clear() {
  display.clearDisplay();
  display.display();
}