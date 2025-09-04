#!/usr/bin/env python3
"""
Final Complete RAG System - Uses Working Test Server Approach
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
        
        # Use the working test server approach
        try:
            import requests
            response = requests.get(f"http://localhost:8082/api/answer?query={message}", timeout=60)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    response_text = data.get('answer', 'No answer found.')
                    return jsonify({
                        'response': response_text,
                        'timestamp': time.time()
                    })
                else:
                    return jsonify({
                        'response': f"Error: {data.get('message', 'Unknown error')}",
                        'timestamp': time.time()
                    })
            else:
                return jsonify({
                    'response': f"Error: HTTP {response.status_code}",
                    'timestamp': time.time()
                })
        except Exception as e:
            logger.error(f"Error calling test server: {e}")
            return jsonify({
                'response': f"Error connecting to RAG system: {str(e)}",
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
        'mode': 'final_complete_rag'
    })

def main():
    """Main startup function"""
    print("🚀 Starting Final Complete RAG System...")
    print("=" * 50)
    
    # Check if test server is running
    try:
        import requests
        response = requests.get("http://localhost:8082/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Test server is running on port 8082")
        else:
            print("❌ Test server not responding. Please start it first: python3 test_server.py")
            sys.exit(1)
    except Exception as e:
        print("❌ Test server not running. Please start it first: python3 test_server.py")
        sys.exit(1)
    
    # Check documents
    data_path = "Data"
    if os.path.exists(data_path):
        pdf_files = [f for f in os.listdir(data_path) if f.endswith('.pdf')]
        print(f"📄 Found {len(pdf_files)} documents: {', '.join(pdf_files)}")
    else:
        print("⚠️  No Data directory found")
    
    print("=" * 50)
    print("🎉 Final Complete RAG System Ready!")
    print("🌐 Open your browser to: http://localhost:8089")
    print("💬 Ask questions about your documents!")
    print("=" * 50)
    
    # Run the Flask app
    try:
        app.run(debug=True, host='0.0.0.0', port=8089)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
