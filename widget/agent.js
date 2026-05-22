/**
 * AI Agent Widget - Fully Customizable Embeddable Chat
 * 
 * Basic Usage:
 * <script src="https://your-domain.com/widget/agent.js" data-tenant-id="YOUR_TENANT_ID"></script>
 * 
 * With Customization:
 * <script 
 *   src="https://your-domain.com/widget/agent.js"
 *   data-tenant-id="YOUR_TENANT_ID"
 *   data-theme-primary="#667eea"
 *   data-theme-accent="#764ba2"
 *   data-background="#ffffff"
 *   data-text-color="#333333"
 *   data-header-text="Chat with us"
 *   data-placeholder="Ask a question..."
 *   data-logo-url="https://yourlogo.png"
 *   data-button-position="bottom-right"
 *   data-button-size="60"
 *   data-width="400"
 *   data-height="600"
 * ></script>
 */

(function() {
  // Configuration
  const API_BASE_URL = 'http://localhost:8000/api'; // Change to your backend URL
  const WIDGET_ID = 'ai-agent-widget';
  const STORAGE_KEY = 'ai_agent_session';

  // Get theme configuration from data attributes
  function getThemeConfig() {
    const script = document.currentScript || document.scripts[document.scripts.length - 1];
    const theme = {
      primary: script.dataset.themePrimary || '#667eea',
      accent: script.dataset.themeAccent || '#764ba2',
      background: script.dataset.background || '#ffffff',
      textColor: script.dataset.textColor || '#333333',
      headerText: script.dataset.headerText || 'Chat with us',
      placeholder: script.dataset.placeholder || 'Type your message...',
      logoUrl: script.dataset.logoUrl || '',
      buttonPosition: script.dataset.buttonPosition || 'bottom-right',
      buttonSize: parseInt(script.dataset.buttonSize) || 60,
      width: parseInt(script.dataset.width) || 400,
      height: parseInt(script.dataset.height) || 600,
    };
    return theme;
  }

  // Get tenant ID from script tag
  function getTenantId() {
    const script = document.currentScript || document.scripts[document.scripts.length - 1];
    return script?.dataset.tenantId || '';
  }

  // Get or create session ID
  function getSessionId() {
    let sessionId = localStorage.getItem(STORAGE_KEY);
    if (!sessionId) {
      sessionId = 'session_' + Math.random().toString(36).substr(2, 9) + Date.now();
      localStorage.setItem(STORAGE_KEY, sessionId);
    }
    return sessionId;
  }

  // Create widget HTML with dynamic theming
  function createWidgetHTML(theme) {
    // Detect if device is mobile
    const isMobile = window.innerWidth < 768;
    const chatWidth = isMobile ? '100vw' : `${theme.width}px`;
    const chatHeight = isMobile ? '100vh' : `${theme.height}px`;
    const chatMaxWidth = isMobile ? 'none' : `${Math.min(theme.width, window.innerWidth - 40)}px`;
    
    // Button position classes
    const positionClass = `ai-agent-button-${theme.buttonPosition}`;
    
    const html = `
      <div id="${WIDGET_ID}" class="ai-agent-widget ${positionClass}">
        <style>
          :root {
            --ai-primary: ${theme.primary};
            --ai-accent: ${theme.accent};
            --ai-background: ${theme.background};
            --ai-text: ${theme.textColor};
            --ai-border: ${lightenColor(theme.primary, 20)};
          }

          .ai-agent-widget {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            position: fixed;
            z-index: 99999;
            font-size: 14px;
          }

          /* Button Positions */
          .ai-agent-widget.ai-agent-button-bottom-right {
            bottom: 20px;
            right: 20px;
          }

          .ai-agent-widget.ai-agent-button-bottom-left {
            bottom: 20px;
            left: 20px;
          }

          .ai-agent-widget.ai-agent-button-top-right {
            top: 20px;
            right: 20px;
          }

          .ai-agent-widget.ai-agent-button-top-left {
            top: 20px;
            left: 20px;
          }

          /* Mobile responsiveness */
          @media (max-width: 768px) {
            .ai-agent-widget {
              bottom: 0 !important;
              right: 0 !important;
              left: 0 !important;
              top: 0 !important;
            }
          }

          .ai-agent-container {
            display: none;
            width: ${chatWidth};
            max-width: ${chatMaxWidth};
            height: ${chatHeight};
            max-height: 90vh;
            background: var(--ai-background);
            border-radius: 12px;
            box-shadow: 0 5px 40px rgba(0, 0, 0, 0.16);
            flex-direction: column;
            overflow: hidden;
            animation: slideUp 0.3s ease-in-out;
          }

          .ai-agent-container.open {
            display: flex;
          }

          @keyframes slideUp {
            from {
              opacity: 0;
              transform: translateY(20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }

          /* Mobile full screen */
          @media (max-width: 768px) {
            .ai-agent-container {
              width: 100vw;
              height: 100vh;
              max-width: 100vw;
              max-height: 100vh;
              border-radius: 0;
            }
          }

          .ai-agent-header {
            background: linear-gradient(135deg, var(--ai-primary) 0%, var(--ai-accent) 100%);
            color: white;
            padding: 16px 20px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-shrink: 0;
          }

          .ai-agent-header-content {
            display: flex;
            align-items: center;
            gap: 12px;
            flex: 1;
          }

          .ai-agent-logo {
            width: 40px;
            height: 40px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
          }

          .ai-agent-logo img {
            width: 100%;
            height: 100%;
            object-fit: cover;
          }

          .ai-agent-title {
            margin: 0;
            font-size: 16px;
            font-weight: 600;
            line-height: 1.2;
          }

          .ai-agent-close {
            background: none;
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
            padding: 8px;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 6px;
            transition: background 0.2s;
            flex-shrink: 0;
          }

          .ai-agent-close:hover {
            background: rgba(255, 255, 255, 0.1);
          }

          .ai-agent-messages {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
            background: var(--ai-background);
            display: flex;
            flex-direction: column;
            gap: 12px;
          }

          /* Scrollbar styling */
          .ai-agent-messages::-webkit-scrollbar {
            width: 6px;
          }

          .ai-agent-messages::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.05);
          }

          .ai-agent-messages::-webkit-scrollbar-thumb {
            background: var(--ai-primary);
            border-radius: 3px;
          }

          .ai-agent-message {
            display: flex;
            animation: fadeIn 0.3s ease-in;
            margin-bottom: 4px;
          }

          @keyframes fadeIn {
            from {
              opacity: 0;
            }
            to {
              opacity: 1;
            }
          }

          .ai-agent-message.user {
            justify-content: flex-end;
          }

          .ai-agent-message.assistant {
            justify-content: flex-start;
          }

          .ai-agent-message-text {
            display: inline-block;
            max-width: 85%;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.4;
            word-wrap: break-word;
            word-break: break-word;
          }

          .ai-agent-message.user .ai-agent-message-text {
            background: linear-gradient(135deg, var(--ai-primary) 0%, var(--ai-accent) 100%);
            color: white;
            border-bottom-right-radius: 4px;
          }

          .ai-agent-message.assistant .ai-agent-message-text {
            background: #f0f0f0;
            color: var(--ai-text);
            border: 1px solid var(--ai-border);
            border-bottom-left-radius: 4px;
          }

          /* Dark mode support */
          @media (prefers-color-scheme: dark) {
            .ai-agent-message.assistant .ai-agent-message-text {
              background: #2a2a2a;
              color: #e0e0e0;
              border-color: #444;
            }
          }

          .ai-agent-footer {
            padding: 12px;
            border-top: 1px solid var(--ai-border);
            display: flex;
            gap: 8px;
            flex-shrink: 0;
          }

          .ai-agent-input {
            flex: 1;
            border: 1px solid var(--ai-border);
            border-radius: 6px;
            padding: 10px 12px;
            font-size: 14px;
            font-family: inherit;
            color: var(--ai-text);
            background: var(--ai-background);
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
          }

          .ai-agent-input:focus {
            border-color: var(--ai-primary);
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
          }

          .ai-agent-input::placeholder {
            color: rgba(0, 0, 0, 0.4);
          }

          /* Dark mode input */
          @media (prefers-color-scheme: dark) {
            .ai-agent-input {
              background: #1a1a1a;
              color: #e0e0e0;
            }
            .ai-agent-input::placeholder {
              color: rgba(255, 255, 255, 0.4);
            }
          }

          .ai-agent-send {
            background: var(--ai-primary);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 16px;
            font-size: 14px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s, opacity 0.2s;
            flex-shrink: 0;
          }

          .ai-agent-send:hover {
            background: ${lightenColor('#667eea', 10)};
            opacity: 0.9;
          }

          .ai-agent-send:disabled {
            background: #ccc;
            cursor: not-allowed;
            opacity: 0.6;
          }

          .ai-agent-button {
            width: ${theme.buttonSize}px;
            height: ${theme.buttonSize}px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--ai-primary) 0%, var(--ai-accent) 100%);
            color: white;
            border: none;
            font-size: ${Math.max(24, theme.buttonSize / 2.5)}px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s, box-shadow 0.2s;
          }

          .ai-agent-button:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
          }

          .ai-agent-button:active {
            transform: scale(0.95);
          }

          .ai-agent-button.hidden {
            display: none;
          }

          .ai-agent-loading {
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--ai-text);
            margin: 0 2px;
            animation: bounce 1.4s infinite;
          }

          .ai-agent-loading:nth-child(1) {
            animation-delay: -0.32s;
          }

          .ai-agent-loading:nth-child(2) {
            animation-delay: -0.16s;
          }

          @keyframes bounce {
            0%, 80%, 100% {
              opacity: 0.3;
              transform: scale(1);
            }
            40% {
              opacity: 1;
              transform: scale(1.2);
            }
          }

          /* Mobile optimizations */
          @media (max-width: 480px) {
            .ai-agent-header {
              padding: 12px 16px;
            }

            .ai-agent-messages {
              padding: 12px;
            }

            .ai-agent-footer {
              padding: 10px;
            }

            .ai-agent-message-text {
              max-width: 90%;
              font-size: 13px;
              padding: 10px 12px;
            }

            .ai-agent-button {
              width: ${theme.buttonSize - 10}px;
              height: ${theme.buttonSize - 10}px;
            }
          }

          /* iPad orientation */
          @media (max-width: 968px) and (orientation: landscape) {
            .ai-agent-container {
              height: 80vh;
            }
          }
        </style>

        <button class="ai-agent-button" id="ai-agent-toggle" title="Chat with us!" aria-label="Open chat">
          💬
        </button>

        <div class="ai-agent-container" id="ai-agent-chat">
          <div class="ai-agent-header">
            <div class="ai-agent-header-content">
              ${theme.logoUrl ? `<div class="ai-agent-logo"><img src="${theme.logoUrl}" alt="Logo" /></div>` : ''}
              <h2 class="ai-agent-title">${escapeHtml(theme.headerText)}</h2>
            </div>
            <button class="ai-agent-close" id="ai-agent-close" aria-label="Close chat">✕</button>
          </div>
          <div class="ai-agent-messages" id="ai-agent-messages"></div>
          <div class="ai-agent-footer">
            <input
              type="text"
              class="ai-agent-input"
              id="ai-agent-input"
              placeholder="${escapeHtml(theme.placeholder)}"
              autocomplete="off"
              aria-label="Message input"
            />
            <button class="ai-agent-send" id="ai-agent-send" aria-label="Send message">Send</button>
          </div>
        </div>
      </div>
    `;
    return html;
  }

  // Lighten color helper
  function lightenColor(color, percent) {
    const num = parseInt(color.replace('#', ''), 16);
    const amt = Math.round(2.55 * percent);
    const R = Math.min(255, (num >> 16) + amt);
    const G = Math.min(255, (num >> 8 & 0x00FF) + amt);
    const B = Math.min(255, (num & 0x0000FF) + amt);
    return '#' + (0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).slice(1);
  }

  // Send message to backend
  async function sendMessage(message) {
    const tenantId = getTenantId();
    const sessionId = getSessionId();

    if (!tenantId) {
      console.error('AI Agent: tenant-id not specified');
      return null;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tenant_id: tenantId,
          message: message,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('AI Agent API error:', error);
      return {
        answer: 'Sorry, I\'m having trouble connecting. Please try again or contact us directly.',
        provider: 'error',
        model: 'error',
        confidence: 0,
        handoff_recommended: true,
        reservation_detected: false,
      };
    }
  }

  // Add message to chat
  function addMessage(text, isUser) {
    const messagesContainer = document.getElementById('ai-agent-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `ai-agent-message ${isUser ? 'user' : 'assistant'}`;

    if (!isUser && text === 'loading') {
      messageDiv.innerHTML = `
        <div class="ai-agent-message-text">
          <span class="ai-agent-loading"></span>
          <span class="ai-agent-loading"></span>
          <span class="ai-agent-loading"></span>
        </div>
      `;
      messageDiv.id = 'ai-agent-loading';
    } else {
      messageDiv.innerHTML = `<div class="ai-agent-message-text">${escapeHtml(text)}</div>`;
    }

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Escape HTML to prevent XSS
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Initialize widget
  function init() {
    const theme = getThemeConfig();

    // Inject widget HTML
    const widgetContainer = document.createElement('div');
    widgetContainer.innerHTML = createWidgetHTML(theme);
    document.body.appendChild(widgetContainer);

    // Get elements
    const toggleBtn = document.getElementById('ai-agent-toggle');
    const closeBtn = document.getElementById('ai-agent-close');
    const chatContainer = document.getElementById('ai-agent-chat');
    const sendBtn = document.getElementById('ai-agent-send');
    const input = document.getElementById('ai-agent-input');
    const messagesContainer = document.getElementById('ai-agent-messages');

    // Toggle chat visibility
    toggleBtn.addEventListener('click', () => {
      chatContainer.classList.toggle('open');
      if (chatContainer.classList.contains('open')) {
        toggleBtn.classList.add('hidden');
        input.focus();
        // Add welcome message if first time
        if (messagesContainer.children.length === 0) {
          addMessage('Hi! How can I help you today?', false);
        }
      }
    });

    closeBtn.addEventListener('click', () => {
      chatContainer.classList.remove('open');
      toggleBtn.classList.remove('hidden');
    });

    // Close on mobile when window resizes to desktop
    window.addEventListener('orientationchange', () => {
      setTimeout(() => {
        if (window.innerWidth > 768 && chatContainer.classList.contains('open')) {
          // Allow it to stay open on desktop
        }
      }, 100);
    });

    // Send message
    async function handleSend() {
      const message = input.value.trim();
      if (!message) return;

      // Clear input and disable button
      input.value = '';
      sendBtn.disabled = true;

      // Add user message
      addMessage(message, true);

      // Add loading indicator
      addMessage('loading', false);

      // Send to backend
      const response = await sendMessage(message);

      // Remove loading
      const loading = document.getElementById('ai-agent-loading');
      if (loading) loading.remove();

      if (response) {
        addMessage(response.answer, false);
        
        // Show handoff suggestion if needed
        if (response.handoff_recommended) {
          addMessage(
            'I recommend connecting with someone from our team. They\'ll be able to help you better.',
            false
          );
        }

        // Show reservation confirmation if detected
        if (response.reservation_detected) {
          addMessage(
            'I see you\'re interested in booking. Please provide your name, preferred date and time, and we\'ll confirm your reservation.',
            false
          );
        }
      }

      // Re-enable button
      sendBtn.disabled = false;
      input.focus();
    }

    sendBtn.addEventListener('click', handleSend);
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    });

    // Handle initial chat opening
    input.addEventListener('focus', () => {
      if (!chatContainer.classList.contains('open')) {
        chatContainer.classList.add('open');
        toggleBtn.classList.add('hidden');
      }
    });
  }

  // Wait for DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
