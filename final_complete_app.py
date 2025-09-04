"""
Final Complete RAG Application - Full Functionality
Uses the original query_data.py system for maximum compatibility
"""
import os
import json
import logging
import subprocess
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
socketio = SocketIO(app, cors_allowed_origins="*")

# Store conversation history in memory
conversations = {}

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages via REST API"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id', 'default')
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get or create conversation
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # Add user message to conversation
        conversations[conversation_id].append({
            'type': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Process the query with the original RAG system
        logger.info(f"Processing query: {message[:50]}...")
        response = process_query_with_original_rag(message)
        
        # Add assistant response to conversation
        conversations[conversation_id].append({
            'type': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'response': response,
            'conversation_id': conversation_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

def process_query_with_original_rag(query_text: str) -> str:
    """Process query using the original query_data.py system"""
    try:
        # Use the original query_data.py system
        result = subprocess.run([
            sys.executable, 'query_data.py', query_text
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
                return '\n'.join(response_lines)
            else:
                return result.stdout.strip()
        else:
            logger.error(f"RAG processing failed: {result.stderr}")
            return f"Error processing query: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "⏰ Query processing timed out. The system is working but may need more time for complex queries."
    except Exception as e:
        logger.error(f"Error in RAG processing: {e}")
        return f"Error processing your request: {str(e)}"

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        # Check documents
        data_path = "Data"
        pdf_files = []
        if os.path.exists(data_path):
            pdf_files = [f for f in os.listdir(data_path) if f.endswith('.pdf')]
        
        # Check database
        chroma_path = "chroma"
        db_exists = os.path.exists(chroma_path)
        
        return jsonify({
            'total_documents': len(pdf_files),
            'database_path': chroma_path,
            'database_exists': db_exists,
            'files': pdf_files,
            'status': 'operational',
            'mode': 'complete_rag_original'
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'mode': 'complete_rag_original',
        'version': '1.0'
    })

# WebSocket events for real-time chat
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to Complete RAG system'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle real-time chat messages"""
    try:
        message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id', 'default')
        
        if not message:
            emit('error', {'message': 'Message cannot be empty'})
            return
        
        # Get or create conversation
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # Add user message
        user_message = {
            'type': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        }
        conversations[conversation_id].append(user_message)
        
        # Emit user message back to client
        emit('message', user_message)
        
        # Process the query
        emit('typing', {'status': True})
        
        response = process_query_with_original_rag(message)
        
        # Add assistant response
        assistant_message = {
            'type': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        }
        conversations[conversation_id].append(assistant_message)
        
        # Emit assistant response
        emit('typing', {'status': False})
        emit('message', assistant_message)
        
    except Exception as e:
        logger.error(f"Error in chat_message: {e}")
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    logger.info("Starting Final Complete RAG Application...")
    
    # Check if database exists
    if not os.path.exists("chroma"):
        logger.info("Database not found, populating...")
        try:
            result = subprocess.run([sys.executable, 'populate_database.py'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                logger.info("Database populated successfully")
            else:
                logger.error(f"Database population failed: {result.stderr}")
        except Exception as e:
            logger.error(f"Error populating database: {e}")
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 8084))
    logger.info(f"Starting server on port {port}")
    socketio.run(app, debug=True, host='0.0.0.0', port=port)
