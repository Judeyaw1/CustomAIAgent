# 🤖 Custom AI Agent - RAG System with React Frontend

A professional Retrieval-Augmented Generation (RAG) system with a modern React TypeScript frontend, designed for document-based question answering.

## ✨ Features

### 🎯 Core RAG System
- **Document Processing**: PDF document loading and chunking
- **Vector Database**: ChromaDB for semantic search
- **Local LLM**: Ollama integration with llama3.2:3b model
- **Embeddings**: nomic-embed-text for document embeddings
- **LangChain**: Complete RAG pipeline implementation

### 🎨 Modern Frontend
- **React TypeScript**: Professional, type-safe frontend
- **Material-UI**: Beautiful, responsive design
- **Real-time Chat**: ChatGPT-like interface
- **Error Handling**: Graceful error management
- **Responsive Design**: Works on all devices

### 🔧 Backend Features
- **Flask API**: RESTful endpoints with CORS support
- **Stable Server**: No auto-reload for production stability
- **Timeout Handling**: Graceful timeout management
- **Health Checks**: System monitoring endpoints

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Ollama installed and running
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Judeyaw1/CustomAIAgent.git
cd CustomAIAgent
```

### 2. Backend Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install and start Ollama models
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# Populate the database
python3 enhanced_populate.py
```

### 3. Frontend Setup
```bash
cd rag-frontend
npm install
```

### 4. Run the System

**Option 1: Run Both Together**
```bash
cd rag-frontend
npm run dev
```

**Option 2: Run Separately**
```bash
# Terminal 1: Backend
source .venv/bin/activate
python3 stable_rag_system.py

# Terminal 2: Frontend
cd rag-frontend
npm start
```

## 🌐 Access Your System

- **React Frontend**: http://localhost:3000
- **Flask Backend API**: http://localhost:8096
- **Health Check**: http://localhost:8096/api/health

## 📁 Project Structure

```
CustomAIAgent/
├── rag-frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   └── Header.tsx
│   │   ├── services/            # API services
│   │   │   └── api.ts
│   │   └── App.tsx
│   ├── package.json
│   └── README.md
├── Data/                        # PDF documents (add your own)
├── chroma/                      # Vector database (auto-generated)
├── config.py                    # Configuration settings
├── enhanced_populate.py         # Database population
├── enhanced_query.py            # RAG query system
├── stable_rag_system.py         # Main Flask application
├── query_data.py                # Core query functionality
├── get_embedding_function.py    # Embedding configuration
├── requirements.txt             # Python dependencies
└── README.md
```

## 🎯 Usage

1. **Add Documents**: Place your PDF files in the `Data/` directory
2. **Populate Database**: Run `python3 enhanced_populate.py`
3. **Start System**: Use the quick start commands above
4. **Ask Questions**: Use the web interface to query your documents

## 🔧 Configuration

### Backend Configuration (`config.py`)
```python
@dataclass
class RAGConfig:
    llm_model: str = "llama3.2:3b"
    embedding_model: str = "nomic-embed-text"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 3
    similarity_threshold: float = 0.6
```

### Frontend Configuration (`rag-frontend/src/services/api.ts`)
```typescript
const API_BASE_URL = 'http://localhost:8096';
```

## 🛠️ Development

### Backend Development
```bash
source .venv/bin/activate
python3 stable_rag_system.py
```

### Frontend Development
```bash
cd rag-frontend
npm start          # Development server
npm run build      # Production build
npm test           # Run tests
```

## 📊 API Endpoints

### Health Check
```bash
GET /api/health
```

### Chat
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "What courses do I need as a freshman?"
}
```

## 🎨 UI Features

- **Professional Header**: RAG Assistant branding with status indicators
- **Message Bubbles**: User/assistant avatars with timestamps
- **Typing Indicators**: Real-time processing feedback
- **Error Handling**: Graceful error messages
- **Responsive Design**: Mobile-friendly interface
- **Keyboard Shortcuts**: Enter to send, Shift+Enter for new line

## 🔍 Example Questions

- "What courses do I need as a freshman?"
- "Tell me about Business Information Systems"
- "What are the core requirements?"
- "What prerequisites do I need?"

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   lsof -ti:8096 | xargs kill -9
   ```

2. **Ollama Not Running**
   ```bash
   ollama serve
   ```

3. **Database Issues**
   ```bash
   rm -rf chroma/
   python3 enhanced_populate.py
   ```

4. **Frontend Build Issues**
   ```bash
   cd rag-frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

## 🎉 Acknowledgments

- [LangChain](https://langchain.com/) for RAG framework
- [Ollama](https://ollama.ai/) for local LLM
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [Material-UI](https://mui.com/) for React components
- [React](https://reactjs.org/) for frontend framework

---

**Built with ❤️ for document-based AI assistance**