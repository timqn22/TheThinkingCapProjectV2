String sanitizeForOLED(String msg) {
  String clean = "";
  for (int i = 0; i < msg.length(); i++) {
    char c = msg[i];
    if (c == '\xe2' && i + 2 < msg.length()) {
      unsigned char b1 = msg[i + 1];
      unsigned char b2 = msg[i + 2];
      if (b1 == 0x80 && b2 == 0x99) { clean += '\''; i += 2; }
      else if (b1 == 0x80 && b2 == 0x98) { clean += '\''; i += 2; }
      else if (b1 == 0x80 && b2 == 0x9C) { clean += '"'; i += 2; }
      else if (b1 == 0x80 && b2 == 0x9D) { clean += '"'; i += 2; }
      else if (b1 == 0x80 && b2 == 0x93) { clean += '-'; i += 2; }
      else if (b1 == 0x80 && b2 == 0x94) { clean += '-'; i += 2; }
      else if (b1 == 0x80 && b2 == 0xA6) { clean += "..."; i += 2; }
      else { clean += '?'; i += 2; }
    } else if (c >= 32 && c <= 126) {
      clean += c;
    } else if (c == '\n') {
      clean += c;
    } else {
      clean += '?';
    }
  }
  return clean;
}

int countLines(String msg, int charsPerLine) {
  int totalLines = 1;
  int col = 0;
  for (int i = 0; i < msg.length(); i++) {
    if (msg[i] == '\n') {
      totalLines++;
      col = 0;
    } else {
      col++;
      if (col >= charsPerLine) {
        totalLines++;
        col = 0;
      }
    }
  }
  return totalLines;
}

int findScrollStart(String msg, int charsPerLine, int scrollLine) {
  int currentLine = 0;
  int col = 0;
  int startIdx = 0;
  for (int i = 0; i < msg.length() && currentLine < scrollLine; i++) {
    if (msg[i] == '\n') {
      currentLine++;
      col = 0;
    } else {
      col++;
      if (col >= charsPerLine) {
        currentLine++;
        col = 0;
      }
    }
    startIdx = i + 1;
  }
  return startIdx;
}

void printVisibleLines(String msg, int startIdx, int charsPerLine, int maxLines) {
  int printed = 0;
  int col = 0;
  for (int i = startIdx; i < msg.length() && printed < maxLines; i++) {
    display.print(msg[i]);
    if (msg[i] == '\n') {
      printed++;
      col = 0;
    } else {
      col++;
      if (col >= charsPerLine) {
        printed++;
        col = 0;
      }
    }
  }
}

void scrollText(String msg, int charsPerLine, int lineHeight, int maxLines, int totalLines) {
  bool firstPrint = true;
  
  for (int scroll = 0; scroll <= totalLines - maxLines; scroll++) {
    display.clearDisplay();
    display.setCursor(0, 0);
    
    int startIdx = findScrollStart(msg, charsPerLine, scroll);
    printVisibleLines(msg, startIdx, charsPerLine, maxLines);
    display.display();
    
    if (firstPrint){
      delay(10000);
      firstPrint = false;
    }
      
    delay(5000);
  }
  
  delay(10000);
}

void oled_showMessage(String msg) {
  msg = sanitizeForOLED(msg);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setTextWrap(true);

  int lineHeight = 8;
  int charsPerLine = 21;
  int maxLines = 64 / lineHeight;
  int totalLines = countLines(msg, charsPerLine);

  if (totalLines <= maxLines) {
    display.setCursor(0, 0);
    display.print(msg);
    display.display();
  } 
  else {
    scrollText(msg, charsPerLine, lineHeight, maxLines, totalLines);
  }
}

void oled_showCentered(String msg) {
  msg = sanitizeForOLED(msg);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setTextWrap(true);

  int lineHeight = 8;
  int charsPerLine = 21;
  int maxLines = 64 / lineHeight;
  int totalLines = countLines(msg, charsPerLine);

  if (totalLines <= maxLines) {
    int y = (64 - totalLines * lineHeight) / 2;
    display.setCursor(0, y);
    display.print(msg);
    display.display();
  } 
  else {
    scrollText(msg, charsPerLine, lineHeight, maxLines, totalLines);
  }
}

void oled_clear() {
  display.clearDisplay();
  display.display();
}