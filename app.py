from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'arunisto@chat_app'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('chat.html')

# Event: Join a room
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', f'{username} has entered the room.', to=room)

# Event: Leave a room
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', f'{username} has left the room.', to=room)

# Event: Sending a message to a room
@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    emit('message', message, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
