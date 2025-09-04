#!/usr/bin/env python3
"""
Startup script for the RAG Web Interface
"""
import os
import sys
import subprocess
import time
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_ollama_running():
    """Check if Ollama is running"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def start_ollama():
    """Start Ollama service"""
    logger.info("Starting Ollama service...")
    try:
        # Try to start Ollama service
        subprocess.run(['brew', 'services', 'start', 'ollama'], check=True)
        time.sleep(3)  # Give it time to start
        
        # Check if it's running
        if check_ollama_running():
            logger.info("✅ Ollama is running")
            return True
        else:
            logger.warning("⚠️  Ollama may not be running properly")
            return False
    except subprocess.CalledProcessError:
        logger.error("❌ Failed to start Ollama service")
        return False

def check_models():
    """Check if required models are available"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            models = result.stdout.lower()
            required_models = ['llama3.2:3b', 'mistral:latest']
            
            missing_models = []
            for model in required_models:
                if model not in models:
                    missing_models.append(model)
            
            if missing_models:
                logger.warning(f"⚠️  Missing models: {', '.join(missing_models)}")
                logger.info("You can install them with:")
                for model in missing_models:
                    logger.info(f"  ollama pull {model}")
                return False
            else:
                logger.info("✅ All required models are available")
                return True
        else:
            logger.error("❌ Failed to check models")
            return False
    except subprocess.TimeoutExpired:
        logger.error("❌ Timeout checking models")
        return False

def check_database():
    """Check if database exists and has documents"""
    chroma_path = Path("chroma")
    if chroma_path.exists():
        logger.info("✅ Database directory exists")
        return True
    else:
        logger.warning("⚠️  Database not found. You may need to populate it first.")
        logger.info("Run: python3 enhanced_populate.py")
        return False

def populate_database():
    """Populate the database if it doesn't exist"""
    logger.info("Populating database...")
    try:
        result = subprocess.run([sys.executable, 'enhanced_populate.py'], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            logger.info("✅ Database populated successfully")
            return True
        else:
            logger.error(f"❌ Failed to populate database: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("❌ Timeout populating database")
        return False

def install_dependencies():
    """Install Python dependencies"""
    logger.info("Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        logger.info("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        return False

def start_web_app():
    """Start the Flask web application"""
    logger.info("Starting web application...")
    try:
        # Set environment variables
        os.environ['FLASK_APP'] = 'app.py'
        os.environ['FLASK_ENV'] = 'development'
        
        # Start the app
        subprocess.run([sys.executable, 'app.py'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to start web app: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("👋 Shutting down...")
        return True

def main():
    """Main startup sequence"""
    print("🚀 Starting RAG Web Interface...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        logger.error("❌ app.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        logger.error("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Check Ollama
    if not check_ollama_running():
        logger.info("Ollama not running, attempting to start...")
        if not start_ollama():
            logger.error("❌ Please start Ollama manually: brew services start ollama")
            sys.exit(1)
    
    # Check models
    if not check_models():
        logger.warning("⚠️  Some models may be missing, but continuing...")
    
    # Check database
    if not check_database():
        logger.info("Database not found, populating...")
        if not populate_database():
            logger.error("❌ Failed to populate database")
            sys.exit(1)
    
    print("=" * 50)
    print("🎉 All checks passed! Starting web interface...")
    print("🌐 Open your browser to: http://localhost:8080")
    print("=" * 50)
    
    # Start the web app
    start_web_app()

if __name__ == "__main__":
    main()
