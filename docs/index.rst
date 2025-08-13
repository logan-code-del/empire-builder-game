Empire Builder Documentation
============================

Welcome to Empire Builder - a real-time multiplayer strategy game built with Flask and Supabase.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   installation
   game-mechanics
   authentication
   api-reference
   development
   deployment

Overview
========

Empire Builder is a web-based multiplayer strategy game that combines classic empire-building gameplay with modern real-time web technologies. Players build and manage empires, engage in battles, form alliances, and compete for dominance in a persistent online world.

🏰 **Key Features**
   - Real-time multiplayer gameplay with WebSocket support
   - Persistent game state using Supabase PostgreSQL
   - Advanced battle and combat systems
   - Resource management and city building
   - Alliance and diplomacy systems
   - Comprehensive user authentication and session management

🚀 **Technology Stack**
   - **Backend**: Flask 2.2.5, Python 3.11+
   - **Database**: Supabase (PostgreSQL) with real-time subscriptions
   - **Real-time**: Flask-SocketIO for WebSocket communication
   - **Frontend**: HTML5/CSS3, JavaScript, Jinja2 templates
   - **Authentication**: Custom Supabase-based auth system

Quick Start
===========

Get Empire Builder running in minutes:

.. code-block:: bash

   # Clone and navigate to empire directory
   cd empire

   # Install dependencies
   pip install -r requirements.txt

   # Set up environment variables
   cp .env.template .env
   # Edit .env with your Supabase credentials

   # Run the application
   python app_supabase.py

The game will be available at http://localhost:5000

Game Features
=============

🏛️ **Empire Management**
   - Build and upgrade cities
   - Manage resources (gold, food, materials)
   - Research technologies
   - Train military units

⚔️ **Combat System**
   - Real-time battles between players
   - Strategic unit positioning
   - Terrain and weather effects
   - Battle history and statistics

🤝 **Multiplayer Features**
   - Alliance formation and management
   - Diplomatic relations
   - Global chat and messaging
   - Leaderboards and rankings

🔧 **Administrative Tools**
   - User account management
   - Game moderation features
   - Analytics and reporting
   - Backup and recovery systems

Architecture
============

Empire Builder uses a modern, scalable architecture:

.. code-block:: text

   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
   │   Web Browser   │◄──►│  Flask Server   │◄──►│   Supabase DB   │
   │                 │    │                 │    │                 │
   │ • HTML/CSS/JS   │    │ • Game Logic    │    │ • PostgreSQL    │
   │ • WebSocket     │    │ • Authentication│    │ • Real-time     │
   │ • Real-time UI  │    │ • API Endpoints │    │ • Row Level Sec │
   └─────────────────┘    └─────────────────┘    └─────────────────┘

**Core Components:**

- **app_supabase.py**: Main Flask application with routes and WebSocket handlers
- **models_supabase.py**: Game logic, database models, and business rules  
- **auth_supabase.py**: User authentication and session management
- **ai_system.py**: AI opponents and automated gameplay
- **supabase_config.py**: Database configuration and connection management

Development Status
==================

Empire Builder is actively developed with the following components:

✅ **Completed Features:**
   - User registration and authentication
   - Basic empire management
   - Real-time WebSocket communication
   - Supabase database integration
   - Battle system foundation

🚧 **In Development:**
   - Advanced combat mechanics
   - Alliance system
   - Technology research trees
   - Enhanced UI/UX

📋 **Planned Features:**
   - Mobile responsive design
   - Advanced AI opponents
   - Tournament system
   - Mod support

Getting Help
============

- **Documentation**: Browse the sections in this documentation
- **Issues**: Report bugs and request features on GitHub
- **Development**: See the development guide for contributing

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`