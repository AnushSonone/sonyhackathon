import requests
import time
import json
from dotenv import load_dotenv
import os

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
    """Display detections in a digestible format"""
    print('\n=== New Frame ===')
    print(f"Timestamp: {data.get('timestamp')}")
    detections = data.get('detections', [])
    
    if not detections:
        print('No detections')
        return

    # filter only person class detections
    person_detections = [det for det in detections if det.get('class_name') == 'person']

    if not person_detections:
        print('No person detected')
        return

    for i, det in enumerate(person_detections, 1):
        class_id = det['class_id']
        class_name = det['class_name']
        confidence = round(det['confidence'] * 100, 2)
        bbox = det['bbox']
        print(f'[{i}] Class: {class_name}, ID: {class_id}, Confidence: {confidence}%, BBox: {bbox}')
    print('====================\n')

    # delay so API doesn't spam
    time.sleep(1)


def main():
    print("Starting live camera polling...\n")
    while True:
        data = fetch_camera_data()
        if data:
            display_detections(data)
        else:
            print('No data received, retrying...')
            time.sleep(5)  # wait before retrying

if __name__ == "__main__":
    main()