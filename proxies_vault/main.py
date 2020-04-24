"""
Main launcher of app
"""
from config import WEB_PORT
from server import Server

if __name__ == '__main__':
    app = Server(WEB_PORT)
    app.run()
