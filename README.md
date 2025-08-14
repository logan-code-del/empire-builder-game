# 🏰 Empire Builder - Strategic Conquest Game

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.2.5+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Custom-red.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/Docs-Read%20the%20Docs-blue.svg)](https://empire-builder.readthedocs.io/)
[![Deploy](https://img.shields.io/badge/Deploy-Render-46E3B7.svg)](https://render.com)

A comprehensive web-based empire building strategy game where players create their own nations, build cities, manage resources, and engage in real-time combat for territorial expansion and world domination.

**Created by Logan-code-del and Doom** | **All Rights Reserved**

## 🎮 [Play Online](https://empire-builder.onrender.com) | 📖 [Full Documentation](https://empire-builder.readthedocs.io/) | 🚀 [Deploy Guide](DEPLOYMENT.md)

## ⚠️ IMPORTANT LEGAL NOTICE

**This software is protected by comprehensive legal terms and conditions. By using, modifying, or deploying this software, you agree to be legally bound by our Terms and Conditions, which include:**

- **Mandatory attribution requirements** for any deployment
- **Commercial use restrictions** without explicit permission
- **Severe legal penalties** for violations (up to $100,000 per violation)
- **Criminal prosecution** under applicable copyright laws

**📋 [Read Full Terms and Conditions](TERMS_AND_CONDITIONS.md) | 📄 [License Agreement](LICENSE) | © [Copyright Notice](COPYRIGHT)**

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

- **Framework**: Flask 2.2.5+ with Socket.IO for real-time gameplay
- **Database**: Supabase (PostgreSQL) with SQLite fallback
- **Production Server**: Gunicorn with eventlet for WebSocket support
- **Frontend**: Responsive HTML5/CSS3/JavaScript with Bootstrap
- **Real-time**: WebSocket communication for live updates
- **Authentication**: Secure user registration and login system
- **Mobile**: Fully optimized for all devices and screen sizes
- **AI**: Intelligent computer opponents with strategic behavior
- **Documentation**: Comprehensive Sphinx documentation on Read the Docs
- **Legal Protection**: Complete terms, conditions, and copyright framework

## 🚀 Deployment

**⚠️ IMPORTANT: All deployments must comply with our [Terms and Conditions](TERMS_AND_CONDITIONS.md) and include proper attribution.**

Deploy your own instance of Empire Builder:

### One-Click Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Deployment Options
See our comprehensive documentation for detailed instructions:

- 📖 **[Complete Documentation](https://empire-builder.readthedocs.io/)** - Full deployment guide
- 🚀 **[Render Deployment](DEPLOYMENT.md)** - Recommended platform
- 🐳 **[Docker Deployment](DEPLOYMENT.md#docker-deployment)** - Containerized deployment
- ☁️ **[Heroku Deployment](DEPLOYMENT.md#heroku-deployment)** - Alternative cloud platform
- 🖥️ **[Local Development](DEPLOYMENT.md#local-development)** - Development setup

### Attribution Requirements
**ALL deployments MUST include this attribution:**

```
Empire Builder Game - Originally created by Logan-code-del and Doom
GitHub: https://github.com/logan-code-del/empire-builder-game
Contact: development.doom.endnote612@passfwd.com

This deployment is based on the original Empire Builder codebase.
All rights reserved to original creators.
```

## 🤝 Contributing

**⚠️ IMPORTANT: All contributions must comply with our [Terms and Conditions](TERMS_AND_CONDITIONS.md). Major modifications require approval via GitHub Issues.**

We welcome contributions! Here's how you can help:

### 🐛 Report Bugs
[Open an issue](https://github.com/logan-code-del/empire-builder-game/issues) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, browser)

### 💡 Suggest Features
Have ideas? [Start a discussion](https://github.com/logan-code-del/empire-builder-game/discussions)!

### 🔧 Development Setup
```bash
# Fork and clone
git clone https://github.com/logan-code-del/empire-builder-game.git
cd empire-builder-game

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run tests
python -m unittest discover tests

# Start development server
python app.py
```

### 📋 Contribution Guidelines
- **Small changes** (bug fixes, minor improvements): Submit pull requests directly
- **Major changes** (>25% of codebase, core features): Request approval via GitHub Issues first
- **Commercial modifications**: Require explicit written permission
- **Attribution**: Must maintain all copyright notices and attribution

## 📚 Documentation

### 📖 Complete Documentation
- **[Read the Docs](https://empire-builder.readthedocs.io/)** - Comprehensive documentation with:
  - Installation and quickstart guide
  - Game mechanics and features
  - API reference and development guide
  - Deployment instructions for all platforms
  - Authentication and security details

### 📋 Legal Documentation
- **[Terms and Conditions](TERMS_AND_CONDITIONS.md)** - Complete legal terms
- **[License Agreement](LICENSE)** - Custom license with usage rights
- **[Copyright Notice](COPYRIGHT)** - Copyright and ownership information

### 🛠️ Technical Guides
- **[Cities & Buildings Guide](CITIES_AND_BUILDINGS.md)** - Complete building system
- **[Deployment Guide](DEPLOYMENT.md)** - Deploy to various platforms
- **[Render Deploy Guide](RENDER_DEPLOY.md)** - Detailed Render deployment
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions
- **[Help System](HELP_SYSTEM.md)** - In-game help documentation

## 🏆 Roadmap

### ✅ Completed Features
- [x] Empire creation and management system
- [x] Real-time combat with advanced calculations
- [x] Cities and buildings system with production bonuses
- [x] AI opponents with strategic behavior
- [x] Resource management and automatic production
- [x] Interactive world map with real geography
- [x] Mobile-responsive design for all devices
- [x] Real-time multiplayer support via WebSockets
- [x] Secure user authentication and registration
- [x] Alliance system for diplomatic gameplay
- [x] Comprehensive legal framework and terms
- [x] Complete Sphinx documentation on Read the Docs
- [x] Multiple deployment options (Render, Heroku, Docker)
- [x] Supabase database integration
- [x] Unit testing and quality assurance

### 🔄 In Development
- [ ] Advanced leaderboards and global rankings
- [ ] Tournament modes and competitive seasons
- [ ] Enhanced AI difficulty levels
- [ ] Performance optimizations

### 💭 Future Plans
- [ ] Real-time chat system for players
- [ ] Email notifications for important events
- [ ] Custom map editor for user-created worlds
- [ ] Achievement system with rewards
- [ ] Trade system between empires
- [ ] Mobile app versions (iOS/Android)
- [ ] Advanced analytics and statistics

## 📊 Project Stats

- **Language**: Python 3.11+
- **Framework**: Flask 2.2.5+ with Socket.IO 5.3.4+
- **Database**: Supabase (PostgreSQL) with SQLite fallback
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap
- **Real-time**: WebSocket support via Socket.IO
- **Mobile**: Fully responsive design
- **Documentation**: Sphinx with Read the Docs hosting
- **Testing**: Comprehensive unit test coverage
- **Deployment**: Render, Heroku, Docker, and local development ready
- **Legal**: Complete terms, conditions, and copyright protection

## 📄 License and Legal

**⚠️ IMPORTANT: This project uses a custom license with specific terms and conditions.**

- **License**: Custom License Agreement - see [LICENSE](LICENSE) file
- **Terms**: Complete Terms and Conditions - see [TERMS_AND_CONDITIONS.md](TERMS_AND_CONDITIONS.md)
- **Copyright**: Full copyright protection - see [COPYRIGHT](COPYRIGHT) file
- **Attribution**: Required for all deployments and modifications
- **Commercial Use**: Requires explicit written permission
- **Violations**: Subject to severe legal penalties up to $100,000 per violation

**By using this software, you agree to be legally bound by all terms and conditions.**

## 🙏 Acknowledgments

- **Flask Team** - Amazing web framework for Python
- **Socket.IO** - Real-time bidirectional communication
- **Supabase** - Modern database and authentication platform
- **OpenStreetMap** - World map data and geographic information
- **Font Awesome** - Beautiful icons and graphics
- **Bootstrap** - Responsive UI components and styling
- **Sphinx** - Documentation generation system
- **Read the Docs** - Documentation hosting platform
- **Classic Strategy Games** - Inspiration for game mechanics and design

## 💬 Community & Support

### 🔗 Official Links
- 🎮 **[Play Online](https://empire-builder.onrender.com)** - Official game instance
- 📖 **[Documentation](https://empire-builder.readthedocs.io/)** - Complete documentation
- 🐛 **[Report Issues](https://github.com/logan-code-del/empire-builder-game/issues)** - Bug reports and technical issues
- 💡 **[Feature Requests](https://github.com/logan-code-del/empire-builder-game/discussions)** - Ideas and suggestions
- ⭐ **[Star this Project](https://github.com/logan-code-del/empire-builder-game)** - Show your support

### 📧 Contact Information
- **General Inquiries**: development.doom.endnote612@passfwd.com
- **Legal Questions**: Submit via GitHub Issues with "Legal" tag
- **Permission Requests**: Submit via GitHub Issues with detailed proposal
- **Technical Support**: Use GitHub Issues for fastest response

### 🏷️ Issue Templates
When reporting issues, please use these tags:
- `bug` - Software bugs and errors
- `enhancement` - Feature requests and improvements
- `legal` - Legal questions and permission requests
- `documentation` - Documentation improvements
- `deployment` - Deployment and setup issues

## ⭐ Support the Project

If you enjoy Empire Builder, please:
- ⭐ **Star** this repository to show your support
- 🍴 **Fork** and contribute (following our legal terms)
- 🐛 **Report** bugs and issues via GitHub Issues
- 💡 **Suggest** new features through discussions
- 📢 **Share** with friends and fellow strategy game enthusiasts
- 📖 **Read** and follow our comprehensive documentation

**Remember**: All contributions and usage must comply with our [Terms and Conditions](TERMS_AND_CONDITIONS.md)

---

<div align="center">

# 🌍 Ready to build your empire and conquer the world? 🏰

## [🎮 Start Playing Now!](https://empire-builder.onrender.com)

### *Build • Expand • Conquer • Dominate*

**Created with ❤️ by Logan-code-del and Doom**  
**For strategy game enthusiasts worldwide**

---

### 📋 Quick Links
**[Play Game](https://empire-builder.onrender.com)** • **[Documentation](https://empire-builder.readthedocs.io/)** • **[GitHub](https://github.com/logan-code-del/empire-builder-game)** • **[Issues](https://github.com/logan-code-del/empire-builder-game/issues)**

---

**© 2024 Logan-code-del and Doom. All Rights Reserved.**  
*This project is protected by comprehensive legal terms and conditions.*

**Empire Builder Game - Originally created by Logan-code-del and Doom**  
**GitHub**: https://github.com/logan-code-del/empire-builder-game  
**Contact**: development.doom.endnote612@passfwd.com

</div>
