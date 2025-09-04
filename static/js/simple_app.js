/**
 * Simplified RAG Chat Application JavaScript
 * Uses REST API instead of WebSockets for faster responses
 */

class SimpleRAGChatApp {
    constructor() {
        this.currentConversationId = 'default';
        this.conversations = new Map();
        
        this.initializeElements();
        this.initializeEventListeners();
        this.createNewConversation();
    }

    initializeElements() {
        // Main elements
        this.sidebar = document.getElementById('sidebar');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.newChatBtn = document.getElementById('newChatBtn');
        this.clearChatBtn = document.getElementById('clearChatBtn');
        this.statsBtn = document.getElementById('statsBtn');
        this.settingsBtn = document.getElementById('settingsBtn');
        
        // Chat elements
        this.chatContainer = document.getElementById('chatContainer');
        this.messagesContainer = document.getElementById('messagesContainer');
        this.welcomeMessage = document.getElementById('welcomeMessage');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.charCount = document.getElementById('charCount');
        
        // Modals
        this.statsModal = document.getElementById('statsModal');
        this.statsModalClose = document.getElementById('statsModalClose');
        this.statsContent = document.getElementById('statsContent');
        this.settingsModal = document.getElementById('settingsModal');
        this.settingsModalClose = document.getElementById('settingsModalClose');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        
        // Lists
        this.conversationsList = document.getElementById('conversationsList');
    }

