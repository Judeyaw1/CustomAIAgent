#!/usr/bin/env python3
"""
One-Command Complete RAG System Startup
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
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        logger.info(f"Processing query: {message[:50]}...")
        
        # Use the original query_data.py system
        result = subprocess.run([
            sys.executable, 'query_data.py', message
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            # Extract the response from the output
            output_lines = result.stdout.strip().split('\n')
            response_lines = []
            in_response = False
            
            for line in output_lines:
                if 'Response:' in line:
                    in_response = True
                    response_lines.append(line.replace('Response:', '').strip())
                elif in_response and line.strip():
                    if line.startswith('Sources:'):
                        break
                    response_lines.append(line.strip())
            
            if response_lines:
                response = '\n'.join(response_lines)
            else:
                response = result.stdout.strip()
        else:
            response = f"Error processing query: {result.stderr}"
        
        return jsonify({
            'response': response,
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
        'mode': 'complete_rag_simple'
    })

def main():
    """Main startup function"""
    print("🚀 Starting Complete RAG System...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("query_data.py"):
        print("❌ query_data.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Check if database exists
    if not os.path.exists("chroma"):
        print("📚 Database not found, populating...")
        try:
            result = subprocess.run([sys.executable, 'populate_database.py'], 
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
    print("🎉 Complete RAG System Ready!")
    print("🌐 Open your browser to: http://localhost:8085")
    print("💬 Ask questions about your documents!")
    print("=" * 50)
    
    # Run the Flask app
    try:
        app.run(debug=True, host='0.0.0.0', port=8085)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
