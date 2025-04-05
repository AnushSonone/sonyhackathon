from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

# fastAPI setup
app = FastAPI()

# serve static files (JavaScript, CSS, etc.)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# template setup (for rendering HTML files from my frontend dir)
templates = Jinja2Templates(directory="frontend")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# sebSocket setup (optional, if needed for real-time communication)
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")
