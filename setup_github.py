#!/usr/bin/env python3
"""
Empire Builder - GitHub Setup Script
Helps prepare the project for GitHub and deployment
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def check_git_installed():
    """Check if Git is installed"""
    return run_command("git --version", "Checking Git installation")

def initialize_git_repo():
    """Initialize Git repository"""
    if not os.path.exists('.git'):
        return run_command("git init", "Initializing Git repository")
    else:
        print("✅ Git repository already initialized")
        return True

def create_gitignore():
    """Ensure .gitignore exists"""
    if os.path.exists('.gitignore'):
        print("✅ .gitignore already exists")
        return True
    else:
        print("❌ .gitignore not found - please create one")
        return False

def add_files_to_git():
    """Add files to Git"""
    commands = [
        ("git add .", "Adding files to Git"),
        ("git commit -m 'Initial commit - Empire Builder game ready for GitHub'", "Creating initial commit")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'models.py', 
        'requirements.txt',
        'README.md',
        'LICENSE',
        'Procfile',
        'runtime.txt',
        'app.json',
        '.gitignore'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            missing_files.append(file)
    
    return len(missing_files) == 0, missing_files

def display_next_steps():
    """Display next steps for GitHub setup"""
    print("\n" + "="*60)
    print("🎉 EMPIRE BUILDER - GITHUB SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 NEXT STEPS:")
    print("1. Create GitHub Repository:")
    print("   - Go to https://github.com/new")
    print("   - Name: empire-builder-game")
    print("   - Description: Strategic conquest game with cities and real-time combat")
    print("   - Make it public")
    print("   - Don't initialize with README (we have one)")
    
    print("\n2. Connect Local Repository to GitHub:")
    print("   git remote add origin https://github.com/yourusername/empire-builder-game.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    
    print("\n3. Deploy to Heroku (One-Click):")
    print("   - Click the 'Deploy to Heroku' button in your README")
    print("   - Or go to: https://heroku.com/deploy?template=https://github.com/yourusername/empire-builder-game")
    
    print("\n4. Alternative Deployment Options:")
    print("   - Railway: https://railway.app")
    print("   - Render: https://render.com")
    print("   - See DEPLOYMENT.md for detailed instructions")
    
    print("\n5. Update README:")
    print("   - Replace 'yourusername' with your GitHub username")
    print("   - Replace 'your-deployed-url-here' with your actual deployment URL")
    print("   - Add screenshots of your game")
    
    print("\n🎮 FEATURES READY FOR GITHUB:")
    print("✅ Complete game with cities and buildings")
    print("✅ Real-time multiplayer combat")
    print("✅ AI opponents")
    print("✅ Responsive web design")
    print("✅ Deployment-ready configuration")
    print("✅ Comprehensive documentation")
    print("✅ MIT License")
    print("✅ GitHub Actions workflow")
    
    print("\n🚀 DEPLOYMENT FEATURES:")
    print("✅ Heroku one-click deploy button")
    print("✅ Environment variable configuration")
    print("✅ Production-ready settings")
    print("✅ Database migration support")
    print("✅ Automatic dependency installation")
    
    print("\n📚 DOCUMENTATION:")
    print("✅ README.md - Main project documentation")
    print("✅ DEPLOYMENT.md - Deployment guide")
    print("✅ CITIES_AND_BUILDINGS.md - Game features guide")
    print("✅ LICENSE - MIT License")
    
    print("\n" + "="*60)
    print("🌍 READY TO CONQUER THE WORLD!")
    print("Your Empire Builder game is ready for GitHub and deployment!")
    print("="*60)

def main():
    """Main setup function"""
    print("🏰 Empire Builder - GitHub Setup")
    print("="*50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this script from the Empire Builder directory.")
        sys.exit(1)
    
    # Check required files
    print("\n📁 Checking required files...")
    files_ok, missing = check_required_files()
    if not files_ok:
        print(f"\n❌ Missing required files: {', '.join(missing)}")
        print("Please ensure all files are created before running this script.")
        sys.exit(1)
    
    # Check Git installation
    if not check_git_installed():
        print("\n❌ Git is not installed. Please install Git first:")
        print("   Windows: https://git-scm.com/download/win")
        print("   Mac: brew install git")
        print("   Linux: sudo apt-get install git")
        sys.exit(1)
    
    # Initialize Git repository
    if not initialize_git_repo():
        sys.exit(1)
    
    # Add files to Git
    print("\n📦 Adding files to Git repository...")
    if not add_files_to_git():
        print("⚠️ Some Git operations failed, but you can continue manually")
    
    # Display next steps
    display_next_steps()

if __name__ == "__main__":
    main()