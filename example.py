"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import asyncio
import websockets
import base64
import cv2
import numpy as np
import json
from gaze_tracking import GazeTracking
import os
print("Current working directory:", os.getcwd())
import gaze_tracking
print("Model file exists:", os.path.exists(
    os.path.join(os.path.dirname(gaze_tracking.__file__), "trained_models", "shape_predictor_68_face_landmarks.dat")
))

# Initialize GazeTracking
gaze = GazeTracking()
HORIZONTAL_THRESHOLD = 0.2  # Distance from center 0.5 exceeding 0.2 is considered distracted

async def process(websocket, path):
    print(f"Client connected to path: {path}")
    print("Client connected")
    async for message in websocket:
        try:
            data = json.loads(message)
            img_b64 = data.get('image')
            if not img_b64:
                continue
            # Remove base64 header
            if ',' in img_b64:
                img_b64 = img_b64.split(',')[1]
            img_bytes = base64.b64decode(img_b64)
            np_arr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is None:
                continue
            # GazeTracking analysis
            gaze.refresh(frame)
            # Determine if focused
            status = "focused"
            hr = gaze.horizontal_ratio()
            if hr is not None and abs(hr - 0.5) > HORIZONTAL_THRESHOLD:
                status = "distracted"
            if gaze.is_blinking():
                status = "distracted"
            # Return status
            await websocket.send(json.dumps({"status": status}))
        except Exception as e:
            print("Error processing frame:", e)
            continue

async def main():
    print("WebSocket service starting, listening on ws://0.0.0.0:8765 ...")
    async with websockets.serve(process, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
