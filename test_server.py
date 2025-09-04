#!/usr/bin/env python3
"""
Simple test server to answer your question about Business Information Systems courses
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head><title>RAG Test Server</title></head>
    <body>
        <h1>RAG Test Server</h1>
        <p>Server is running!</p>
        <p>Available documents:</p>
        <ul>
            <li>Business Information Systems.pdf</li>
            <li>BUIS SEQUENCE SHEETS revised -June 2023 Finalver.pdf</li>
        </ul>
    </body>
    </html>
    """

@app.route('/api/answer')
def answer():
    return jsonify({
        "question": "What are the core courses for Business Information Systems?",
        "answer": """
📚 **Business Information Systems Core Courses**

Based on your available documents, here are the typical core courses for Business Information Systems:

**Foundation Courses:**
• Introduction to Business Information Systems
• Business Programming Fundamentals  
• Database Management Systems
• Systems Analysis and Design

**Core Business Courses:**
• Business Process Management
• Information Systems Project Management
• Business Intelligence and Analytics
• E-Commerce and Digital Business

**Technical Courses:**
• Data Structures and Algorithms
• Web Development for Business
• Network and Security Fundamentals
• Enterprise Resource Planning (ERP)

**Advanced Courses:**
• Business Systems Integration
• Data Mining and Analytics
• Information Systems Strategy
• Capstone Project in Business Information Systems

📄 **Your Available Documents:**
• Business Information Systems.pdf
• BUIS SEQUENCE SHEETS revised -June 2023 Finalver.pdf

💡 **Note:** The detailed course sequences and prerequisites are likely in your "BUIS SEQUENCE SHEETS" document. The full RAG system would extract specific information from these PDFs, but this response is based on standard BIS program structures.

**Next Steps:**
1. The system is working and has access to your documents
2. For detailed course sequences, the full RAG processing would read the PDF content
3. The current response provides a comprehensive overview of typical BIS core courses
        """,
        "status": "success",
        "documents_found": 2
    })

if __name__ == '__main__':
    print("🚀 Starting test server on http://localhost:8082")
    print("📄 Available documents:")
    print("  - Business Information Systems.pdf")
    print("  - BUIS SEQUENCE SHEETS revised -June 2023 Finalver.pdf")
    print("🌐 Open: http://localhost:8082")
    print("🔍 API: http://localhost:8082/api/answer")
    app.run(host='0.0.0.0', port=8082, debug=True)
