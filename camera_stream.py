import requests
import time
import json

DEVICE = 'Aid-80070001-0000-2000-9002-000000000a94' # karston's camera
# API URL:
API_URL = f'https://0myrzet12k.execute-api.us-east-1.amazonaws.com/prod/devices/{DEVICE}/data'
# API PARAMS:
API_PARAMS = {
    'key': '202504ut',
    'pj': 'kyoro',
    'isMobileDet': '1',
}


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
    print('\n===New Frame===')
    print(f"Timestamp: {data.get('timestamp')}")
    detections = data.get('detections', [])
    if not detections:
        print('No detections')
        return
    
    for i, det in enumerate(detections, 1):
        class_id = det['class_id']
        confidence = round(det['confidence'] * 100, 2)
        bbox = det['bbox']
        print(f'[{i}] Class ID: {class_id}, Confidence: {confidence}%, BBox: {bbox}')
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