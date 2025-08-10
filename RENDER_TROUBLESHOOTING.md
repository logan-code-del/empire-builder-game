# 🔧 Empire Builder - Render Deployment Troubleshooting

Common issues and solutions when deploying Empire Builder to Render.

## 🚨 Common Deployment Issues

### Issue 1: "Werkzeug web server is not designed to run in production"

**Error Message:**
```
RuntimeError: The Werkzeug web server is not designed to run in production. 
Pass allow_unsafe_werkzeug=True to the run() method to disable this error.
```

**✅ Solution:**
This is fixed in the latest version! We now use Gunicorn as the production server.

**What we changed:**
- Added `gunicorn` and `eventlet` to `requirements.txt`
- Created `wsgi.py` for proper WSGI entry point
- Updated `render.yaml` with production start command
- Updated deployment guides with correct commands

**Start Command (use this in Render):**
```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT wsgi:application
```

### Issue 2: Build Fails - Missing Dependencies

**Error Message:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**✅ Solution:**
Make sure your `requirements.txt` includes all dependencies:

```txt
Flask==2.2.5
Flask-SocketIO==5.3.6
Werkzeug==2.2.3
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.2
gunicorn==21.2.0
eventlet==0.33.3
```

### Issue 3: App Starts But Socket.IO Doesn't Work

**Symptoms:**
- App loads but real-time features don't work
- No live updates
- Combat system fails

**✅ Solution:**
Ensure you're using the eventlet worker class:

```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT wsgi:application
```

**Why eventlet?**
- Socket.IO requires async support
- Eventlet provides WebSocket compatibility
- Single worker (`-w 1`) prevents session conflicts

### Issue 4: Database Errors

**Error Message:**
```
sqlite3.OperationalError: database is locked
```

**✅ Solution:**
This is normal for SQLite with multiple workers. Solutions:

1. **Use single worker** (already configured):
   ```bash
   gunicorn --worker-class eventlet -w 1 ...
   ```

2. **Upgrade to PostgreSQL** (for high traffic):
   - Add PostgreSQL service in Render
   - Update database connection in `models.py`

### Issue 5: Static Files Not Loading

**Symptoms:**
- CSS/JS files return 404
- Game interface looks broken

**✅ Solution:**
Flask serves static files automatically. If issues persist:

1. **Check file paths** in templates
2. **Verify static folder** structure
3. **Clear browser cache**

### Issue 6: Environment Variables Not Set

**Error Message:**
```
KeyError: 'SECRET_KEY'
```

**✅ Solution:**
Render should auto-generate environment variables. If not:

1. **Go to Render Dashboard**
2. **Select your service**
3. **Go to Environment tab**
4. **Add variables:**
   - `SECRET_KEY`: Generate a random string
   - `FLASK_ENV`: `production`

## 🔍 Debugging Steps

### Step 1: Check Build Logs

1. **Go to Render Dashboard**
2. **Select your service**
3. **Click on latest deployment**
4. **Review build logs** for errors

### Step 2: Check Runtime Logs

1. **In Render Dashboard**
2. **Go to Logs tab**
3. **Look for runtime errors**
4. **Check for startup messages**

### Step 3: Test Locally

Before deploying, test locally:

```bash
# Install production dependencies
pip install gunicorn eventlet

# Test with Gunicorn locally
gunicorn --worker-class eventlet -w 1 --bind 127.0.0.1:5000 wsgi:application

# Test in browser
# Go to http://localhost:5000
```

### Step 4: Verify Configuration

Check these files are correct:

**render.yaml:**
```yaml
services:
  - type: web
    name: empire-builder
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT wsgi:application
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
    autoDeploy: true
```

**wsgi.py:**
```python
from app import app, socketio
application = socketio
```

## 🚀 Performance Optimization

### For Better Performance on Render

1. **Enable Gzip Compression:**
   ```python
   from flask_compress import Compress
   Compress(app)
   ```

2. **Optimize Database Queries:**
   - Add indexes to frequently queried fields
   - Use connection pooling for PostgreSQL

3. **Cache Static Assets:**
   - Set proper cache headers
   - Use CDN for static files

### Scaling Considerations

**Free Tier Limits:**
- 750 hours/month
- 512 MB RAM
- 0.1 CPU

**When to Upgrade:**
- High concurrent users (>50)
- Database performance issues
- Memory usage consistently high

## 📞 Getting Help

### Render Support

1. **Render Documentation**: https://render.com/docs
2. **Render Community**: Discord/Forums
3. **Support Tickets**: For paid plans

### Empire Builder Support

1. **Check GitHub Issues**: Common problems and solutions
2. **Review Documentation**: Complete guides available
3. **Test Locally First**: Isolate deployment vs code issues

### Useful Commands

**Check service status:**
```bash
curl -I https://your-app.onrender.com
```

**Test Socket.IO connection:**
```javascript
// In browser console
io.connect('https://your-app.onrender.com')
```

**Monitor resource usage:**
- Check Render dashboard metrics
- Monitor response times
- Watch memory usage

## ✅ Deployment Checklist

Before deploying to Render:

- [ ] All files committed to GitHub
- [ ] `requirements.txt` includes gunicorn and eventlet
- [ ] `wsgi.py` file exists and is correct
- [ ] `render.yaml` has correct start command
- [ ] Environment variables configured
- [ ] Tested locally with Gunicorn
- [ ] Database migrations ready (if needed)

After successful deployment:

- [ ] Test all game features
- [ ] Verify real-time functionality
- [ ] Check mobile compatibility
- [ ] Monitor initial performance
- [ ] Share with beta testers

## 🎉 Success!

Once these issues are resolved, your Empire Builder game will be:

- ✅ **Running smoothly** on Render
- ✅ **Production-ready** with Gunicorn
- ✅ **Real-time enabled** with Socket.IO
- ✅ **Globally accessible** to all players
- ✅ **Automatically updating** on GitHub pushes

**Your empire is ready to conquer the web!** 🏰🌍

---

**Still having issues?** 
- Check the main [Deployment Guide](DEPLOYMENT.md)
- Review [Render Deploy Guide](RENDER_DEPLOY.md)
- Test with the [Troubleshooting Guide](TROUBLESHOOTING.md)