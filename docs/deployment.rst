Deployment Guide
================

This guide covers deploying Empire Builder to various platforms, from development to production environments.

Deployment Options
------------------

Platform Comparison
~~~~~~~~~~~~~~~~~~~

**Render (Recommended)**
- ✅ Free tier available
- ✅ Automatic deployments from Git
- ✅ Built-in SSL certificates
- ✅ Environment variable management
- ✅ PostgreSQL add-on available

**Heroku**
- ✅ Easy deployment process
- ✅ Add-on ecosystem
- ❌ No free tier (as of 2022)
- ✅ Excellent documentation

**Railway**
- ✅ Modern deployment platform
- ✅ Git-based deployments
- ✅ Competitive pricing
- ✅ Good performance

**DigitalOcean App Platform**
- ✅ Scalable infrastructure
- ✅ Multiple deployment options
- ✅ Integrated monitoring
- ❌ More complex setup

**Self-hosted (VPS)**
- ✅ Full control
- ✅ Cost-effective for scale
- ❌ Requires system administration
- ❌ Manual security updates

Render Deployment
-----------------

Render is the recommended platform for Empire Builder deployment due to its simplicity and Supabase compatibility.

Prerequisites
~~~~~~~~~~~~~

1. **Render Account**: Sign up at https://render.com
2. **GitHub Repository**: Code must be in a Git repository
3. **Supabase Project**: Production database ready

Step-by-Step Deployment
~~~~~~~~~~~~~~~~~~~~~~~

1. **Prepare Repository**

   Create ``render.yaml`` in the empire directory:

   .. code-block:: yaml

      services:
        - type: web
          name: empire-builder
          env: python
          buildCommand: pip install -r requirements.txt
          startCommand: gunicorn -w 4 -b 0.0.0.0:$PORT app_supabase:app
          envVars:
            - key: PYTHON_VERSION
              value: 3.11.0
            - key: SUPABASE_URL
              sync: false
            - key: SUPABASE_ANON_KEY
              sync: false
            - key: SUPABASE_SERVICE_KEY
              sync: false
            - key: SECRET_KEY
              generateValue: true

2. **Update Requirements**

   Add production dependencies to ``requirements.txt``:

   .. code-block:: text

      # Existing dependencies
      Flask==2.2.5
      supabase==1.0.4
      flask-socketio==5.3.4
      python-dotenv==1.0.0
      
      # Production dependencies
      gunicorn==21.2.0
      psycopg2-binary==2.9.7

3. **Configure Application**

   Update ``app_supabase.py`` for production:

   .. code-block:: python

      import os
      from flask import Flask
      from dotenv import load_dotenv

      # Load environment variables
      load_dotenv(override=True)

      app = Flask(__name__)
      
      # Production configuration
      app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
      app.config['DEBUG'] = os.environ.get('DEBUG', 'False').lower() == 'true'
      
      # Get port from environment (Render sets this)
      port = int(os.environ.get('PORT', 5000))
      
      if __name__ == '__main__':
          app.run(host='0.0.0.0', port=port)

4. **Create Render Service**

   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the empire directory (if monorepo)
   - Choose "Python" environment
   - Set build command: ``pip install -r requirements.txt``
   - Set start command: ``gunicorn -w 4 -b 0.0.0.0:$PORT app_supabase:app``

5. **Configure Environment Variables**

   In Render dashboard, add environment variables:

   .. code-block:: text

      SUPABASE_URL=https://your-project.supabase.co
      SUPABASE_ANON_KEY=your-anon-key
      SUPABASE_SERVICE_KEY=your-service-key
      SECRET_KEY=your-production-secret-key-very-long-and-random
      DEBUG=False

6. **Deploy**

   - Click "Create Web Service"
   - Render will automatically build and deploy
   - Monitor build logs for any issues
   - Access your app at the provided URL

Production Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

**Environment Variables:**

.. code-block:: bash

   # Required
   SUPABASE_URL=https://your-prod-project.supabase.co
   SUPABASE_ANON_KEY=your-production-anon-key
   SUPABASE_SERVICE_KEY=your-production-service-key
   SECRET_KEY=very-long-random-production-secret-key
   
   # Optional
   DEBUG=False
   PORT=5000
   WORKERS=4

**Gunicorn Configuration:**

Create ``gunicorn.conf.py``:

.. code-block:: python

   import os

   # Server socket
   bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
   backlog = 2048

   # Worker processes
   workers = int(os.environ.get('WORKERS', 4))
   worker_class = "gevent"
   worker_connections = 1000
   timeout = 30
   keepalive = 2

   # Logging
   accesslog = "-"
   errorlog = "-"
   loglevel = "info"

   # Process naming
   proc_name = "empire-builder"

   # Server mechanics
   preload_app = True
   daemon = False
   pidfile = "/tmp/gunicorn.pid"
   user = None
   group = None
   tmp_upload_dir = None

Heroku Deployment
-----------------

Alternative deployment to Heroku platform.

Prerequisites
~~~~~~~~~~~~~

