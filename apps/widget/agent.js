(function() {
  // 1. Configuration
  const scriptUrl = new URL(document.currentScript.src);
  const agentId = scriptUrl.searchParams.get('agent_id');
  const backendUrl = "http://localhost:8000"; // Real life: https://api.yourdomain.com
  
  if (!agentId) {
    console.error("AI Agent: No agent_id provided in script URL.");
    return;
  }

  // 2. Inject CSS
  const style = document.createElement('style');
  style.innerHTML = `
    #ai-agent-widget-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 999999;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    #ai-agent-button {
      width: 60px;
      height: 60px;
      border-radius: 30px;
      background: linear-gradient(135deg, #0ea5e9, #0284c7);
      color: white;
      border: none;
      box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s;
    }
    #ai-agent-button:hover {
      transform: scale(1.05);
    }
    #ai-agent-button svg {
      width: 30px;
      height: 30px;
      fill: currentColor;
    }
    #ai-agent-chat-window {
      position: absolute;
      bottom: 80px;
      right: 0;
      width: 350px;
      height: 500px;
      max-height: 80vh;
      background: #ffffff;
      border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
      display: none;
      flex-direction: column;
      overflow: hidden;
      border: 1px solid #e5e7eb;
    }
    #ai-agent-chat-window.open {
      display: flex;
    }
    #ai-agent-header {
      background: #0ea5e9;
      color: white;
      padding: 16px;
      font-weight: 600;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    #ai-agent-close {
      background: none;
      border: none;
      color: white;
      cursor: pointer;
      font-size: 20px;
      line-height: 1;
    }
    #ai-agent-messages {
      flex: 1;
      padding: 16px;
      overflow-y: auto;
      background: #f8fafc;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .ai-agent-message {
      max-width: 80%;
      padding: 10px 14px;
      border-radius: 12px;
      font-size: 14px;
      line-height: 1.4;
      white-space: pre-wrap;
    }
    .ai-agent-message.assistant {
      background: white;
      color: #1e293b;
      align-self: flex-start;
      border: 1px solid #e2e8f0;
      border-bottom-left-radius: 4px;
    }
    .ai-agent-message.user {
      background: #0ea5e9;
      color: white;
      align-self: flex-end;
      border-bottom-right-radius: 4px;
    }
    #ai-agent-input-container {
      padding: 16px;
      background: white;
      border-top: 1px solid #e5e7eb;
      display: flex;
      gap: 8px;
    }
    #ai-agent-input {
      flex: 1;
      border: 1px solid #e2e8f0;
      border-radius: 20px;
      padding: 10px 16px;
      font-size: 14px;
      outline: none;
    }
    #ai-agent-input:focus {
      border-color: #0ea5e9;
    }
    #ai-agent-send {
      background: #0ea5e9;
      color: white;
      border: none;
      border-radius: 20px;
      padding: 0 16px;
      font-weight: 500;
      cursor: pointer;
    }
    #ai-agent-send:disabled {
      background: #94a3b8;
      cursor: not-allowed;
    }
    #ai-agent-typing {
      font-size: 12px;
      color: #64748b;
      margin-top: -4px;
      margin-bottom: 8px;
    }
  `;
  document.head.appendChild(style);

  // 3. Inject HTML
  const container = document.createElement('div');
  container.id = 'ai-agent-widget-container';
  container.innerHTML = `
    <div id="ai-agent-chat-window">
      <div id="ai-agent-header">
        <span>Chat with us</span>
        <button id="ai-agent-close">&times;</button>
      </div>
      <div id="ai-agent-messages">
        <div class="ai-agent-message assistant">Hi there! How can I help you today?</div>
      </div>
      <div id="ai-agent-input-container">
        <input type="text" id="ai-agent-input" placeholder="Type a message..." />
        <button id="ai-agent-send">Send</button>
      </div>
    </div>
    <button id="ai-agent-button" aria-label="Open Chat">
      <svg viewBox="0 0 24 24"><path d="M12 3c5.5 0 10 3.58 10 8s-4.5 8-10 8c-1.24 0-2.43-.2-3.53-.5C5.55 21 2 21 2 21c2.33-2.33 2.7-3.9 2.75-4.25C3.05 15.07 2 13.13 2 11c0-4.42 4.5-8 10-8z"/></svg>
    </button>
  `;
  document.body.appendChild(container);

  // 4. Logic
  const button = document.getElementById('ai-agent-button');
  const chatWindow = document.getElementById('ai-agent-chat-window');
  const closeBtn = document.getElementById('ai-agent-close');
  const input = document.getElementById('ai-agent-input');
  const sendBtn = document.getElementById('ai-agent-send');
  const messagesDiv = document.getElementById('ai-agent-messages');
  
  let chatHistory = [];
  let isOpen = false;

  button.addEventListener('click', () => {
    isOpen = !isOpen;
    if (isOpen) {
      chatWindow.classList.add('open');
      input.focus();
    } else {
      chatWindow.classList.remove('open');
    }
  });

  closeBtn.addEventListener('click', () => {
    isOpen = false;
    chatWindow.classList.remove('open');
  });

  function addMessage(text, sender) {
    const msg = document.createElement('div');
    msg.className = \`ai-agent-message \${sender}\`;
    msg.textContent = text;
    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  function showTyping() {
    const typing = document.createElement('div');
    typing.id = 'ai-agent-typing';
    typing.textContent = 'Assistant is typing...';
    messagesDiv.appendChild(typing);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  function removeTyping() {
    const typing = document.getElementById('ai-agent-typing');
    if (typing) typing.remove();
  }

  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    // UI Updates
    addMessage(text, 'user');
    input.value = '';
    input.disabled = true;
    sendBtn.disabled = true;
    showTyping();

    try {
      const response = await fetch(\`\${backendUrl}/api/chat/\${agentId}\`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          history: chatHistory
        })
      });

      if (!response.ok) throw new Error('API Error');
      
      const data = await response.json();
      removeTyping();
      addMessage(data.response, 'assistant');
      
      // Save to history
      chatHistory.push({ role: 'user', content: text });
      chatHistory.push({ role: 'assistant', content: data.response });
      
    } catch (e) {
      removeTyping();
      addMessage("Sorry, I'm having trouble connecting right now. Please try again later.", 'assistant');
      console.error(e);
    } finally {
      input.disabled = false;
      sendBtn.disabled = false;
      input.focus();
    }
  }

  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });

})();
