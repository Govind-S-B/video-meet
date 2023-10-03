from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request
from pyngrok import ngrok

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('meet.html')

@socketio.on('connect')
def handle_connect():
    emit('user_connected', request.sid, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    emit('user_disconnected', request.sid, broadcast=True)

@socketio.on('offer')
def handle_offer(data):
    emit('offer', data, room=data['target'])

@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, room=data['target'])

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    emit('ice_candidate', data, room=data['target'])

if __name__ == '__main__':
    # Start ngrok tunnel
    public_url = ngrok.connect(8000, bind_tls=True).public_url
    print(f" * ngrok tunnel: {public_url}")

    # Run Flask app
    socketio.run(app, host='0.0.0.0', port=8000)