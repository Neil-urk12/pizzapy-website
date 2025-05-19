# asgi.py
from app import create_app
from flask import Flask
from asgiref.wsgi import WsgiToAsgi

flask_app: Flask = create_app()
application = WsgiToAsgi(flask_app)
