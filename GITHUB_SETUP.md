# 🚀 Empire Builder - GitHub Setup Guide

This guide will walk you through getting your Empire Builder game on GitHub and deployed online so people can play it!

## 📋 Prerequisites

Before starting, make sure you have:
- [x] Git installed on your computer
- [x] A GitHub account (free at github.com)
- [x] Your Empire Builder game working locally

## 🎯 Quick Setup (5 Minutes)

### Step 1: Run the Setup Script
```bash
python setup_github.py
```

This script will:
- ✅ Check all required files exist
- ✅ Initialize Git repository
- ✅ Add files and create initial commit
- ✅ Display next steps

### Step 2: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Repository Name**: `empire-builder-game`
3. **Description**: `Strategic conquest game with cities, buildings, and real-time combat`
4. **Visibility**: Public (so people can play it!)
5. **Initialize**: Don't check any boxes (we have our own files)
6. **Click**: "Create repository"

### Step 3: Connect Your Local Code to GitHub

Copy and paste these commands (replace `yourusername` with your GitHub username):

```bash
git remote add origin https://github.com/yourusername/empire-builder-game.git
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Render (Easy Setup!)

1. **Update your README**: Replace `yourusername` with your actual GitHub username
2. **Go to Render**: https://render.com
3. **Sign up/Login** with your GitHub account
4. **Create Web Service**: Click "New +" → "Web Service"
5. **Connect Repository**: Select your empire-builder-game repository
6. **Configure Settings**:
   - Name: `empire-builder`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
7. **Deploy**: Click "Create Web Service"

That's it! Your game will be live in 2-3 minutes! 🎉

## 🔧 Manual Setup (If You Prefer)

### 1. Initialize Git Repository

```bash
# Navigate to your Empire Builder directory
cd path/to/empire-builder

# Initialize Git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit - Empire Builder game"
```

### 2. Create .gitignore (Already Done!)

The `.gitignore` file is already created and includes:
- Python cache files
- Database files (for security)
- Test files
- IDE files
- Environment variables

### 3. Prepare for Deployment

All deployment files are ready:
- ✅ `Procfile` - Tells Heroku how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `app.json` - One-click deploy configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ Environment variable support in `app.py`

## 🌐 Deployment Options

### Option 1: Render (Recommended)

**Pros**: Free tier, modern platform, easy setup, automatic SSL
**Best for**: Getting started quickly with great performance

1. **Web Interface Deploy**: 
   - Go to render.com
   - Connect GitHub repository
   - Configure and deploy
2. **Automatic Deploys**: Updates automatically when you push to GitHub

### Option 2: Railway

**Pros**: Modern platform, great performance
**Best for**: Long-term hosting

1. Go to https://railway.app
2. Connect your GitHub repository
3. Deploy automatically

### Option 3: Heroku

**Pros**: Well-established platform, lots of documentation
**Best for**: If you prefer traditional PaaS

1. Go to https://heroku.com
2. Create new app
3. Connect GitHub repository
4. Deploy branch

## 📝 Customization Checklist

Before going live, update these files:

### README.md
- [ ] Replace `yourusername` with your GitHub username
- [ ] Replace `your-deployed-url-here` with your actual URL
- [ ] Add screenshots of your game
- [ ] Update contact information

### app.json
- [ ] Update repository URL
- [ ] Change app name if desired
- [ ] Update contact email

### GitHub Actions (.github/workflows/deploy.yml)
- [ ] Update Heroku app name
- [ ] Update email address
- [ ] Add HEROKU_API_KEY to GitHub secrets (if using)

## 🎮 Game Features Ready for GitHub

Your Empire Builder game includes:

### ✅ Core Features
- Complete empire building gameplay
- Real-time multiplayer combat
- Cities and buildings system
- Resource management
- AI opponents
- Interactive world map

### ✅ Technical Features
- Flask web framework
- Socket.IO real-time communication
- SQLite database (PostgreSQL ready)
- Responsive design for mobile/desktop
- Background resource generation
- Session management

### ✅ Deployment Ready
- Environment variable configuration
- Production-ready settings
- Database migration support
- Error handling
- Security considerations

## 🔒 Security & Production

### Environment Variables
Set these in your deployment platform:
- `SECRET_KEY`: Flask session security (auto-generated)
- `FLASK_ENV`: Set to `production`
- `DATABASE_URL`: If using external database

### Database Considerations
- **Development**: SQLite (included)
- **Production**: PostgreSQL recommended for high traffic
- **Heroku**: Automatically provides PostgreSQL

## 📊 Monitoring Your Game

### After Deployment
1. **Test all features** on the live site
2. **Monitor error logs** in your deployment dashboard
3. **Check performance** and response times
4. **Share with friends** for beta testing

### Analytics (Optional)
- Add Google Analytics to track visitors
- Monitor game statistics
- Track popular features

## 🐛 Troubleshooting

### Common Issues

**Port Binding Error**
- ✅ Fixed: App uses `PORT` environment variable

**Database Issues**
- ✅ Fixed: SQLite works for small deployments
- For high traffic: Consider PostgreSQL

**Static Files Not Loading**
- ✅ Fixed: All templates and static files included

**Secret Key Warnings**
- ✅ Fixed: Uses environment variables in production

### Getting Help

1. **Check deployment logs** in your platform dashboard
2. **Test locally first** to isolate issues
3. **Review error messages** carefully
4. **Check GitHub Issues** for common problems

## 🎯 Post-Deployment Checklist

### Immediate (First Hour)
- [ ] Test game creation and login
- [ ] Test building cities and buildings
- [ ] Test military training and combat
- [ ] Test on mobile device
- [ ] Share URL with friends

### Short-term (First Week)
- [ ] Monitor error logs
- [ ] Gather user feedback
- [ ] Fix any reported bugs
- [ ] Consider performance optimizations

### Long-term (First Month)
- [ ] Add user analytics
- [ ] Consider new features based on feedback
- [ ] Optimize database queries if needed
- [ ] Plan marketing and promotion

## 🚀 Success! Your Game is Live!

Once deployed, your Empire Builder game will be accessible to anyone with the URL. Players can:

- 🏰 Create their own empires
- 🏗️ Build cities and buildings
- ⚔️ Engage in real-time combat
- 🌍 Compete on the world map
- 📱 Play on any device

## 📢 Sharing Your Game

### Social Media
- Share on Twitter, Reddit, Discord
- Post in game development communities
- Share with friends and family

### Game Development Communities
- r/gamedev on Reddit
- IndieDB
- Itch.io (if you want to list it there)
- Game development Discord servers

### Example Social Media Post
```
🏰 Just launched Empire Builder - a web-based strategy game!

✨ Features:
- Real-time multiplayer combat
- Cities and buildings system  
- AI opponents
- Works on any device

🎮 Play free at: [your-url-here]
🔧 Open source: [your-github-url]

#gamedev #strategy #webgame #python #flask
```

## 🎉 Congratulations!

You've successfully:
- ✅ Prepared your game for GitHub
- ✅ Set up deployment configuration
- ✅ Created comprehensive documentation
- ✅ Made your game accessible to the world

**Your Empire Builder game is now ready to conquer the internet!** 🌍👑

---

**Need help?** Check the other documentation files:
- 📖 [Game Features](CITIES_AND_BUILDINGS.md)
- 🚀 [Deployment Details](DEPLOYMENT.md)
- 🔧 [Troubleshooting](TROUBLESHOOTING.md)