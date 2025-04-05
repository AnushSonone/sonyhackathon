from flask import Flask, render_template
from flask_socketio import SocketIO
import os

app = Flask(__name__, static_folder='frontend', template_folder='frontend')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return app.send_static_file('index.html')

def send_detection(data):
    socketio.emit('detection', data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)