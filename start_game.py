#!/usr/bin/env python3
"""
Empire Builder - Simple Game Starter
Quick start script that launches the game and opens browser
"""

import webbrowser
import time
import threading
import subprocess
import sys

def open_browser():
    """Open browser after a short delay"""
    time.sleep(3)
    print("🌐 Opening browser...")
    webbrowser.open('http://localhost:5000')

def main():
    print("🏰 Starting Empire Builder...")
    print("📍 Server will be available at: http://localhost:5000")
    
    # Start browser in background
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the Flask application
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Game stopped by user")

if __name__ == "__main__":
    main()