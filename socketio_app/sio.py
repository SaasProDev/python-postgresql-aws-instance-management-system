import os
import socketio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ahome.settings")
manager = socketio.RedisManager('')
sio = socketio.Server(client_manager=manager)