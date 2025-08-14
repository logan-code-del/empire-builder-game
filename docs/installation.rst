Installation Guide
==================

This comprehensive guide covers all aspects of installing and configuring Empire Builder.

System Requirements
-------------------

**Minimum Requirements:**
- Python 3.11 or higher
- 2GB RAM
- 1GB free disk space
- Internet connection for Supabase

**Recommended:**
- Python 3.11+
- 4GB RAM
- 2GB free disk space
- Stable broadband connection

**Supported Operating Systems:**
- Windows 10/11
- macOS 10.15 (Catalina) or later
- Linux (Ubuntu 20.04+, CentOS 8+, or equivalent)

Installation Methods
--------------------

Method 1: Standard Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Install Python**

   Download Python from https://python.org/downloads/

   **Windows:**
   - Download the installer
   - Check "Add Python to PATH" during installation
   - Verify: ``python --version``

   **macOS:**
   - Use the official installer or Homebrew: ``brew install python@3.11``
   - Verify: ``python3 --version``

   **Linux:**
   
   .. code-block:: bash

      # Ubuntu/Debian
      sudo apt update
      sudo apt install python3.11 python3.11-pip python3.11-venv

      # CentOS/RHEL
      sudo dnf install python3.11 python3.11-pip

2. **Clone the Repository**

   .. code-block:: bash

      git clone https://github.com/logan-code-del/empire-builder-game.git
      cd empire-builder-game

3. **Create Virtual Environment** (Recommended)

   .. code-block:: bash

      # Create virtual environment
      python -m venv empire-env

      # Activate it
      # Windows:
      empire-env\Scripts\activate
      
      # macOS/Linux:
      source empire-env/bin/activate

4. **Install Dependencies**

   .. code-block:: bash

      pip install -r requirements.txt

Method 2: Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For developers who want to contribute:

1. **Fork the Repository** on GitHub

2. **Clone Your Fork**

   .. code-block:: bash

      git clone https://github.com/logan-code-del/empire-builder-game.git
      cd empire-builder-game

3. **Set Up Development Environment**

   .. code-block:: bash

      python -m venv empire-dev-env
      source empire-dev-env/bin/activate  # or empire-dev-env\Scripts\activate on Windows
      
      pip install -r requirements.txt
      pip install -r requirements-dev.txt  # If available

4. **Set Up Pre-commit Hooks** (Optional)

   .. code-block:: bash

      pip install pre-commit
      pre-commit install

Supabase Configuration
----------------------

Empire Builder requires a Supabase project for database and real-time features.

Setting Up Supabase
~~~~~~~~~~~~~~~~~~~~

1. **Create Account**
   - Go to https://supabase.com
   - Sign up for a free account
   - Verify your email address

2. **Create New Project**
   - Click "New Project"
   - Choose your organization
   - Enter project name: "empire-builder"
   - Choose a database password (save this!)
   - Select a region close to your users
   - Click "Create new project"

3. **Wait for Setup**
   - Project creation takes 1-2 minutes
   - You'll see a progress indicator

4. **Get API Credentials**
   - Go to Settings → API
   - Copy the following:
     - Project URL
     - anon/public key
     - service_role key (keep this secret!)

Database Schema Setup
~~~~~~~~~~~~~~~~~~~~~

1. **Access SQL Editor**
   - In your Supabase dashboard
   - Go to SQL Editor
   - Click "New query"

2. **Run Schema Script**

   Copy and paste the contents of ``supabase_auth_schema_uuid.sql``:

   .. code-block:: sql

      -- Users table with UUID primary key
      CREATE TABLE IF NOT EXISTS users (
          id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
          username VARCHAR(50) UNIQUE NOT NULL,
          email VARCHAR(255) UNIQUE NOT NULL,
          password_hash VARCHAR(255) NOT NULL,
          salt VARCHAR(255) NOT NULL,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
          last_login TIMESTAMP WITH TIME ZONE,
          is_active BOOLEAN DEFAULT TRUE,
          empire_id UUID
      );

      -- Additional tables for empires, battles, etc.
      -- (Full schema in the SQL file)

3. **Execute the Query**
   - Click "Run" to create all tables
   - Verify tables appear in the Table Editor