1. **Heroku Account**: Sign up at https://heroku.com
2. **Heroku CLI**: Install from https://devcenter.heroku.com/articles/heroku-cli

Deployment Steps
~~~~~~~~~~~~~~~~

1. **Create Heroku App**

   .. code-block:: bash

      # Login to Heroku
      heroku login

      # Create app
      heroku create empire-builder-yourname

2. **Configure Buildpack**

   .. code-block:: bash

      heroku buildpacks:set heroku/python

3. **Create Procfile**

   Create ``Procfile`` in empire directory:

   .. code-block:: text

      web: gunicorn -w 4 -b 0.0.0.0:$PORT app_supabase:app
      worker: python worker.py  # If you have background tasks

4. **Set Environment Variables**

   .. code-block:: bash

      heroku config:set SUPABASE_URL=https://your-project.supabase.co
      heroku config:set SUPABASE_ANON_KEY=your-anon-key
      heroku config:set SUPABASE_SERVICE_KEY=your-service-key
      heroku config:set SECRET_KEY=your-production-secret-key-very-long-and-random

5. **Deploy**

   .. code-block:: bash

      # Add Heroku remote
      heroku git:remote -a empire-builder-yourname

      # Deploy
      git push heroku main

Docker Deployment
-----------------

Containerized deployment for any platform supporting Docker.

Dockerfile
~~~~~~~~~~

Create ``Dockerfile`` in empire directory:

