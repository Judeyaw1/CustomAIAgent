# 🚀 Professional RAG System with React TypeScript Frontend

## ✨ Features

- **Modern React TypeScript Frontend**: Professional, responsive UI with Material-UI
- **Real-time Chat Interface**: ChatGPT-like experience with message bubbles
- **RAG Integration**: Connects to your Business Information Systems documents
- **Professional Design**: Clean, modern interface with proper typography
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Error Handling**: Graceful error handling and loading states
- **CORS Enabled**: Seamless communication between frontend and backend

## 🎯 Quick Start

### Option 1: Run Both Together (Recommended)
```bash
cd rag-frontend
npm run dev
```
This will start both the React frontend (port 3000) and Flask backend (port 8095) simultaneously.

### Option 2: Run Separately

**Start Backend:**
```bash
source .venv/bin/activate
python3 stable_rag_system.py
```

**Start Frontend:**
```bash
cd rag-frontend
npm start
```

## 🌐 Access Your System

- **React Frontend**: http://localhost:3000
- **Flask Backend API**: http://localhost:8096
- **Health Check**: http://localhost:8096/api/health

## 🎨 UI Features

### Header
- RAG Assistant branding with AI icon
- Document indicator showing "Business Information Systems"
- Online status indicator

### Chat Interface
- Message bubbles with user/assistant avatars
- Timestamps and RAG indicators
- Typing indicators during processing
- Auto-scroll to latest messages
- Professional color scheme

### Input Area
- Multi-line text input
- Send button with loading states
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)
- Placeholder text with helpful hints

## 🔧 Technical Stack

### Frontend
- **React 18** with TypeScript
- **Material-UI (MUI)** for components
- **Axios** for API calls
- **date-fns** for date formatting
- **Inter font** for typography

### Backend
- **Flask** with CORS enabled
- **ChromaDB** for vector storage
- **Ollama** for LLM processing
- **LangChain** for RAG pipeline

## 📱 Responsive Design

The interface is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (320px - 767px)

## 🎯 Usage

1. **Open** http://localhost:3000 in your browser
2. **Ask questions** about Business Information Systems
3. **Get answers** from your document knowledge base
4. **Enjoy** the professional chat experience

## 🔍 Example Questions

- "What courses do I need as a freshman?"
- "Tell me about Business Information Systems"
- "What are the core requirements?"
- "What prerequisites do I need?"

## 🛠️ Development

### Frontend Development
```bash
cd rag-frontend
npm start          # Start development server
npm run build      # Build for production
npm test           # Run tests
```

### Backend Development
```bash
source .venv/bin/activate
python3 stable_rag_system.py
```

## 🎉 Your Professional RAG System is Ready!

You now have a beautiful, professional RAG system with:
- ✅ Modern React TypeScript frontend
- ✅ Professional Material-UI design
- ✅ Real-time chat interface
- ✅ Document-based Q&A
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states
- ✅ Professional typography

**Open http://localhost:3000 and start chatting with your RAG system!**
