from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio
import uvicorn
from typing import List

app = FastAPI()

# store active WebSocket connections
active_connections: List[WebSocket] = []

# serve the frontend HTML
@app.get("/")
async def get():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # receive messages from client if needed
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# function to send data to all connected WebSockets
async def send_detection_to_frontend(detection_data: dict):
    # send the data to all active WebSocket connections
    for connection in active_connections:
        await connection.send_json(detection_data)
