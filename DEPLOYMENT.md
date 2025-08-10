# Empire Builder - Deployment Guide

This guide will help you deploy Empire Builder to various platforms so people can play online.

## 🚀 Quick Deploy Options

### Option 1: Heroku (Recommended - Free Tier Available)

#### Prerequisites
- GitHub account
- Heroku account (free at heroku.com)
- Git installed on your computer

#### Steps

1. **Prepare the Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Empire Builder game"
   ```

2. **Create GitHub Repository**
   - Go to github.com and create a new repository
   - Name it something like "empire-builder-game"
   - Push your code:
   ```bash
   git remote add origin https://github.com/yourusername/empire-builder-game.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy to Heroku**
   - Go to heroku.com and create a new app
   - Connect your GitHub repository
   - Enable automatic deploys
   - Click "Deploy Branch"

4. **Set Environment Variables** (Optional but recommended)
   - In Heroku dashboard, go to Settings > Config Vars
   - Add: `SECRET_KEY` = `your-secret-key-here`
   - Add: `FLASK_ENV` = `production`

### Option 2: Railway (Modern Alternative)

1. **Push to GitHub** (same as above)
2. **Go to railway.app**
3. **Connect GitHub repository**
4. **Deploy automatically**

### Option 3: Render (Free Tier)

1. **Push to GitHub** (same as above)
2. **Go to render.com**
3. **Create new Web Service**
4. **Connect GitHub repository**
5. **Use these settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

## 🔧 Local Development Setup

### For Contributors

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/empire-builder-game.git
   cd empire-builder-game
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python app.py
   ```

4. **Open browser**
   - Go to `http://localhost:5000`

## 📁 Project Structure

```
empire-builder-game/
├── app.py                 # Main Flask application
├── models.py             # Game models and database
├── ai_system.py          # AI opponent system
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment config
├── runtime.txt          # Python version for deployment
├── README.md            # Project documentation
├── .gitignore           # Git ignore rules
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── military.html
│   ├── cities.html
│   ├── world_map.html
│   └── create_empire.html
└── docs/                # Additional documentation
    ├── CITIES_AND_BUILDINGS.md
    ├── HELP_SYSTEM.md
    └── DEPLOYMENT.md
```

## 🌐 Environment Variables

### Required for Production
- `SECRET_KEY`: Flask secret key for sessions
- `PORT`: Port number (automatically set by most platforms)

### Optional
- `FLASK_ENV`: Set to `production` for production deployment
- `DATABASE_URL`: If using external database (SQLite is default)

## 🔒 Security Considerations

### For Production Deployment

1. **Change Secret Key**
   - Generate a secure secret key
   - Set as environment variable
   - Never commit secrets to Git

2. **Database Security**
   - Consider using PostgreSQL for production
   - Enable database backups
   - Use connection pooling for high traffic

3. **CORS Configuration**
   - Update CORS settings for your domain
   - Remove wildcard (*) in production

## 📊 Performance Optimization

### For High Traffic

1. **Database Optimization**
   ```python
   # Consider switching to PostgreSQL
   # Add database connection pooling
   # Implement caching for frequent queries
   ```

2. **Static File Serving**
   - Use CDN for static assets
   - Enable gzip compression
   - Implement browser caching

3. **Scaling Options**
   - Use multiple worker processes
   - Implement Redis for session storage
   - Consider load balancing

## 🐛 Troubleshooting

### Common Deployment Issues

1. **Port Binding Error**
   - Ensure app uses `PORT` environment variable
   - Check Procfile configuration

2. **Database Issues**
   - SQLite works for small deployments
   - Consider PostgreSQL for production
   - Check file permissions

3. **Static Files Not Loading**
   - Verify template paths
   - Check static file configuration
   - Ensure all files are committed to Git

### Debug Mode

For development, set environment variable:
```bash
export FLASK_ENV=development
```

## 📈 Monitoring and Analytics

### Recommended Tools

1. **Application Monitoring**
   - Heroku metrics (built-in)
   - New Relic (free tier)
   - Sentry for error tracking

2. **User Analytics**
   - Google Analytics
   - Simple visitor counters
   - Game statistics tracking

## 🎮 Game Features for Online Play

### Current Features
- ✅ Real-time multiplayer battles
- ✅ Persistent game state
- ✅ AI opponents
- ✅ Cities and buildings system
- ✅ Resource management
- ✅ World map interaction

### Recommended Enhancements for Online
- [ ] User registration/login system
- [ ] Leaderboards
- [ ] Chat system
- [ ] Tournament modes
- [ ] Alliance system
- [ ] Email notifications

## 🚀 Go Live Checklist

### Before Deployment
- [ ] Test all game features locally
- [ ] Update README with live URL
- [ ] Set production environment variables
- [ ] Test database migrations
- [ ] Verify all templates load correctly

### After Deployment
- [ ] Test game functionality on live site
- [ ] Monitor error logs
- [ ] Test multiplayer features
- [ ] Share with friends for beta testing
- [ ] Update documentation with live URL

## 🎯 Next Steps

1. **Deploy to your preferred platform**
2. **Test the live game thoroughly**
3. **Share the URL with friends**
4. **Monitor usage and performance**
5. **Consider additional features based on feedback**

## 📞 Support

If you encounter issues during deployment:

1. Check the platform-specific documentation
2. Review error logs in the deployment dashboard
3. Test locally first to isolate issues
4. Check GitHub Issues for common problems

---

**Ready to conquer the world online!** 🌍⚔️👑

Your Empire Builder game is now ready for global domination!