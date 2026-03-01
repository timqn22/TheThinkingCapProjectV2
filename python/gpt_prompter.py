import os
import base64
import cv2
from openai import OpenAI
from dotenv import load_dotenv
from arduino.app_utils import Bridge
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SNAPSHOT_PATH = "/tmp/snapshot.jpg"

def capture_snapshot():
    camera = cv2.VideoCapture(2)

    ret, frame = camera.read()
    camera.release()
    if ret:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite(SNAPSHOT_PATH, frame)
        return SNAPSHOT_PATH
    return None

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

tools = [
    {
        "type": "function",
        "name": "take_snapshot",
        "description": "Takes a photo using the camera and analyzes it. Use this when the user asks about something visual, asks what you can see, references the camera, or asks about their surroundings/environment.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "type": "function",
        "name": "get_distance",
        "description": "Gets the distance to the nearest object in front of the user in feet using an ultrasonic sensor. Use this when the user asks how far something is, asks about distance, or asks what's in front of the sensor.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

def gpt_prompter(prompt: str):
    messages = [{"role": "user", "content": prompt}]

    # First call — let GPT decide if it needs the camera
    response = client.responses.create(
        model="gpt-5.2",
        instructions="Keep your response within 100 words",
        tools=tools,
        input=messages
    )

    # Check if GPT wants to take a snapshot
    tool_call = next((item for item in response.output if item.type == "function_call"), None)

    if tool_call and tool_call.name == "take_snapshot":
        print("GPT requested camera snapshot...")
        snapshot_path = capture_snapshot()

        if snapshot_path:
            image_data = encode_image(snapshot_path)

            # Second call — send the image back with the original prompt
            response = client.chat.completions.create(
                model="gpt-5.2",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }}
                    ]
                }]
            )
            return response.choices[0].message.content
        else:
            return "I tried to access the camera but couldn't get a snapshot."
    elif tool_call and tool_call.name == "get_distance":
        print("GPT requested ultrasonic distance...")
        try:
            distance_feet = Bridge.call("show_feet")
            
            # Second call — tell GPT the result so it can form a natural response
            response = client.responses.create(
                model="gpt-5.2",
                instructions="Keep your response within 20 words",
                input=[
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": f"Tool result: the distance is {distance_feet:.2f} feet."}
                ]
            )
            return response.output_text
        except Exception as e:
            return f"Couldn't get distance reading: {str(e)}"
        
    # No tool call — return the plain text response
    return response.output_text