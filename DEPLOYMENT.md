# 🚀 Deployment Guide

## 📋 Prerequisites

Before deploying your RAG system, ensure you have:

- **Python 3.8+** installed
- **Node.js 16+** installed
- **Git** installed
- **Ollama** installed and running
- **Internet connection** for model downloads

## 🏗️ Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Judeyaw1/CustomAIAgent.git
cd CustomAIAgent
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Ollama models
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# Add your PDF documents to the Data/ directory
# Then populate the database
python3 enhanced_populate.py
```

### 3. Frontend Setup
```bash
cd rag-frontend
npm install
```

### 4. Run the System
```bash
# Option 1: Run both together
cd rag-frontend
npm run dev

# Option 2: Run separately
# Terminal 1: Backend
source .venv/bin/activate
python3 stable_rag_system.py

# Terminal 2: Frontend
cd rag-frontend
npm start
```

## 🌐 Production Deployment

### Backend Deployment (Flask)

#### Option 1: Using Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8096 stable_rag_system:app
```

#### Option 2: Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8096

CMD ["python3", "stable_rag_system.py"]
```

### Frontend Deployment (React)

#### Option 1: Build and Serve
```bash
cd rag-frontend
npm run build
# Serve the build folder with any static server
```

#### Option 2: Using Docker
```dockerfile
FROM node:16-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

## ☁️ Cloud Deployment Options

### Heroku
1. Create `Procfile`:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT stable_rag_system:app
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### AWS EC2
1. Launch EC2 instance
2. Install dependencies
3. Configure security groups
4. Run with PM2 or systemd

### DigitalOcean App Platform
1. Connect GitHub repository
2. Configure build and run commands
3. Set environment variables
4. Deploy

## 🔧 Environment Configuration

### Backend Environment Variables
```bash
export PORT=8096
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
```

### Frontend Environment Variables
```bash
REACT_APP_API_URL=http://localhost:8096
```

## 📊 Monitoring and Logging

### Health Checks
```bash
curl http://localhost:8096/api/health
```

### Logs
```bash
# Backend logs
tail -f logs/app.log

# Frontend logs
npm run build 2>&1 | tee build.log
```

## 🛡️ Security Considerations

1. **Environment Variables**: Never commit secrets
2. **CORS**: Configure for production domains
3. **Rate Limiting**: Implement API rate limiting
4. **HTTPS**: Use SSL certificates in production
5. **Firewall**: Configure proper firewall rules

## 🔄 Updates and Maintenance

### Updating the System
```bash
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
cd rag-frontend && npm install
```

### Database Updates
```bash
# Rebuild database with new documents
rm -rf chroma/
python3 enhanced_populate.py
```

## 📈 Performance Optimization

### Backend
- Use Gunicorn with multiple workers
- Implement caching
- Optimize database queries
- Use CDN for static files

### Frontend
- Enable gzip compression
- Use React.memo for components
- Implement code splitting
- Optimize bundle size

## 🚨 Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in configuration
2. **Memory issues**: Increase server memory
3. **Model loading**: Ensure Ollama is running
4. **CORS errors**: Check CORS configuration

### Debug Mode
```bash
# Backend debug
export FLASK_DEBUG=1
python3 stable_rag_system.py

# Frontend debug
cd rag-frontend
npm start
```

## 📞 Support

For deployment issues:
1. Check the logs
2. Verify all dependencies are installed
3. Ensure all services are running
4. Check network connectivity
5. Review configuration files

---

**Happy Deploying! 🚀**
