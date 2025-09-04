#!/usr/bin/env python3
"""
Stable RAG System - No auto-reload, stable for testing
"""
import os
import sys
import subprocess
import time
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

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
        
        # Use the virtual environment Python
        venv_python = os.path.join(os.getcwd(), '.venv', 'bin', 'python3')
        
        # Create a fast query script
        fast_query_script = f'''
import sys
sys.path.append('.')
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function

# Use faster, smaller model
model = OllamaLLM(model="deepseek-r1:1.5b")  # Much faster model
embedding_function = get_embedding_function()
db = Chroma(persist_directory="chroma", embedding_function=embedding_function)

# Search with fewer results for speed
results = db.similarity_search_with_score("{message}", k=2)  # Reduced from 5 to 2

context_text = "\\n\\n---\\n\\n".join([doc.page_content for doc, _score in results])

prompt_template = ChatPromptTemplate.from_template("""
Answer the question based only on the following context:

{{context}}

---

Answer the question based on the above context: {{question}}
""")

prompt = prompt_template.format(context=context_text, question="{message}")
response_text = model.invoke(prompt)

print(f"Response: {{response_text}}")
print(f"Sources: {{[doc.metadata.get('id', None) for doc, _score in results]}}")
'''
        
        with open('temp_fast_query.py', 'w') as f:
            f.write(fast_query_script)
        
        # Run the fast query
        result = subprocess.run([
            venv_python, 'temp_fast_query.py'
        ], capture_output=True, text=True, timeout=20)  # Much shorter timeout
        
        # Clean up
        if os.path.exists('temp_fast_query.py'):
            os.remove('temp_fast_query.py')
        
        if result.returncode == 0:
            # Extract the response
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
        'mode': 'stable_rag_system'
    })

def main():
    """Main startup function"""
    print("🚀 Starting Stable RAG System...")
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
    print("🎉 Stable RAG System Ready!")
    print("🌐 Open your browser to: http://localhost:8095")
    print("💬 Ask questions about your documents!")
    print("=" * 50)
    
    # Run the Flask app WITHOUT debug mode to prevent auto-reload
    try:
        app.run(debug=False, host='0.0.0.0', port=8096)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
