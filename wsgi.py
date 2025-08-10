"""
WSGI entry point for Empire Builder
Used by production servers like Gunicorn
"""

from app import app, socketio

# For Gunicorn to use
application = socketio

if __name__ == "__main__":
    socketio.run(app)