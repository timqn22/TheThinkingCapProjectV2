#include "libraries/DFRobotDFPlayerMini/DFRobotDFPlayerMini.h"

DFRobotDFPlayerMini myDFPlayer;

void setupAudio(int volume) {
  Serial1.begin(9600); //make sure to use pins 0(rx) and 1(tx)

  if (!myDFPlayer.begin(Serial1)) {
    // If it fails to initialize, print an error and halt
    Monitor.println("DFPlayer Error: Check connection/SD Card");
    while(true);
  }
  
  myDFPlayer.volume(volume); 
  Monitor.println("Audio System Online.");
}

void play(int fileIndex) {
  myDFPlayer.play(fileIndex);
}