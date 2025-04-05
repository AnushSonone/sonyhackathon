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
        print(f'Fetching data from {API_URL}...')
        
        response = requests.get(API_URL, params=API_PARAMS)
        response.raise_for_status()  # raise error if the response is bad
        return response.json()
    except Exception as e:
        print(f'[Error] Failed to fetch data: {e}')
        return None

async def handle_detections(data):
    """Handle and display detection data"""
    print('\n=== New Frame ===')
    print(f"Timestamp: {data.get('timestamp')}")
    detections = data.get('detections', [])
    
    if not detections:
        print('No detections')
    else:
        for i, det in enumerate(detections, 1):
            class_name = det.get('class_name')
            if class_name != 'person':
                continue  # skip non-person classes

            user_type = det.get('user_type', 'unknown')

            detection_data = {
                'class_name': class_name,
                'user_type': user_type
            }

            # Send detection to frontend
            await send_detection_to_frontend(detection_data)

            print(f'[{i}] {class_name} ({user_type})')

    print('====================\n')
    await asyncio.sleep(1)  # small delay for readability

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

async def run_fake_mode():
    print("Starting in TEST mode (Fake Data)...\n")
    async for fake_data in generate_fake_data():
        await handle_detections(fake_data)

async def run_live_mode():
    print("Starting live camera polling...\n")
    while True:
        data = fetch_camera_data()
        if data:
            await handle_detections(data)
        else:
            print('No data received, retrying...')
            await asyncio.sleep(5)

def main(test_mode=False):
    loop = asyncio.get_event_loop()
    if test_mode:
        loop.run_until_complete(run_fake_mode())
    else:
        loop.run_until_complete(run_live_mode())

if __name__ == "__main__":
    # check if 'test' argument is passed
    test_mode = len(sys.argv) > 1 and sys.argv[1].lower() == "test"
    main(test_mode)
