#!/usr/bin/env python3
"""
Fast Test RAG - Uses smaller model for faster responses
"""
import os
import sys
import subprocess
import time
import logging
from flask import Flask, render_template, request, jsonify

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('simple_index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        logger.info(f"Processing query: {message[:50]}...")
        
        # Use the virtual environment Python with a faster model
        venv_python = os.path.join(os.getcwd(), '.venv', 'bin', 'python3')
        
        # Create a temporary query file with faster model
        temp_query = f"""
import sys
sys.path.append('.')
from query_data import query_rag
from langchain_ollama import OllamaLLM

# Use faster model
model = OllamaLLM(model="deepseek-r1:1.5b")  # Smaller, faster model
query_rag("{message}", model=model)
"""
        
        with open('temp_query.py', 'w') as f:
            f.write(temp_query)
        
        # Run the query
        result = subprocess.run([
            venv_python, 'temp_query.py'
        ], capture_output=True, text=True, timeout=30)  # Shorter timeout
        
        # Clean up
        if os.path.exists('temp_query.py'):
            os.remove('temp_query.py')
        
        if result.returncode == 0:
            response = result.stdout.strip()
        else:
            response = f"Error: {result.stderr}"
        
        return jsonify({
            'response': response,
            'timestamp': time.time()
        })
        
    except subprocess.TimeoutExpired:
        logger.error("Query timed out")
        return jsonify({
            'response': "⏰ Query processing timed out. The system is working but may need more time for complex queries. Try asking a simpler question.",
            'timestamp': time.time()
        })
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'mode': 'fast_test_rag'
    })

def main():
    """Main startup function"""
    print("🚀 Starting Fast Test RAG System...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("query_data.py"):
        print("❌ query_data.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Check if virtual environment exists
    venv_python = os.path.join(os.getcwd(), '.venv', 'bin', 'python3')
    if not os.path.exists(venv_python):
        print("❌ Virtual environment not found. Please run: python3 -m venv .venv")
        sys.exit(1)
    
    # Check if database exists
    if not os.path.exists("chroma"):
        print("📚 Database not found, populating...")
        try:
            result = subprocess.run([venv_python, 'populate_database.py'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Database populated successfully")
            else:
                print(f"❌ Database population failed: {result.stderr}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error populating database: {e}")
            sys.exit(1)
    else:
        print("✅ Database already exists")
    
    # Check documents
    data_path = "Data"
    if os.path.exists(data_path):
        pdf_files = [f for f in os.listdir(data_path) if f.endswith('.pdf')]
        print(f"📄 Found {len(pdf_files)} documents: {', '.join(pdf_files)}")
    else:
        print("⚠️  No Data directory found")
    
    print("=" * 50)
    print("🎉 Fast Test RAG System Ready!")
    print("🌐 Open your browser to: http://localhost:8093")
    print("💬 Ask questions about your documents!")
    print("=" * 50)
    
    # Run the Flask app
    try:
        app.run(debug=True, host='0.0.0.0', port=8093)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
