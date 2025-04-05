from dotenv import load_dotenv
import requests
import time
import os
import random
import asyncio
import sys

# server.py file in root dir
from server import send_detection

# use env for API protection
load_dotenv()
DEVICE = os.getenv('DEVICE')
API_PARAMS = {
    'key': os.getenv('API_KEY'),
    'pj': os.getenv('API_PJ'),
    'isMobileDet': os.getenv('API_IS_MOBILE_DET'),
}
API_URL = f'https://0myrzet12k.execute-api.us-east-1.amazonaws.com/prod/devices/{DEVICE}/data'


def fetch_camera_data():
    """Real time data fetch from the camera"""
    try:
        response = requests.get(API_URL, params=API_PARAMS)
        response.raise_for_status() # raise bad response errors
        return response.json()
    except Exception as e:
        print(f'[Error] Failed to fetch data: {e}')
        return None
    
def display_detections(data):
    print('\n===New Frame===')
    print(f"Timestamp: {data.get('timestamp')}")
    detections = data.get('detections', [])
    if not detections:
        print('No detections')
        return
    
    for i, det in enumerate(detections, 1):
        class_name = det['class_name']
        if class_name != 'person':
            continue

        user_type = det.get('user_type', 'unknown')

        detection_data = {
            'class_name': class_name,
            'user_type': user_type
        }

        send_detection(detection_data)

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
                    'user_type': random.choice(['local', 'guest', 'unknown'])
                },
                {
                    'class_name': random.choice(['car', 'tv', 'bed']),
                    'user_type': 'unknown'
                }
            ]
        }
        yield fake_data
        await asyncio.sleep(2)  # simulate delay

def main(test_mode=False): # default to real version
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