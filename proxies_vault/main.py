"""
Main launcher of app
"""

from server import Server

if __name__ == '__main__':
    app = Server()
    app.run()