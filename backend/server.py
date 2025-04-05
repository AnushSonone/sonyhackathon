import json
import socketio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# fastAPI setup
app = FastAPI()

# allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve static files (JavaScript, CSS, etc.)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# template setup (for rendering HTML files from the frontend dir)
templates = Jinja2Templates(directory="frontend")

# socket.IO server instance
sio = socketio.AsyncServer(async_mode='asgi')
sio_app = socketio.ASGIApp(sio, app)

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# event handlers
@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected.")

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected.")

@sio.event
async def detection(sid, data):
    print(f"Message from {sid}: {data}")

# function to send detection data to the frontend
async def send_detection_to_frontend(detection_data: dict):
    """Function to send detection data to all connected clients"""
    print(f"Sending data to frontend: {detection_data}")
    # emit the detection data to all clients connected via socket.io
    await sio.emit('detection', detection_data)

# add the Socket.io handler to FastAPI
app.mount("/socket.io", sio_app)