    initializeEventListeners() {
        // Sidebar toggle
        this.sidebarToggle?.addEventListener('click', () => this.toggleSidebar());
        
        // New chat
        this.newChatBtn?.addEventListener('click', () => this.createNewConversation());
        
        // Clear chat
        this.clearChatBtn?.addEventListener('click', () => this.clearCurrentChat());
        
        // Stats modal
        this.statsBtn?.addEventListener('click', () => this.showStats());
        this.statsModalClose?.addEventListener('click', () => this.hideModal(this.statsModal));
        
        // Settings modal
        this.settingsBtn?.addEventListener('click', () => this.showSettings());
        this.settingsModalClose?.addEventListener('click', () => this.hideModal(this.settingsModal));
        
        // Message input
        this.messageInput?.addEventListener('input', () => this.handleInputChange());
        this.messageInput?.addEventListener('keydown', (e) => this.handleKeyDown(e));
        
        // Send button
        this.sendBtn?.addEventListener('click', () => this.sendMessage());
        
        // Prompt suggestions
        document.querySelectorAll('.prompt-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const prompt = e.target.getAttribute('data-prompt');
                this.messageInput.value = prompt;
                this.handleInputChange();
                this.sendMessage();
            });
        });
        
        // Modal close on outside click
        [this.statsModal, this.settingsModal].forEach(modal => {
            modal?.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.hideModal(modal);
                }
            });
        });
    }

    toggleSidebar() {
        this.sidebar.classList.toggle('open');
    }

    createNewConversation() {
        this.currentConversationId = 'conv_' + Date.now();
        this.conversations.set(this.currentConversationId, []);
        this.clearMessages();
        this.showWelcomeMessage();
        this.updateConversationsList();
        this.messageInput.focus();
    }

    clearCurrentChat() {
        if (confirm('Are you sure you want to clear this conversation?')) {
            this.clearMessages();
            this.showWelcomeMessage();
            if (this.currentConversationId) {
                this.conversations.set(this.currentConversationId, []);
            }
        }
    }

    clearMessages() {
        this.messagesContainer.innerHTML = '';
        this.hideWelcomeMessage();
    }

    showWelcomeMessage() {
        this.welcomeMessage.style.display = 'flex';
    }

    hideWelcomeMessage() {
        this.welcomeMessage.style.display = 'none';
    }

    handleInputChange() {
        const text = this.messageInput.value.trim();
        const length = this.messageInput.value.length;
        
        // Update character count
        this.charCount.textContent = `${length}/4000`;
        
        // Enable/disable send button
        this.sendBtn.disabled = !text || length === 0;
        
        // Auto-resize textarea
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }

    handleKeyDown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.sendMessage();
        }
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Add user message to UI
        this.addMessage('user', message);
        
        // Clear input
        this.messageInput.value = '';
        this.handleInputChange();
        
        // Hide welcome message
        this.hideWelcomeMessage();
        
        // Show loading indicator
        this.showLoadingIndicator();
        
        try {
            // Send via REST API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_id: this.currentConversationId
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
            } else {
                this.addMessage('assistant', data.response, data.timestamp);
            }
            
        } catch (error) {
            this.showError(`Network error: ${error.message}`);
        } finally {
            this.hideLoadingIndicator();
        }
    }

    addMessage(type, content, timestamp = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = type === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = content;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = timestamp ? this.formatTime(timestamp) : this.formatTime(new Date().toISOString());
        
        messageContent.appendChild(messageText);
        messageContent.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Store in conversation
        if (this.currentConversationId) {
            const conversation = this.conversations.get(this.currentConversationId) || [];
            conversation.push({
                type: type,
                content: content,
                timestamp: timestamp || new Date().toISOString()
            });
            this.conversations.set(this.currentConversationId, conversation);
        }
    }

    showLoadingIndicator() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message assistant loading-message';
        loadingDiv.id = 'loadingIndicator';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'typing-indicator';
        loadingIndicator.innerHTML = `
            <span>RAG Assistant is processing...</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
            <div class="processing-steps">
                <div class="step">🔍 Searching documents...</div>
                <div class="step">🧠 Generating response...</div>
            </div>
        `;
        
        messageContent.appendChild(loadingIndicator);
        loadingDiv.appendChild(avatar);
        loadingDiv.appendChild(messageContent);
        
        this.messagesContainer.appendChild(loadingDiv);
        this.scrollToBottom();
    }

    hideLoadingIndicator() {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    updateConversationsList() {
        this.conversationsList.innerHTML = '';
        
        this.conversations.forEach((conversation, id) => {
            if (conversation.length === 0) return;
            
            const firstMessage = conversation.find(msg => msg.type === 'user');
            if (!firstMessage) return;
            
            const conversationItem = document.createElement('div');
            conversationItem.className = `conversation-item ${id === this.currentConversationId ? 'active' : ''}`;
            conversationItem.textContent = firstMessage.content.substring(0, 50) + (firstMessage.content.length > 50 ? '...' : '');
            
            conversationItem.addEventListener('click', () => {
                this.loadConversation(id);
            });
            
            this.conversationsList.appendChild(conversationItem);
        });
    }

    loadConversation(conversationId) {
        this.currentConversationId = conversationId;
        this.clearMessages();
        
        const conversation = this.conversations.get(conversationId) || [];
        if (conversation.length === 0) {
            this.showWelcomeMessage();
        } else {
            conversation.forEach(msg => {
                this.addMessage(msg.type, msg.content, msg.timestamp);
            });
        }
        
        this.updateConversationsList();
    }

    async showStats() {
        this.showModal(this.statsModal);
        this.statsContent.innerHTML = '<div class="loading">Loading statistics...</div>';
        
        try {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            
            if (stats.error) {
                this.statsContent.innerHTML = `<div class="error">Error: ${stats.error}</div>`;
            } else {
                this.statsContent.innerHTML = `
                    <div class="stats-grid">
                        <div class="stat-item">
                            <h4>Documents</h4>
                            <p>${stats.total_documents || 0}</p>
                        </div>
                        <div class="stat-item">
                            <h4>Database Path</h4>
                            <p>${stats.database_path || 'Unknown'}</p>
                        </div>
                        <div class="stat-item">
                            <h4>Model</h4>
                            <p>${document.querySelector('.model-info')?.textContent || 'Unknown'}</p>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            this.statsContent.innerHTML = `<div class="error">Error loading statistics: ${error.message}</div>`;
        }
    }

    showSettings() {
        this.showModal(this.settingsModal);
    }

    showModal(modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    hideModal(modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }

    showError(message) {
        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message assistant error-message';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.style.backgroundColor = '#fee';
        messageContent.style.border = '1px solid #fcc';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = `Error: ${message}`;
        
        messageContent.appendChild(messageText);
        errorDiv.appendChild(avatar);
        errorDiv.appendChild(messageContent);
        
        this.messagesContainer.appendChild(errorDiv);
        this.scrollToBottom();
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SimpleRAGChatApp();
});
