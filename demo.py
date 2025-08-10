#!/usr/bin/env python3
"""
Empire Builder - Demo Script
Demonstrates key features of the Empire Builder game
"""

import os
import sys
import time
import webbrowser
import subprocess
from pathlib import Path

def print_banner():
    """Print game banner"""
    print("🏰" + "=" * 60 + "🏰")
    print("🏰" + " " * 20 + "EMPIRE BUILDER" + " " * 20 + "🏰")
    print("🏰" + " " * 15 + "Strategic Conquest Game" + " " * 15 + "🏰")
    print("🏰" + "=" * 60 + "🏰")

def print_features():
    """Print game features"""
    print("\n🎮 GAME FEATURES:")
    print("=" * 50)
    
    features = [
        ("🏛️", "Empire Creation", "Create your own empire with custom name and ruler"),
        ("🗺️", "Global Map", "Choose starting location on real world map"),
        ("⚔️", "Military Units", "Train Infantry, Tanks, Aircraft, and Ships"),
        ("💰", "Resource Management", "Manage Gold, Food, Iron, Oil, and Population"),
        ("🎯", "Real-time Combat", "Advanced battle system with unit losses"),
        ("🤖", "AI Opponents", "Fight against intelligent AI empires"),
        ("👥", "Multiplayer", "Play against other human players"),
        ("📊", "Live Updates", "Real-time notifications and data refresh"),
        ("🌍", "Territory Expansion", "Capture land and resources from enemies"),
        ("📈", "Strategic Depth", "Balance economy, military, and expansion")
    ]
    
    for icon, title, description in features:
        print(f"{icon} {title:20} - {description}")

def print_gameplay():
    """Print gameplay instructions"""
    print("\n🎯 HOW TO PLAY:")
    print("=" * 50)
    
    steps = [
        "1. 🏗️  Create your empire with a unique name and ruler",
        "2. 📍  Choose your starting location on the world map",
        "3. 💰  Start with 2,000 acres and basic resources",
        "4. 🏭  Train military units using your resources",
        "5. 🗺️  Explore the world map to find other empires",
        "6. ⚔️  Attack weaker empires to capture land and resources",
        "7. 🛡️  Defend your territory from enemy attacks",
        "8. 📈  Grow your empire through strategic expansion",
        "9. 👑  Become the dominant empire on the world map!"
    ]
    
    for step in steps:
        print(step)

def print_units():
    """Print unit information"""
    print("\n⚔️ MILITARY UNITS:")
    print("=" * 50)
    
    units = [
        ("🏃", "Infantry", "ATK: 10 | DEF: 15 | SPD: 5", "Basic ground forces, cheap and reliable"),
        ("🚗", "Tanks", "ATK: 25 | DEF: 20 | SPD: 8", "Heavy ground units with high attack power"),
        ("✈️", "Aircraft", "ATK: 30 | DEF: 10 | SPD: 15", "Fast air units with strong offense"),
        ("🚢", "Ships", "ATK: 20 | DEF: 25 | SPD: 6", "Naval forces with balanced stats")
    ]
    
    for icon, name, stats, description in units:
        print(f"{icon} {name:10} {stats:25} - {description}")

def demo_battle():
    """Demonstrate battle system"""
    print("\n⚔️ BATTLE DEMONSTRATION:")
    print("=" * 50)
    
    print("🏛️ Your Empire vs 🤖 AI Empire")
    print("📊 Your Forces: 200 Infantry, 50 Tanks, 20 Aircraft, 10 Ships")
    print("📊 Enemy Forces: 150 Infantry, 30 Tanks, 15 Aircraft, 8 Ships")
    print("🎯 Attack Force: 100 Infantry, 25 Tanks, 10 Aircraft, 5 Ships")
    
    print("\n⚡ Calculating battle...")
    time.sleep(1)
    
    # Simulate battle calculation
    your_power = 100*10 + 25*25 + 10*30 + 5*20  # 2225
    enemy_power = 150*15 + 30*20 + 15*10 + 8*25  # 3200
    
    print(f"💪 Your Attack Power: {your_power:,}")
    print(f"🛡️ Enemy Defense Power: {enemy_power:,}")
    
    if your_power > enemy_power * 0.8:  # Close battle
        print("🎉 VICTORY! You captured 200 acres and resources!")
        print("💀 Your Losses: 15 Infantry, 3 Tanks, 1 Aircraft")
        print("💀 Enemy Losses: 25 Infantry, 8 Tanks, 2 Aircraft, 1 Ship")
    else:
        print("😞 DEFEAT! Your attack was repelled!")
        print("💀 Your Losses: 30 Infantry, 8 Tanks, 3 Aircraft, 2 Ships")
        print("💀 Enemy Losses: 10 Infantry, 2 Tanks")

def start_game():
    """Start the game"""
    print("\n🚀 STARTING EMPIRE BUILDER...")
    print("=" * 50)
    
    try:
        # Check if we're in the right directory
        if not Path("app.py").exists():
            print("❌ Error: Not in empire directory!")
            print("Please run this demo from the empire/ directory")
            return False
        
        print("📦 Checking dependencies...")
        
        # Try to import required modules
        try:
            import flask
            import flask_socketio
            print("✅ Dependencies found")
        except ImportError:
            print("📦 Installing dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed")
        
        print("🌐 Starting web server...")
        print("📍 Game will be available at: http://localhost:5000")
        print("🔄 Opening browser in 3 seconds...")
        
        # Open browser
        def open_browser():
            time.sleep(3)
            webbrowser.open('http://localhost:5000')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the game
        subprocess.run([sys.executable, "app.py"])
        
    except KeyboardInterrupt:
        print("\n🛑 Game stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        return False

def main():
    """Main demo function"""
    print_banner()
    print_features()
    print_gameplay()
    print_units()
    demo_battle()
    
    print("\n" + "=" * 60)
    print("🎮 Ready to play Empire Builder?")
    print("=" * 60)
    
    while True:
        choice = input("\n[S]tart Game, [T]est Features, or [Q]uit? ").lower().strip()
        
        if choice in ['s', 'start']:
            if start_game():
                break
        elif choice in ['t', 'test']:
            print("\n🧪 Running feature tests...")
            try:
                subprocess.run([sys.executable, "test_game.py"])
            except Exception as e:
                print(f"❌ Test error: {e}")
        elif choice in ['q', 'quit']:
            print("👋 Thanks for checking out Empire Builder!")
            break
        else:
            print("❓ Please enter S, T, or Q")

if __name__ == "__main__":
    main()