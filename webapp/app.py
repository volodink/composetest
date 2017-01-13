import html
import socket
from flask import Flask, render_template
from flask_socketio import SocketIO
from redis import Redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

redis = Redis(host='redis', port=6379)

redis.set('users_online', 0)

host = socket.gethostname()
host_ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]


@app.route('/')
def hello():
    return render_template('index.html')


@socketio.on('connect', namespace='/mcc')
def ws_conn():
    c = redis.incr('hits')
    users_online = redis.incr('users_online')
    print('Socket connected. Users online: {}. Yay!'.format(users_online))
    socketio.emit('hits_count', {'hits_count': c, 'host_ip': host_ip, 'host': host, 'users_online': users_online}, namespace='/mcc')


@socketio.on("disconnect", namespace='/mcc')
def ws_discon():
    c = redis.incr('hits')
    users_online = redis.decr('users_online')
    print('Socket disconnected. Users left: {}. Bye!'.format(users_online))
    socketio.emit('hits_count', {'hits_count': c, 'host_ip': host_ip, 'host': host, 'users_online': users_online}, namespace='/mcc')


@socketio.on('msg', namespace='/mcc')
def ws_message(message):
    redis.incr('hits')
    socketio.emit('msg', {'message': html.escape(message['message'])}, namespace='/mcc')


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
