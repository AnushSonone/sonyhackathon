import firebase_admin
from firebase_admin import credentials, storage
import urllib.request
from PIL import Image, ImageTk
import tkinter as tk
import io
from datetime import timedelta
from dotenv import load_dotenv
import os
import json

# Load env variables
load_dotenv()

# Construct the service account JSON from env vars
service_account_info = {
    "type": "service_account",
    "project_id": "sonyaitrios",
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": "firebase-adminsdk-fbsvc@sonyaitrios.iam.gserviceaccount.com",
    "client_id": "109582101077702986298",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40sonyaitrios.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'sonyaitrios.firebasestorage.app'
})

# Access the image
bucket = storage.bucket()
blob = bucket.blob('license.jpg')

# Generate a signed URL
image_url = blob.generate_signed_url(
    version="v4",
    expiration=timedelta(minutes=60),
    method="GET"
)

# Download and display image
with urllib.request.urlopen(image_url) as response:
    image_data = response.read()

image = Image.open(io.BytesIO(image_data))

# Show popup
root = tk.Tk()
root.title("License Viewer")
image.thumbnail((800, 800))
img_tk = ImageTk.PhotoImage(image)
label = tk.Label(root, image=img_tk)
label.pack()
root.mainloop()