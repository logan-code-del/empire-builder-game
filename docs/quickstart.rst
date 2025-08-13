Quick Start Guide
=================

Get Empire Builder up and running in just a few minutes!

Prerequisites
-------------

Before you begin, ensure you have:

- **Python 3.11 or higher** installed
- **Git** for cloning the repository
- **Internet connection** for Supabase integration
- A **Supabase account** (free tier available)

Step 1: Installation
--------------------

1. **Clone the Repository**

   .. code-block:: bash

      git clone https://github.com/your-username/strategic-pro.git
      cd strategic-pro/empire

2. **Install Dependencies**

   .. code-block:: bash

      pip install -r requirements.txt

   This installs all required packages including Flask, Supabase client, and other dependencies.

Step 2: Supabase Setup
----------------------

1. **Create a Supabase Project**

   - Go to https://supabase.com
   - Sign up for a free account
   - Create a new project
   - Wait for the project to be ready (usually 1-2 minutes)

2. **Get Your Credentials**

   From your Supabase dashboard:
   - Go to Settings → API
   - Copy your **Project URL**
   - Copy your **anon/public key**
   - Copy your **service_role key**

3. **Set Up Database Schema**

   In your Supabase dashboard:
   - Go to SQL Editor
   - Run the schema from ``supabase_auth_schema_uuid.sql``

   .. code-block:: sql

      -- This creates the necessary tables for users, empires, battles, etc.
      -- The file contains all required table definitions

Step 3: Configuration
---------------------

1. **Create Environment File**

   Copy the template and add your credentials:

   .. code-block:: bash

      cp .env.template .env

2. **Edit .env File**

   Open ``.env`` in your text editor and add your Supabase credentials:

   .. code-block:: bash

      # Supabase Configuration
      SUPABASE_URL=https://your-project-id.supabase.co
      SUPABASE_ANON_KEY=your-anon-key-here
      SUPABASE_SERVICE_KEY=your-service-key-here
      SECRET_KEY=your-flask-secret-key-here

   **Important**: Replace the placeholder values with your actual Supabase credentials.

Step 4: Launch the Game
-----------------------

1. **Start the Server**

   .. code-block:: bash

      python app_supabase.py

   You should see output similar to:

   .. code-block:: text

      Supabase connected successfully
      * Running on http://127.0.0.1:5000
      * Debug mode: on

2. **Open Your Browser**

   Navigate to: http://localhost:5000

3. **Create Your Account**

   - Click "Register" to create a new account
   - Fill in username, email, and password
   - Click "Create Account"

4. **Start Playing!**

   - Log in with your new account
   - Create your first empire
   - Begin building and expanding

First Steps in the Game
-----------------------

Once you're logged in and have created an empire:

1. **Build Your First City**
   - Click "Build City" on the dashboard
   - Choose a location on the map
   - Start with basic buildings (houses, farms)

2. **Manage Resources**
   - Monitor your gold, food, and materials
   - Build resource-generating buildings
   - Balance production and consumption

3. **Train Units**
   - Build military buildings (barracks, stables)
   - Train basic units (soldiers, archers)
   - Prepare for defense and expansion

4. **Explore Multiplayer**
   - View other players on the leaderboard
   - Send diplomatic messages
   - Consider forming alliances

Troubleshooting
---------------

**Common Issues:**

**"Supabase connection failed"**
   - Check your internet connection
   - Verify your Supabase credentials in ``.env``
   - Ensure your Supabase project is active

**"Registration failed" or 400 errors**
   - Make sure you've run the database schema
   - Check that your service key has proper permissions
   - Verify Row Level Security policies are set up correctly

**"Port already in use"**
   - Another application is using port 5000
   - Kill the existing process or change the port:

   .. code-block:: bash

      python app_supabase.py --port 5001

**Import errors**
   - Ensure you're in the ``empire`` directory
   - Reinstall dependencies: ``pip install -r requirements.txt``
   - Check Python version: ``python --version``

**Database connection issues**
   - Verify your ``.env`` file has the correct credentials
   - Check Supabase project status in the dashboard
   - Ensure your IP is not blocked by Supabase

Getting Help
------------

If you encounter issues:

1. **Check the logs** in your terminal for error messages
2. **Review the installation guide** for detailed setup instructions
3. **Test your setup** using the debug scripts in the project
4. **Report bugs** on the project's GitHub issues page

Next Steps
----------

Now that you have Empire Builder running:

- **Read the Game Mechanics** guide to understand gameplay
- **Explore the API Reference** for advanced features  
- **Check the Development Guide** if you want to contribute
- **Join the community** to connect with other players

Congratulations! You're now ready to build your empire! 🏰