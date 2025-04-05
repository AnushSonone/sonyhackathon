import asyncio
import random
import time
import requests
import json
import os
import sys
from dotenv import load_dotenv
from server import send_detection_to_frontend

# Load environment variables
load_dotenv()
DEVICE = os.getenv('DEVICE')
API_PARAMS = {
    'key': os.getenv('API_KEY'),
    'pj': os.getenv('API_PJ'),
    'isMobileDet': os.getenv('API_IS_MOBILE_DET'),
}
API_URL = f'https://0myrzet12k.execute-api.us-east-1.amazonaws.com/prod/devices/{DEVICE}/data'

def fetch_camera_data():
    """Fetch real-time data from the camera"""
    try:
        response = requests.get(API_URL, params=API_PARAMS)
        response.raise_for_status()  # raise error if the response is bad
        return response.json()
    except Exception as e:
        print(f'[Error] Failed to fetch data: {e}')
        return None

def display_detections(data):
    """Display and handle detection data"""
    print('\n===New Frame===')
    print(f"Timestamp: {data.get('timestamp')}")
    detections = data.get('detections', [])
    if not detections:
        print('No detections')
        return

    # process each detection
    for i, det in enumerate(detections, 1):
        class_name = det['class_name']
        if class_name != 'person':
            continue

        user_type = det.get('user_type', 'unknown')

        detection_data = {
            'class_name': class_name,
            'user_type': user_type
        }

        # send detection data to the frontend via WebSocket (using socket.io)
        asyncio.create_task(send_detection_to_frontend(detection_data))

        print(f'[{i}] {class_name} ({user_type})')
    print('====================\n')
    time.sleep(1)

async def generate_fake_data():
    """Simulate a stream of detection data (in case wifi not working)"""
    while True:
        fake_data = {
            'timestamp': time.time(),
            'detections': [
                {
                    'class_name': 'person',
                    'user_type': random.choice(['local', 'tourist'])
                },
                {
                    'class_name': random.choice(['car', 'tv', 'bed']),
                    'user_type': 'unknown'
                }
            ]
        }
        yield fake_data
        await asyncio.sleep(5)  # simulate delay

def main(test_mode=False):  # default to real version
    if test_mode:
        print("Starting in TEST mode (Fake Data)...\n")
        loop = asyncio.get_event_loop()

        async def run_fake():
            async for fake_data in generate_fake_data():
                display_detections(fake_data)

        loop.run_until_complete(run_fake())
    else:
        print("Starting live camera polling...\n")
        while True:
            data = fetch_camera_data()
            if data:
                display_detections(data)
            else:
                print('No data received, retrying...')
                time.sleep(5)  # wait before retrying

if __name__ == "__main__":
    # check if 'test' argument is passed
    test_mode = len(sys.argv) > 1 and sys.argv[1].lower() == "test"
    main(test_mode)
