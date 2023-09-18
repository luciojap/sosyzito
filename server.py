import os
from flask import Flask, send_from_directory, render_template, redirect
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

port = int(os.environ.get("PORT", 5000))

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')

@socketio.on("connect")
def on_connect():
    print("Cliente conectado")

@socketio.on("message")
def handle_message(message):
    for user in users:
        socketio.emit("message", message, room=user)

@socketio.on("join")
def on_join(username):
    users.append(username)
    print(f"El usuario {username} se ha unido")
    socketio.emit("message", f"El usuario {username} se ha unido", room=username)

@socketio.on("leave")
def on_leave(username):
    users.remove(username)
    print(f"El usuario {username} se ha ido")
    socketio.emit("message", f"El usuario {username} se ha ido", room=username)

if __name__ == "__main__":
    socketio.run(app)