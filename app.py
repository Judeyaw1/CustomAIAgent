"""
Flask web application for the RAG system with ChatGPT-like interface
"""
import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from enhanced_query import rag_system, query_rag
from config import config
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
socketio = SocketIO(app, cors_allowed_origins="*")

# Store conversation history in memory (in production, use a database)
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
        conversation_id = data.get('conversation_id', str(uuid.uuid4()))
        
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
        
        # Process the query
        response = query_rag(message)
        
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

@app.route('/api/conversations/<conversation_id>')
def get_conversation(conversation_id):
    """Get conversation history"""
    if conversation_id in conversations:
        return jsonify(conversations[conversation_id])
    return jsonify([])

@app.route('/api/conversations', methods=['DELETE'])
def clear_conversations():
    """Clear all conversations"""
    conversations.clear()
    return jsonify({'message': 'All conversations cleared'})

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        stats = rag_system.get_database_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model': config.llm_model,
        'embedding_model': config.embedding_model
    })

# WebSocket events for real-time chat
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to RAG system'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle real-time chat messages"""
    try:
        message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id', str(uuid.uuid4()))
        
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
        
        response = query_rag(message)
        
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

@socketio.on('get_conversation')
def handle_get_conversation(data):
    """Get conversation history via WebSocket"""
    conversation_id = data.get('conversation_id')
    if conversation_id and conversation_id in conversations:
        emit('conversation_history', conversations[conversation_id])
    else:
        emit('conversation_history', [])

if __name__ == '__main__':
    # Initialize the RAG system
    try:
        logger.info("Initializing RAG system...")
        # The rag_system is already initialized in enhanced_query.py
        logger.info("RAG system initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 8080))  # Use port 8080 by default
    socketio.run(app, debug=True, host='0.0.0.0', port=port)
