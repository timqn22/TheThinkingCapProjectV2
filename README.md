The Thinking Cap Project is a wearable AI assistant that listens for a wake word, processes voice commands, and provides intelligent responses. It integrates local speech-to-text with the powerful capabilities of OpenAI's GPT models, including visual analysis through a connected camera. Responses are displayed on a compact OLED screen, making it a truly hands-free AI companion.

## How It Works

The system operates through the Arduino Uno Q, bridging a Linux MPU with a STM32 MCU. The MPU handles the voice to text and API calls, while the MCU operates the OLED display.

1.  **Wake Word Detection**: The main Python script (`main.py`) continuously listens for the wake word "jarvis" using the `vosk` offline speech recognition engine. This ensures privacy and low-latency activation.

2.  **Voice Command Capture**: Upon detecting the wake word, the device begins recording the user's speech. It transcribes the audio into text in real-time. The recording stops after a period of silence.

3.  **AI Processing**: The transcribed text is sent to the `gpt_prompter.py` script. This script interacts with the OpenAI API. It uses a tool-calling feature that allows the AI model to decide if it needs to see its surroundings to answer a query.

4.  **Visual Analysis**: If the user asks a question about their environment (e.g., "What do you see?"), the AI can trigger the `take_snapshot` function. The system captures an image from the camera, which is then sent along with the original prompt to the GPT-4V model for analysis.

5.  **Displaying the Response**: The final text response from the AI is sent to the Arduino via the `Arduino_RouterBridge`. The Arduino sketch then displays the message on the OLED screen, with automatic scrolling for longer responses.

## Key Components

### Hardware
*   An Arduino Uno Q
*   A 128x64 OLED Display (driven by the SSD1306 chipset)
*   A usb webcam/microphone

### Software
*   **Python**:
    *   `vosk`: For offline, on-device wake word detection and speech-to-text.
    *   `openai`: For interacting with GPT-4V.
    *   `opencv-python`: For capturing images from the camera.
    *   `Arduino_RouterBridge`: For communication between the Python script and the Arduino.
*   **Arduino (C++)**:
    *   `Adafruit_SSD1306` & `Adafruit_GFX`: For controlling the OLED display.
    *   `Arduino_RouterBridge`: To receive messages from the Python backend.

## Setup and Installation

### 1. Hardware Setup
1.  Connect the OLED display to the I2C pins of your microcontroller.
2.  Connect the microphone and camera to the host computer running the Python script.
3.  Upload the Arduino sketch to your microcontroller.

### 2. Arduino Sketch
1.  Open the `sketch/sketch.ino` file in the Arduino IDE.
2.  Install the required libraries listed in `sketch/sketch.yaml`, including:
    *   `Adafruit GFX Library`
    *   `Adafruit SSD1306`
    *   `Arduino_RouterBridge`
3.  Upload the sketch to your board.

### 3. Python Backend
1.  Clone this repository:
    ```bash
    git clone https://github.com/timqn22/TheThinkingCapProjectV2.git
    cd TheThinkingCapProjectV2/python
    ```
2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3.  Create a `.env` file in the `python/` directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY='your_openai_api_key_here'
    ```
4.  The required Vosk model is already included in the `python/models/` directory.
5.  You may need to update the audio device in `python/main.py` from `"plughw:CARD=B100,DEV=0"` to match your system's microphone configuration. You can list your devices using `arecord -l`.

## Usage
1.  Run the main Python script:
    ```bash
    python python/main.py
    ```
2.  The script will initialize, and the console will display `Waiting for 'Hey Jarvis'...`. The OLED screen will show "Say 'Hey Jarvis'".
3.  Activate the assistant by saying "jarvis".
4.  The OLED will update to "Listening...". State your question or command.
5.  After you finish speaking, the script will process your request and the OLED will show "Asking GPT...".
6.  The AI's response will then be displayed on the OLED screen.

## File Structure
```
.
├── python/
│   ├── main.py             # Main application entry point, handles wake word and STT
│   ├── gpt_prompter.py     # Manages interaction with OpenAI API & camera
│   ├── requirements.txt    # Python dependencies
│   └── models/             # Contains the Vosk speech recognition model
│
└── sketch/
    ├── sketch.ino          # Main Arduino sketch for device-side logic
    ├── oled.ino            # Helper functions for OLED display control
    └── sketch.yaml         # Arduino project configuration and libraries
