#!/usr/bin/env python3
"""
Complete RAG System Startup Script
"""
import os
import sys
import subprocess
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_ollama():
    """Check if Ollama is running"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except:
        return False

def start_ollama():
    """Start Ollama service"""
    logger.info("Starting Ollama service...")
    try:
        subprocess.run(['brew', 'services', 'start', 'ollama'], check=True)
        time.sleep(3)
        return check_ollama()
    except:
        logger.error("Failed to start Ollama. Please start it manually: brew services start ollama")
        return False

def check_models():
    """Check if required models are available"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            models = result.stdout.lower()
            required_models = ['llama3.2:3b', 'nomic-embed-text']
            
            missing_models = []
            for model in required_models:
                if model not in models:
                    missing_models.append(model)
            
            if missing_models:
                logger.warning(f"Missing models: {', '.join(missing_models)}")
                logger.info("Installing missing models...")
                for model in missing_models:
                    logger.info(f"Installing {model}...")
                    subprocess.run(['ollama', 'pull', model], check=True)
                return True
            else:
                logger.info("All required models are available")
                return True
        else:
            logger.error("Failed to check models")
            return False
    except Exception as e:
        logger.error(f"Error checking models: {e}")
        return False

def populate_database():
    """Populate the database if needed"""
    if not os.path.exists("chroma"):
        logger.info("Populating database...")
        try:
            result = subprocess.run(['python3', 'populate_database.py'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                logger.info("Database populated successfully")
                return True
            else:
                logger.error(f"Database population failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error populating database: {e}")
            return False
    else:
        logger.info("Database already exists")
        return True

def install_dependencies():
    """Install required dependencies"""
    logger.info("Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        logger.info("Dependencies installed successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False

def main():
    """Main startup sequence"""
    print("🚀 Starting Complete RAG System...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("complete_rag_app.py"):
        logger.error("complete_rag_app.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        logger.error("Failed to install dependencies")
        sys.exit(1)
    
    # Check Ollama
    if not check_ollama():
        logger.info("Ollama not running, attempting to start...")
        if not start_ollama():
            logger.error("Please start Ollama manually: brew services start ollama")
            sys.exit(1)
    
    # Check models
    if not check_models():
        logger.error("Failed to setup models")
        sys.exit(1)
    
    # Populate database
    if not populate_database():
        logger.error("Failed to populate database")
        sys.exit(1)
    
    print("=" * 60)
    print("🎉 All systems ready! Starting Complete RAG Application...")
    print("🌐 Open your browser to: http://localhost:8080")
    print("=" * 60)
    
    # Start the complete RAG app
    try:
        subprocess.run([sys.executable, 'complete_rag_app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        logger.error(f"Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
