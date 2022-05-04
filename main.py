# -*- coding: utf-8 -*-
# main.py

from app import app, socketio


if __name__ == '__main__':
    socketio.run(app, debug=True)
