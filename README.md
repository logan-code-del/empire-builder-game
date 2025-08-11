# 🏰 Empire Builder - Strategic Conquest Game

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Render-46E3B7.svg)](https://render.com)

A comprehensive web-based empire building strategy game where players create their own nations, build cities, manage resources, and engage in real-time combat for territorial expansion and world domination.

## 🎮 [Play Online](https://empire-builder.onrender.com) | 📖 [Documentation](CITIES_AND_BUILDINGS.md) | 🚀 [Deploy Guide](DEPLOYMENT.md)

![Empire Builder Screenshot](https://via.placeholder.com/800x400/1a1a1a/ffffff?text=Empire+Builder+Game+Screenshot)

## ✨ Features

### 🏰 Empire Management
- **Create Your Empire**: Choose your empire name, ruler, and starting location on a real world map
- **Resource Management**: Manage Gold, Food, Iron, Oil, and Population
- **Cities & Buildings**: Build cities and construct buildings to boost resource production
- **Land Expansion**: Purchase additional land for building construction and growth
- **Territory Control**: Start with 2,000 acres and expand through conquest and purchase
- **Real-time Updates**: Automatic resource generation and live game updates

### 🏙️ Cities & Buildings System
Build and manage cities to boost your empire's production:

| City Type | Buildings | Defense | Production | Cost |
|-----------|-----------|---------|------------|------|
| Small     | 15 max    | +10%    | Base       | 5K Gold |
| Medium    | 35 max    | +20%    | +10%       | 15K Gold |
| Large     | 60 max    | +30%    | +20%       | 40K Gold |

**Building Types:**
- 🌾 **Farms**: +25 Food/min
- ⛏️ **Mines**: +15 Iron/min  
- 🛢️ **Oil Wells**: +10 Oil/min
- 🏛️ **Banks**: +50 Gold/min
- 🏠 **Housing**: +20 Population/min
- 🏭 **Factories**: Multi-resource bonus

### ⚔️ Military System
Train and deploy diverse military forces:

| Unit Type | Attack | Defense | Speed | Cost | Best Use |
|-----------|--------|---------|-------|------|----------|
| Infantry  | 10     | 15      | 5     | Low  | Cheap, defensive |
| Tanks     | 25     | 20      | 8     | Med  | Balanced assault |
| Aircraft  | 30     | 10      | 15    | High | Fast strikes |
| Ships     | 20     | 25      | 6     | High | Naval dominance |

### 🌍 World Map & Combat
- **Interactive Map**: Real world geography with strategic positioning
- **Real-time Battles**: Advanced combat calculations with unit losses
- **Strategic Depth**: Unit composition and city bonuses matter
- **Risk vs Reward**: Capture resources but risk losing units

### 👥 Multiplayer Support
- **Real-time Multiplayer**: Battle other players instantly
- **AI Opponents**: Intelligent computer-controlled empires
- **Live Updates**: Socket.IO powered real-time notifications
- **Persistent World**: Your empire grows even when offline

## 🚀 Quick Start

### 🎮 Play Online (Recommended)
**[Start Playing Now!](https://empire-builder.onrender.com)**

### 💻 Local Development
```bash
# Clone the repository
git clone https://github.com/logan-code-del/empire-builder-game.git
cd empire-builder-game

# Install dependencies
pip install -r requirements.txt

# Run the game
python app.py

# Open browser to http://localhost:5000
```

## 🎯 How to Play

1. **Create Your Empire**
   - Choose empire name and ruler
   - Select starting location on world map
   - Begin with 2,000 acres and starting resources

2. **Build Your Economy**
   - Construct cities for building capacity
   - Build farms, mines, banks for resource production
   - Buy land for expansion opportunities

3. **Train Your Military**
   - Use resources to train Infantry, Tanks, Aircraft, Ships
   - Balance unit types for effective combat
   - Keep reserves for defense

4. **Conquer the World**
   - Attack other empires on the interactive map
   - Capture land and resources through victory
   - Defend against enemy attacks

## 📱 Screenshots

| Dashboard | World Map | Cities | Military |
|-----------|-----------|--------|----------|
| ![Dashboard](https://via.placeholder.com/200x150/2c3e50/ffffff?text=Dashboard) | ![World Map](https://via.placeholder.com/200x150/27ae60/ffffff?text=World+Map) | ![Cities](https://via.placeholder.com/200x150/3498db/ffffff?text=Cities) | ![Military](https://via.placeholder.com/200x150/e74c3c/ffffff?text=Military) |

## 🛠️ Technical Features

- **Framework**: Flask + Socket.IO for real-time gameplay
- **Production Server**: Gunicorn with eventlet for WebSocket support
- **Database**: SQLite with PostgreSQL support
- **Frontend**: Responsive HTML5/CSS3/JavaScript
- **Real-time**: WebSocket communication
- **Mobile**: Optimized for all devices
- **AI**: Intelligent computer opponents

## 🚀 Deployment

Deploy your own instance of Empire Builder:

### One-Click Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Deployment
See our [Deployment Guide](DEPLOYMENT.md) for detailed instructions on:
- Render deployment (recommended)
- Railway deployment  
- Heroku deployment
- Local development setup

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 Report Bugs
[Open an issue](https://github.com/logan-code-del/empire-builder-game/issues) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior

### 💡 Suggest Features
Have ideas? [Start a discussion](https://github.com/logan-code-del/empire-builder-game/discussions)!

### 🔧 Development
```bash
# Fork and clone
git clone https://github.com/logan-code-del/empire-builder-game.git
cd empire-builder-game

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_game.py

# Start development server
python app.py
```

## 📚 Documentation

- 📖 [Cities & Buildings Guide](CITIES_AND_BUILDINGS.md) - Complete building system guide
- 🚀 [Deployment Guide](DEPLOYMENT.md) - Deploy to various platforms
- 🌐 [Render Deploy Guide](RENDER_DEPLOY.md) - Detailed Render deployment
- 🔧 [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
- 🛠️ [Render Troubleshooting](RENDER_TROUBLESHOOTING.md) - Render-specific fixes
- ❓ [Help System](HELP_SYSTEM.md) - In-game help documentation

## 🏆 Roadmap

### ✅ Completed Features
- [x] Empire creation and management
- [x] Real-time combat system
- [x] Cities and buildings system
- [x] AI opponents with strategic behavior
- [x] Resource management and production
- [x] Interactive world map
- [x] Mobile-responsive design
- [x] Real-time multiplayer support
- [x] User authentication system
- [x] Alliance system

### 🔄 In Development
- [ ] Leaderboards and rankings
- [ ] Tournament modes

### 💭 Future Plans
- [ ] Chat system for players
- [ ] Email notifications
- [ ] Advanced AI difficulty levels
- [ ] Custom map editor
- [ ] Achievement system
- [ ] Trade system between empires

## 📊 Project Stats

- **Language**: Python 3.11+
- **Framework**: Flask + Socket.IO
- **Database**: SQLite (PostgreSQL ready)
- **Frontend**: HTML5, CSS3, JavaScript
- **Real-time**: WebSocket support
- **Mobile**: Fully responsive
- **Deployment**: Heroku, Railway, Render ready

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask Team** - Amazing web framework
- **Socket.IO** - Real-time communication
- **OpenStreetMap** - World map data
- **Font Awesome** - Beautiful icons
- **Bootstrap** - Responsive UI components
- **Classic Strategy Games** - Inspiration for game mechanics

## 💬 Community & Support

- 🐛 [Report Issues](https://github.com/logan-code-del/empire-builder-game/issues)
- 💡 [Feature Requests](https://github.com/logan-code-del/empire-builder-game/discussions)
- 📧 [Contact Developer](mailto:development.doom.endnote612@passfwd.com)
- ⭐ [Star this Project](https://github.com/logan-code-del/empire-builder-game)

## ⭐ Support the Project

If you enjoy Empire Builder, please:
- ⭐ **Star** this repository
- 🍴 **Fork** and contribute
- 🐛 **Report** bugs and issues
- 💡 **Suggest** new features
- 📢 **Share** with friends

---

<div align="center">

**🌍 Ready to build your empire and conquer the world? 🏰**

### [🎮 Start Playing Now!](https://empire-builder.onrender.com)

*Build • Expand • Conquer • Dominate*

**Made with ❤️ for strategy game enthusiasts**

</div>
