document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages-box');
    const typingIndicator = document.getElementById('typing-indicator');
    const clearBtn = document.getElementById('clear-btn');


    // Clear chat log
    clearBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear the conversation history?')) {
            // Keep only the first welcome message
            const firstMessage = chatMessages.firstElementChild;
            chatMessages.innerHTML = '';
            if (firstMessage) {
                chatMessages.appendChild(firstMessage);
            }
        }
    });

    // Handle suggestion and pill buttons click
    const setupSuggestionButtons = () => {
        const actionButtons = document.querySelectorAll('.suggest-btn, .pill-btn');
        actionButtons.forEach(btn => {
            // Remove existing listener to prevent duplicate binding
            const newBtn = btn.cloneNode(true);
            btn.parentNode.replaceChild(newBtn, btn);
            
            newBtn.addEventListener('click', (e) => {
                const query = e.target.getAttribute('data-query');
                if (query) {
                    chatInput.value = query;
                    chatForm.dispatchEvent(new Event('submit'));
                }
            });
        });
    };

    setupSuggestionButtons();

    // Form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const messageText = chatInput.value.trim();
        if (!messageText) return;
        
        // Append user message
        appendMessage(messageText, 'user');
        chatInput.value = '';
        
        // Show typing indicator
        typingIndicator.style.display = 'flex';
        scrollToBottom();
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: messageText })
            });
            
            const data = await response.json();
            
            // Hide typing indicator
            typingIndicator.style.display = 'none';
            
            if (data.success) {
                appendMessage(data.response, 'bot', data.sql_query);
            } else {
                appendMessage(data.response || 'An error occurred. Please try again.', 'bot');
            }
        } catch (error) {
            console.error('Error fetching chat response:', error);
            typingIndicator.style.display = 'none';
            appendMessage('Failed to connect to the database server. Please ensure the backend is running.', 'bot');
        }
        
        scrollToBottom();
    });

    // Appends bubble helper
    function appendMessage(text, sender, sqlQuery = null) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        
        // Avatar element
        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('message-avatar');
        if (sender === 'user') {
            avatarDiv.innerHTML = '<i class="fa-solid fa-user"></i>';
        } else if (sender === 'system') {
            avatarDiv.innerHTML = '<i class="fa-solid fa-info"></i>';
        } else {
            avatarDiv.innerHTML = '<i class="fa-solid fa-robot"></i>';
        }
        messageDiv.appendChild(avatarDiv);
        
        // Content container
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        
        // Render simple formatting: bullet points and linebreaks
        const formattedText = formatBotResponse(text);
        contentDiv.innerHTML = formattedText;
        

        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
    }

    // Basic HTML escaping
    function escapeHtml(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Formatter to render Markdown bullet points or markdown tables/bolds into HTML tags
    function formatBotResponse(text) {
        if (!text) return '';
        
        let html = text;
        
        // Escape standard HTML first
        html = escapeHtml(html);
        
        // Handle bolding: **text** to <strong>text</strong>
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Handle list bullet points: * or - followed by text
        // Group multiple lists
        const lines = html.split('\n');
        let inList = false;
        let result = [];
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            if (line.startsWith('* ') || line.startsWith('- ')) {
                if (!inList) {
                    result.push('<ul>');
                    inList = true;
                }
                result.push(`<li>${line.substring(2)}</li>`);
            } else {
                if (inList) {
                    result.push('</ul>');
                    inList = false;
                }
                if (line === '') {
                    result.push('<br>');
                } else {
                    result.push(`<p>${line}</p>`);
                }
            }
        }
        if (inList) {
            result.push('</ul>');
        }
        
        return result.join('');
    }

    // Scroll chat pane helper
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