4. **Set Up Row Level Security** (Important!)

   .. code-block:: sql

      -- Enable RLS on users table
      ALTER TABLE users ENABLE ROW LEVEL SECURITY;

      -- Create policies for service role access
      CREATE POLICY "Service role can manage users" ON users
      FOR ALL USING (auth.role() = 'service_role');

Environment Configuration
-------------------------

1. **Create Environment File**

   .. code-block:: bash

      cp .env.template .env

2. **Edit Configuration**

   Open ``.env`` in your preferred text editor:

   .. code-block:: bash

      # Supabase Configuration for Empire Builder
      SUPABASE_URL=https://your-project-id.supabase.co
      SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      
      # Flask Configuration
      SECRET_KEY=your-very-long-random-secret-key-here-change-this-in-production
      DEBUG=True
      PORT=5000

   **Security Notes:**
   - Never commit ``.env`` to version control
   - Use a strong, random SECRET_KEY
   - Keep your service_role key secret

3. **Verify Configuration**

   Test your setup with the debug script:

   .. code-block:: bash

      python debug_registration.py

Verification and Testing
------------------------

1. **Test Database Connection**

   .. code-block:: bash

      python test_simple_connection.py

   Expected output:
   
   .. code-block:: text

      ✅ Basic HTTP works: 200
      ✅ Supabase REST API accessible: 200
      ✅ Supabase client created
      ✅ Query successful

2. **Test Authentication System**

   .. code-block:: bash

      python debug_registration.py

   This will test:
   - Environment variable loading
   - Supabase connection
   - User creation
   - Authentication flow

3. **Launch the Application**

   .. code-block:: bash

      python app_supabase.py

   Expected output:

   .. code-block:: text

      Supabase connected successfully
      * Running on http://127.0.0.1:5000
      * Debug mode: on
      * Restarting with stat
      * Debugger is active!

4. **Test in Browser**
   - Open http://localhost:5000
   - Try registering a new account
   - Test login functionality
   - Verify dashboard access

Troubleshooting
---------------

Common Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Python Version Issues**

.. code-block:: bash

   # Check Python version
   python --version
   
   # If using multiple Python versions
   python3.11 --version
   
   # Use specific version for virtual environment
   python3.11 -m venv empire-env

**Dependency Installation Failures**

.. code-block:: bash

   # Upgrade pip first
   pip install --upgrade pip
   
   # Install with verbose output
   pip install -r requirements.txt -v
   
   # Install individual packages if needed
   pip install flask supabase flask-socketio python-dotenv

**Virtual Environment Issues**

.. code-block:: bash

   # Recreate virtual environment
   rm -rf empire-env  # or rmdir /s empire-env on Windows
   python -m venv empire-env
   source empire-env/bin/activate
   pip install -r requirements.txt

Supabase Connection Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

**"getaddrinfo failed" Error**
- Check internet connection
- Verify Supabase URL is correct
- Try accessing Supabase dashboard in browser

**"Row Level Security" Errors**
- Ensure RLS policies are set up correctly
- Verify service_role key has proper permissions
- Check that tables were created successfully

**Authentication Failures**
- Verify all environment variables are set
- Check for typos in credentials
- Ensure ``.env`` file is in the correct directory

**Database Schema Issues**
- Re-run the schema SQL script
- Check for SQL syntax errors
- Verify all tables were created

Performance Optimization
------------------------

For better performance in production:

1. **Use Production WSGI Server**

   .. code-block:: bash

      pip install gunicorn
      gunicorn -w 4 -b 0.0.0.0:5000 app_supabase:app

2. **Configure Caching**

   .. code-block:: bash

      pip install flask-caching
      # Configure in app_supabase.py

3. **Database Optimization**
   - Add indexes to frequently queried columns
   - Use connection pooling
   - Enable query optimization in Supabase

Security Considerations
-----------------------

**Environment Variables**
- Never commit ``.env`` files
- Use different keys for development/production
- Rotate keys regularly

**Database Security**
- Enable Row Level Security on all tables
- Use least-privilege access patterns
- Regular security audits

**Application Security**
- Keep dependencies updated
- Use HTTPS in production
- Implement rate limiting

Next Steps
----------

After successful installation:

1. **Read the Quick Start Guide** for basic usage
2. **Explore Game Mechanics** to understand gameplay
3. **Check API Reference** for advanced features
4. **Review Development Guide** for contributing

You're now ready to start building your empire! 🏰