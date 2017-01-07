from flask import Flask
import socket
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    count = redis.incr('hits')
    host = socket.gethostname()
    host_ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
    return 'Hello World! I have been seen {} times.\n So, you hit REDIS for {} times. Server HOST IP={} and HOST={}.\n'.format(count, count, host_ip, host)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
