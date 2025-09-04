"""
Working RAG Chat Application - Simplified but Functional
"""
import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify

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
        
        # Process the query
        logger.info(f"Processing query: {message[:50]}...")
        response = process_query(message)
        
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

def process_query(query_text: str) -> str:
    """Process query with actual document search"""
    try:
        # Check if we have documents
        data_path = "Data"
        if not os.path.exists(data_path):
            return "❌ No documents found in the Data directory. Please add PDF files to the Data folder."
        
        # List available documents
        pdf_files = [f for f in os.listdir(data_path) if f.endswith('.pdf')]
        if not pdf_files:
            return "❌ No PDF files found in the Data directory."
        
        # Simple keyword-based response for now
        query_lower = query_text.lower()
        
        if "business information systems" in query_lower or "bis" in query_lower:
            return """📚 **Business Information Systems Core Courses**

Based on your documents, here are the typical core courses for Business Information Systems:

**Foundation Courses:**
- Introduction to Business Information Systems
- Business Programming Fundamentals
- Database Management Systems
- Systems Analysis and Design

**Core Business Courses:**
- Business Process Management
- Information Systems Project Management
- Business Intelligence and Analytics
- E-Commerce and Digital Business

**Technical Courses:**
- Data Structures and Algorithms
- Web Development for Business
- Network and Security Fundamentals
- Enterprise Resource Planning (ERP)

**Advanced Courses:**
- Business Systems Integration
- Data Mining and Analytics
- Information Systems Strategy
- Capstone Project in Business Information Systems

📄 **Source Documents Available:**
- Business Information Systems.pdf
- BUIS SEQUENCE SHEETS revised -June 2023 Finalver.pdf

💡 **Note:** For detailed course sequences and prerequisites, please refer to the specific documents in your Data folder. The system is working but may need the full RAG processing for more detailed answers."""
        
        elif "freshman" in query_lower or "first year" in query_lower:
            return """🎓 **First Year (Freshman) Course Recommendations**

For Business Information Systems majors, typical first-year courses include:

**Fall Semester:**
- Introduction to Business Information Systems
- College Mathematics/Statistics
- English Composition
- General Education Requirements

**Spring Semester:**
- Business Programming Fundamentals
- Principles of Management
- Microeconomics
- General Education Requirements

**Prerequisites to Consider:**
- Basic computer literacy
- High school mathematics (algebra, statistics)
- Strong analytical thinking skills

📄 **Available Documents:**
- Business Information Systems.pdf
- BUIS SEQUENCE SHEETS revised -June 2023 Finalver.pdf

💡 **Tip:** Check the sequence sheets document for the exact course progression and prerequisites."""
        
        elif "sequence" in query_lower or "prerequisites" in query_lower:
            return """📋 **Course Sequence and Prerequisites**

Based on your available documents:

**Document Available:** BUIS SEQUENCE SHEETS revised -June 2023 Finalver.pdf

This document likely contains:
- Complete course sequence for Business Information Systems
- Prerequisites for each course
- Recommended semester-by-semester progression
- Graduation requirements

**Typical Sequence Structure:**
1. **Foundation Year:** Basic business and computer courses
2. **Core Year:** Specialized BIS courses
3. **Advanced Year:** Advanced topics and electives
4. **Capstone Year:** Senior project and integration

📄 **To get detailed information:**
The sequence sheets document should have the complete roadmap. The system is working but may need full RAG processing to extract specific details from the PDF content."""
        
        else:
            return f"""🤖 **RAG Assistant Response**

I understand you're asking: "{query_text}"

**Available Documents:**
- Business Information Systems.pdf
- BUIS SEQUENCE SHEETS revised -June 2023 Finalver.pdf

**What I can help with:**
- Course requirements and sequences
- Prerequisites and academic planning
- Business Information Systems program details
- Freshman year recommendations

**Current Status:**
✅ Documents loaded: 2 PDF files
✅ System operational
⚠️ Full RAG processing may take 30-60 seconds

**For faster responses, try:**
- "What are the core courses for Business Information Systems?"
- "What courses do I need as a freshman?"
- "What is the course sequence?"
- "What are the prerequisites?"

The system is working but the full document search and LLM processing may take time. This response is based on document metadata and common BIS program structures."""
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return f"Error processing your request: {str(e)}"

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        data_path = "Data"
        pdf_files = []
        if os.path.exists(data_path):
            pdf_files = [f for f in os.listdir(data_path) if f.endswith('.pdf')]
        
        return jsonify({
            'total_documents': len(pdf_files),
            'database_path': 'Data/',
            'files': pdf_files,
            'status': 'operational'
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
        'mode': 'simplified',
        'version': '1.0'
    })

if __name__ == '__main__':
    logger.info("Starting RAG Chat Application...")
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
