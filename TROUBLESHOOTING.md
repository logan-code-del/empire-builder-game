# Empire Builder - Troubleshooting Guide

## Common Issues and Solutions

### 1. Template Errors

**Error**: `jinja2.exceptions.TemplateAssertionError: No filter named 'tojsonfilter'`
**Solution**: ✅ **FIXED** - Changed `tojsonfilter` to `tojson` in all templates:
- ✅ military.html - Fixed
- ✅ world_map.html - Fixed (3 occurrences)
- ✅ All other templates - Verified clean

**Error**: Template not found
**Solution**: Ensure all template files are in the `templates/` directory:
- `base.html`
- `index.html` 
- `create_empire.html`
- `dashboard.html`
- `world_map.html`
- `military.html`

### 2. Import Errors

**Error**: `ImportError: cannot import name 'GameDatabase' from 'app'`
**Solution**: ✅ **FIXED** - Moved models to separate `models.py` file to avoid circular imports

**Error**: `ModuleNotFoundError: No module named 'flask'`
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Database Issues

**Error**: Database file not found or corrupted
**Solution**: Delete `empire_game.db` file - it will be recreated automatically

**Error**: SQLite errors
**Solution**: Check file permissions and ensure the directory is writable

### 4. Port/Network Issues

**Error**: `Address already in use`
**Solution**: 
- Kill existing Flask processes
- Change port in `app.py`: `socketio.run(app, port=5001)`

**Error**: Cannot access from other devices
**Solution**: The app runs on `0.0.0.0` so it should be accessible from other devices on your network at `http://YOUR_IP:5000`

### 5. JavaScript Errors

**Error**: `formatNumber is not defined`
**Solution**: ✅ **FIXED** - Function is defined in `base.html`

**Error**: Socket.IO connection issues
**Solution**: Check that Socket.IO CDN is accessible and Flask-SocketIO is installed

### 6. AI System Issues

**Error**: AI not making moves
**Solution**: Check that `initialize_ai_system()` is called and AI thread is running

**Error**: Circular import with AI system
**Solution**: ✅ **FIXED** - AI system imports from `models.py` instead of `app.py`

## Quick Fixes

### Reset Game State
```bash
# Delete database to start fresh
rm empire_game.db
python app.py
```

### Reinstall Dependencies
```bash
pip uninstall Flask Flask-SocketIO Werkzeug -y
pip install -r requirements.txt
```

### Check Server Status
```bash
# Test if server is running
curl http://localhost:5000
# or
python test_game.py
```

## File Structure Check

Ensure your directory structure looks like this:
```
empire/
├── app.py                 # Main Flask application
├── models.py             # Game models and database
├── ai_system.py          # AI opponents
├── requirements.txt      # Dependencies
├── test_game.py         # Tests
├── start_game.py        # Simple launcher
├── demo.py              # Interactive demo
├── empire_game.db       # SQLite database (auto-created)
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── create_empire.html
│   ├── dashboard.html
│   ├── world_map.html
│   └── military.html
└── README.md
```

## Performance Tips

1. **Database**: SQLite is fine for single-player/small multiplayer. For larger games, consider PostgreSQL
2. **Real-time**: Socket.IO handles real-time updates efficiently
3. **AI**: AI runs in background threads and checks every 30 seconds
4. **Resources**: Resource generation happens every 60 seconds

## Development Mode

The app runs in debug mode by default. For production:
1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn
3. Set up proper database backups
4. Configure proper logging

## Getting Help

1. Check the console output for error messages
2. Run `python test_game.py` to verify core functionality
3. Check browser developer tools for JavaScript errors
4. Ensure all dependencies are installed correctly

## Current Status: ✅ WORKING

All major issues have been resolved:
- ✅ Template errors fixed
- ✅ Import errors resolved  
- ✅ Database working
- ✅ AI system functional
- ✅ Web interface operational
- ✅ Real-time features active

The game should be fully playable at http://localhost:5000