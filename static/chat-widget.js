/* ═══════════════════════════════════════
   SKILLTECH AI — SHARED CHAT WIDGET
   chat-widget.js
   Drop this after the closing </main> tag.
   Requires chat-widget.css to be linked.
═══════════════════════════════════════ */
(function(){
  'use strict';

  const API = 'http://localhost:8000';

  /* ── Inject HTML ── */
  document.body.insertAdjacentHTML('beforeend', `
    <button id="chatFab" aria-label="Open AI assistant">
      💬<div class="fab-dot" id="fabDot"></div>
    </button>

    <div id="chatPanel" role="dialog" aria-label="SkillTech Assistant">
      <div class="chat-head">
        <div class="chat-av">AI</div>
        <div>
          <div class="chat-name">SKILLTECH ASSISTANT</div>
          <div class="chat-status" id="widgetStatus">● ONLINE AND READY</div>
        </div>
        <button class="chat-x" id="chatClose" aria-label="Close chat">×</button>
      </div>
      <div class="chat-msgs" id="chatMsgs">
        <div class="cmsg ai">
          <div class="c-av">AI</div>
          <div class="c-bub">Hi! 👋 I'm your SkillTech career assistant.

I can help with career advice, course recommendations, EV industry info, resume tips, and salary benchmarks for Tamil Nadu's automotive sector.

What would you like to know?</div>
        </div>
        <div class="chat-chips" id="chatChips">
          <button class="chip" onclick="widgetSendChip(this)">What jobs suit a Diploma in EV?</button>
          <button class="chip" onclick="widgetSendChip(this)">Best free PLC courses?</button>
          <button class="chip" onclick="widgetSendChip(this)">How do I get into EV sector?</button>
          <button class="chip" onclick="widgetSendChip(this)">Expected salary for BMS roles?</button>
        </div>
      </div>
      <div class="chat-row">
        <textarea class="c-inp" id="widgetInp" placeholder="Ask about careers, courses, skills…" rows="1"></textarea>
        <button class="c-send" id="widgetSend" aria-label="Send">↑</button>
      </div>
    </div>
  `);

  /* ── State ── */
  let chatOpen    = false;
  let chatHistory = [];

  /* ── DOM refs (after injection) ── */
  const fab    = document.getElementById('chatFab');
  const panel  = document.getElementById('chatPanel');
  const msgs   = document.getElementById('chatMsgs');
  const inp    = document.getElementById('widgetInp');
  const sendBtn= document.getElementById('widgetSend');
  const closeBtn=document.getElementById('chatClose');
  const fabDot = document.getElementById('fabDot');

  /* ── Toggle ── */
  function toggleChat(){
    chatOpen = !chatOpen;
    panel.classList.toggle('open', chatOpen);
    fab.textContent = '';
    if(chatOpen){
      fab.innerHTML = '×<div class="fab-dot" id="fabDot" style="display:none"></div>';
      fab.style.fontSize = '22px';
      fabDot && (fabDot.style.display = 'none');
      inp.focus();
    } else {
      fab.innerHTML = '💬<div class="fab-dot" id="fabDot"></div>';
      fab.style.fontSize = '20px';
    }
  }

  fab.addEventListener('click', toggleChat);
  closeBtn.addEventListener('click', toggleChat);

  /* Close on Escape */
  document.addEventListener('keydown', e => {
    if(e.key === 'Escape' && chatOpen) toggleChat();
  });

  /* ── Auto-resize textarea ── */
  inp.addEventListener('input', () => {
    inp.style.height = 'auto';
    inp.style.height = Math.min(inp.scrollHeight, 90) + 'px';
  });
  inp.addEventListener('keydown', e => {
    if(e.key === 'Enter' && !e.shiftKey){ e.preventDefault(); sendChat(); }
  });
  sendBtn.addEventListener('click', sendChat);

  /* ── Chip click ── */
  window.widgetSendChip = function(btn){
    document.getElementById('chatChips')?.remove();
    inp.value = btn.textContent;
    sendChat();
  };

  /* ── Add message bubble ── */
  function addMsg(role, text){
    const wrap = document.createElement('div');
    wrap.className = 'cmsg ' + role;
    const av  = document.createElement('div');
    av.className = 'c-av';
    av.textContent = role === 'ai' ? 'AI' : 'YOU';
    const bub = document.createElement('div');
    bub.className = 'c-bub';
    if(role === 'ai') bub.innerHTML = renderMd(text);
    else              bub.textContent = text;
    wrap.appendChild(av);
    wrap.appendChild(bub);
    msgs.appendChild(wrap);
    msgs.scrollTop = msgs.scrollHeight;
    return bub;
  }

  /* ── Typing indicator ── */
  function addTyping(){
    const wrap = document.createElement('div');
    wrap.className = 'cmsg ai'; wrap.id = 'widgetTyping';
    wrap.innerHTML = `<div class="c-av">AI</div><div class="c-bub"><div class="t-dots"><div class="t-d"></div><div class="t-d"></div><div class="t-d"></div></div></div>`;
    msgs.appendChild(wrap);
    msgs.scrollTop = msgs.scrollHeight;
  }

  /* ── Markdown renderer ── */
  function renderMd(text){
    let h = text
      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
      .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
      .replace(/\*(.+?)\*/g,'<em>$1</em>')
      .replace(/`(.+?)`/g,'<code style="background:rgba(20,184,166,.1);padding:1px 5px;border-radius:4px;font-family:monospace;font-size:11px;color:#0d9488">$1</code>');
    const lines = h.split('\n');
    let out = '', inList = false;
    for(const line of lines){
      const m = line.match(/^[\-\*•]\s+(.*)/);
      if(m){
        if(!inList){ out += '<ul style="margin:6px 0 6px 14px;padding:0;list-style:disc">'; inList = true; }
        out += `<li style="margin:2px 0">${m[1]}</li>`;
      } else {
        if(inList){ out += '</ul>'; inList = false; }
        out += line ? `<span>${line}</span><br>` : '<br>';
      }
    }
    if(inList) out += '</ul>';
    return out;
  }

  /* ── Send ── */
  async function sendChat(){
    document.getElementById('chatChips')?.remove();
    const text = inp.value.trim();
    if(!text) return;
    inp.value = ''; inp.style.height = 'auto';
    sendBtn.disabled = true;
    addMsg('user', text);
    addTyping();

    const payload = {
      message: text,
      history: chatHistory,
      // No skill context on shared pages — assistant answers generally
    };

    try {
      const resp = await fetch(`${API}/api/chat/stream`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(payload),
      });
      document.getElementById('widgetTyping')?.remove();

      if(!resp.ok) throw new Error(`Server ${resp.status}`);

      const bub    = addMsg('ai','');
      const reader = resp.body.getReader();
      const dec    = new TextDecoder();
      let full = '';

      while(true){
        const { done, value } = await reader.read();
        if(done) break;
        dec.decode(value).split('\n').forEach(line => {
          if(!line.startsWith('data: ')) return;
          const d = line.slice(6);
          if(d === '[DONE]') return;
          try {
            const p = JSON.parse(d);
            if(p.token){ full += p.token; bub.innerHTML = renderMd(full); msgs.scrollTop = msgs.scrollHeight; }
          } catch{}
        });
      }
      chatHistory.push({role:'user',content:text},{role:'assistant',content:full});

    } catch(e){
      document.getElementById('widgetTyping')?.remove();
      const isOffline = e.message.includes('fetch') || e.message.includes('Failed');
      addMsg('ai', isOffline
        ? '⚠️ The AI backend is offline. Start it with:\n\n`uvicorn main:app --reload`\n\nThen try again.'
        : '⚠️ ' + e.message
      );
    } finally {
      sendBtn.disabled = false;
    }
  }

  /* ── Health check — update status dot ── */
  fetch(`${API}/api/health`)
    .then(r => r.json())
    .then(d => {
      document.getElementById('widgetStatus').textContent =
        d.model_loaded ? '● MODEL READY' : '● SERVER READY';
    })
    .catch(() => {
      document.getElementById('widgetStatus').textContent = '● OFFLINE';
      document.getElementById('widgetStatus').style.color = '#94a3b8';
    });

})();
