import os
import uuid
import socket

from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from redis import Redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

redis = Redis(host='redis', port=6379)

host = socket.gethostname()
host_ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]

test = 0
test2 = 0

@app.route('/')
def hello():
    return render_template('index.html')


@socketio.on('connect', namespace='/mcc')
def ws_conn():
    c = redis.incr('hits')
    socketio.emit('hits_count', {'hits_count': c, 'host_ip': host_ip, 'host': host}, namespace='/mcc')

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)