.. code-block:: dockerfile

   FROM python:3.11-slim

   # Set working directory
   WORKDIR /app

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       gcc \
       && rm -rf /var/lib/apt/lists/*

   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application code
   COPY . .

   # Create non-root user
   RUN useradd --create-home --shell /bin/bash app \
       && chown -R app:app /app
   USER app

   # Expose port
   EXPOSE 5000

   # Health check
   HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
       CMD curl -f http://localhost:5000/health || exit 1

   # Start application
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app_supabase:app"]

Docker Compose
~~~~~~~~~~~~~~

For local development with Docker:

.. code-block:: yaml

   version: '3.8'

   services:
     web:
       build: .
       ports:
         - "5000:5000"
       environment:
         - SUPABASE_URL=${SUPABASE_URL}
         - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
         - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
         - SECRET_KEY=${SECRET_KEY}
         - DEBUG=True
       volumes:
         - .:/app
       depends_on:
         - redis

     redis:
       image: redis:7-alpine
       ports:
         - "6379:6379"

Build and Run
~~~~~~~~~~~~~

.. code-block:: bash

   # Build image
   docker build -t empire-builder .

   # Run container
   docker run -p 5000:5000 \
     -e SUPABASE_URL=your-url \
     -e SUPABASE_ANON_KEY=your-key \
     -e SUPABASE_SERVICE_KEY=your-service-key \
     -e SECRET_KEY=your-secret \
     empire-builder

   # Or use docker-compose
   docker-compose up

Self-Hosted Deployment
----------------------

Deploy on your own VPS or dedicated server.

Server Setup (Ubuntu 20.04+)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Update System**

   .. code-block:: bash

      sudo apt update && sudo apt upgrade -y

2. **Install Dependencies**

   .. code-block:: bash

      # Python and pip
      sudo apt install python3.11 python3.11-pip python3.11-venv -y

      # Nginx (reverse proxy)
      sudo apt install nginx -y

      # Supervisor (process management)
      sudo apt install supervisor -y

      # SSL certificates
      sudo apt install certbot python3-certbot-nginx -y

3. **Create Application User**

   .. code-block:: bash

      sudo useradd --system --shell /bin/bash --home /opt/empire empire
      sudo mkdir -p /opt/empire
      sudo chown empire:empire /opt/empire

4. **Deploy Application**

   .. code-block:: bash

      # Switch to app user
      sudo -u empire -i

      # Clone repository
      cd /opt/empire
      git clone https://github.com/logan-code-del/empire-builder-game.git
      cd empire-builder-game

      # Create virtual environment
      python3.11 -m venv venv
      source venv/bin/activate

      # Install dependencies
      pip install -r requirements.txt

      # Configure environment
      cp .env.template .env
      # Edit .env with production values

Nginx Configuration
~~~~~~~~~~~~~~~~~~~

Create ``/etc/nginx/sites-available/empire-builder``:

.. code-block:: nginx

   server {
       listen 80;
       server_name empire-builder.onrender.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /socket.io/ {
           proxy_pass http://127.0.0.1:5000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }

Enable the site:

.. code-block:: bash

   sudo ln -s /etc/nginx/sites-available/empire-builder /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx

Supervisor Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

Create ``/etc/supervisor/conf.d/empire-builder.conf``:

.. code-block:: ini

   [program:empire-builder]
   command=/opt/empire/strategic-pro/empire/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app_supabase:app
   directory=/opt/empire/strategic-pro/empire
   user=empire
   autostart=true
   autorestart=true
   redirect_stderr=true
   stdout_logfile=/var/log/empire-builder.log
   environment=PATH="/opt/empire/strategic-pro/empire/venv/bin"

Start the service:

.. code-block:: bash

   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start empire-builder

SSL Certificate
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Get SSL certificate
   sudo certbot --nginx -d empire-builder.onrender.com

   # Auto-renewal (add to crontab)
   sudo crontab -e
   # Add: 0 12 * * * /usr/bin/certbot renew --quiet

Monitoring and Maintenance
--------------------------

Health Checks
~~~~~~~~~~~~~

Add health check endpoint to ``app_supabase.py``:

.. code-block:: python

   @app.route('/health')
   def health_check():
       """Health check endpoint for monitoring."""
       try:
           # Test database connection
           result = supabase_config.get_supabase_client().table('users').select('count').limit(1).execute()
           
           return jsonify({
               'status': 'healthy',
               'timestamp': datetime.now().isoformat(),
               'database': 'connected' if result.data else 'disconnected'
           }), 200
       except Exception as e:
           return jsonify({
               'status': 'unhealthy',
               'error': str(e),
               'timestamp': datetime.now().isoformat()
           }), 503

Logging Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from logging.handlers import RotatingFileHandler

   if not app.debug:
       # File logging
       file_handler = RotatingFileHandler(
           'logs/empire.log', 
           maxBytes=10240000, 
           backupCount=10
       )
       file_handler.setFormatter(logging.Formatter(
           '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
       ))
       file_handler.setLevel(logging.INFO)
       app.logger.addHandler(file_handler)
       
       app.logger.setLevel(logging.INFO)
       app.logger.info('Empire Builder startup')

Backup Strategy
~~~~~~~~~~~~~~~

**Database Backups:**
Supabase provides automatic backups, but you can also create manual backups:

.. code-block:: bash

   # Create backup script
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   pg_dump $DATABASE_URL > backups/empire_backup_$DATE.sql
   
   # Compress and upload to cloud storage
   gzip backups/empire_backup_$DATE.sql
   aws s3 cp backups/empire_backup_$DATE.sql.gz s3://your-backup-bucket/

**Application Backups:**

.. code-block:: bash

   # Backup application files
   tar -czf empire_app_backup_$(date +%Y%m%d).tar.gz \
     --exclude=venv \
     --exclude=__pycache__ \
     --exclude=.git \
     /opt/empire/strategic-pro/empire

Performance Optimization
------------------------

Application Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

**Caching:**

.. code-block:: python

   from flask_caching import Cache

   cache = Cache(app, config={'CACHE_TYPE': 'redis'})

   @cache.cached(timeout=300)
   def get_leaderboard():
       """Cached leaderboard data."""
       # Expensive database query
       return leaderboard_data

**Database Connection Pooling:**

.. code-block:: python

   # Configure connection pooling in supabase_config.py
   def create_client_with_pooling():
       return create_client(
           url=SUPABASE_URL,
           key=SUPABASE_KEY,
           options=ClientOptions(
               postgrest_client_timeout=10,
               storage_client_timeout=10
           )
       )

**Static File Optimization:**

.. code-block:: nginx

   # In Nginx configuration
   location /static/ {
       alias /opt/empire/strategic-pro/empire/static/;
       expires 1y;
       add_header Cache-Control "public, immutable";
       gzip_static on;
   }

Security Considerations
-----------------------

Application Security
~~~~~~~~~~~~~~~~~~~~

**Environment Variables:**
- Never commit secrets to version control
- Use different keys for each environment
- Rotate keys regularly

**HTTPS Enforcement:**

.. code-block:: python

   from flask_talisman import Talisman

   # Force HTTPS in production
   if not app.debug:
       Talisman(app, force_https=True)

**Rate Limiting:**

.. code-block:: python

   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address

   limiter = Limiter(
       app,
       key_func=get_remote_address,
       default_limits=["200 per day", "50 per hour"]
   )

   @app.route('/api/login', methods=['POST'])
   @limiter.limit("5 per minute")
   def login():
       # Login logic

Server Security
~~~~~~~~~~~~~~~

**Firewall Configuration:**

.. code-block:: bash

   # UFW firewall setup
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw allow ssh
   sudo ufw allow 'Nginx Full'
   sudo ufw enable

**Automatic Updates:**

.. code-block:: bash

   # Install unattended-upgrades
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure -plow unattended-upgrades

**Fail2Ban:**

.. code-block:: bash

   # Install fail2ban
   sudo apt install fail2ban

   # Configure for Nginx
   sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
   # Edit jail.local to enable nginx protection

Troubleshooting
---------------

Common Deployment Issues
~~~~~~~~~~~~~~~~~~~~~~~~

**Build Failures:**
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Review build logs for specific errors

**Runtime Errors:**
- Check environment variables are set
- Verify database connectivity
- Review application logs

**Performance Issues:**
- Monitor resource usage
- Check database query performance
- Implement caching where appropriate

**SSL Certificate Issues:**
- Verify domain DNS settings
- Check certificate expiration
- Ensure port 80 is accessible for renewal

This comprehensive deployment guide covers all major deployment scenarios for Empire Builder, from simple cloud deployments to complex self-hosted setups.