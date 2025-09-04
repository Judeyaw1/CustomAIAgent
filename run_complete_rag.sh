#!/bin/bash

echo "🚀 Starting Complete RAG System..."
echo "=================================="

# Activate virtual environment
source .venv/bin/activate

# Check if database exists
if [ ! -d "chroma" ]; then
    echo "📚 Database not found, populating..."
    python3 populate_database.py
    if [ $? -eq 0 ]; then
        echo "✅ Database populated successfully"
    else
        echo "❌ Database population failed"
        exit 1
    fi
else
    echo "✅ Database already exists"
fi

# Check documents
if [ -d "Data" ]; then
    pdf_count=$(find Data -name "*.pdf" | wc -l)
    echo "📄 Found $pdf_count PDF documents"
else
    echo "⚠️  No Data directory found"
fi

echo "=================================="
echo "🎉 Complete RAG System Ready!"
echo "🌐 Open your browser to: http://localhost:8085"
echo "💬 Ask questions about your documents!"
echo "=================================="

# Start the Flask app
python3 start_complete_rag.py
