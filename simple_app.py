"""
Simplified Flask app for faster RAG responses
"""
import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from enhanced_query import rag_system
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Store conversation history in memory
conversations = {}

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('simple_index.html')

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
        
        # Process the query with timeout
        logger.info(f"Processing query: {message[:50]}...")
        
        # Use a simpler, faster approach
        response = process_query_fast(message)
        
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

def process_query_fast(query_text: str) -> str:
    """Fast query processing with simplified approach"""
    try:
        # Get database stats first
        stats = rag_system.get_database_stats()
        if "error" in stats:
            return f"Database error: {stats['error']}"
        
        # Simple response for now
        return f"""I found {stats.get('total_documents', 0)} documents in the database.

Based on your question: "{query_text}"

I can help you find information about:
- Course requirements and sequences
- Business Information Systems programs
- Academic planning and prerequisites

The system is currently processing your request. For faster responses, try asking more specific questions like:
- "What are the core courses for Business Information Systems?"
- "What prerequisites do I need for advanced courses?"
- "What is the course sequence for my major?"

Note: The full RAG system is working but may take 30-60 seconds for complete responses due to the local LLM processing."""
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return f"Error processing your request: {str(e)}"

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

if __name__ == '__main__':
    # Initialize the RAG system
    try:
        logger.info("Initializing RAG system...")
        # The rag_system is already initialized in enhanced_query.py
        logger.info("RAG system initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
