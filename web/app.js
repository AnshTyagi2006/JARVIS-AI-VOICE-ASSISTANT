/* ==========================================================================
   JARVIS AI VOICE ASSISTANT — INTERACTIVE BLUEPRINT ENGINE (APP.JS)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    
    // UI Element References
    const micBtn = document.getElementById('mic-trigger-btn');
    const textCommandForm = document.getElementById('text-command-form');
    const textInput = document.getElementById('text-input');
    const consoleOutput = document.getElementById('console-output');
    const pillStatusText = document.getElementById('pill-status-text');
    const hudStatusBadge = document.getElementById('hud-status-badge');
    const hudInputVal = document.getElementById('hud-input-val');
    const aiGlowOverlay = document.getElementById('ai-glow-overlay');

    // Modals
    const btnAbout = document.getElementById('btn-about');
    const btnHowTo = document.getElementById('btn-how-to');
    const btnContact = document.getElementById('btn-contact');
    const modalAbout = document.getElementById('modal-about');
    const modalHowTo = document.getElementById('modal-how-to');
    const modalContact = document.getElementById('modal-contact');
    const modalCloses = document.querySelectorAll('.modal-close');

    // State
    let isListening = false;
    let isSpeaking = false;
    let recognition = null;

    // Sound Cues Audio Instances
    const soundStart = new Audio('/api/sounds/ding_start.mp3');
    const soundEnd = new Audio('/api/sounds/ding_end.mp3');

    function playSound(audioObj) {
        if (audioObj) {
            audioObj.currentTime = 0;
            audioObj.play().catch(err => console.log('Sound playback cue:', err));
        }
    }

    /* ==========================================================================
       BLUEPRINT TECH GRID CANVAS BACKGROUND
       ========================================================================== */
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    let nodes = [];

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    class GridNode {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.vx = (Math.random() - 0.5) * 0.4;
            this.vy = (Math.random() - 0.5) * 0.4;
            this.radius = Math.random() * 1.8 + 0.8;
        }

        update() {
            const speed = (isSpeaking || isListening) ? 2.0 : 1.0;
            this.x += this.vx * speed;
            this.y += this.vy * speed;

            if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
            if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = isSpeaking ? 'rgba(20, 241, 149, 0.7)' : (isListening ? 'rgba(255, 0, 85, 0.7)' : 'rgba(0, 240, 255, 0.4)');
            ctx.fill();
        }
    }

    for (let i = 0; i < 65; i++) {
        nodes.push(new GridNode());
    }

    function drawBlueprintGrid() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw Blueprint Grid Lines
        const gridSize = 45;
        ctx.strokeStyle = 'rgba(0, 240, 255, 0.03)';
        ctx.lineWidth = 1;

        for (let x = 0; x < canvas.width; x += gridSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += gridSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }

        // Draw Nodes and Connecting Lines
        for (let i = 0; i < nodes.length; i++) {
            nodes[i].update();
            nodes[i].draw();

            for (let j = i + 1; j < nodes.length; j++) {
                const dx = nodes[i].x - nodes[j].x;
                const dy = nodes[i].y - nodes[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 130) {
                    ctx.beginPath();
                    ctx.moveTo(nodes[i].x, nodes[i].y);
                    ctx.lineTo(nodes[j].x, nodes[j].y);
                    const alpha = (1 - dist / 130) * 0.15;
                    ctx.strokeStyle = isSpeaking ? `rgba(20, 241, 149, ${alpha})` : (isListening ? `rgba(255, 0, 85, ${alpha})` : `rgba(0, 240, 255, ${alpha})`);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(drawBlueprintGrid);
    }
    drawBlueprintGrid();

    /* ==========================================================================
       TRANSCRIPT & CONSOLE LOGIC
       ========================================================================== */
    function updateExchange(sender, text) {
        consoleOutput.innerHTML = '';
        const msgDiv = document.createElement('div');
        msgDiv.className = `transcript-msg ${sender.toLowerCase()}-msg`;
        
        let prefix = '';
        if (sender === 'USER') prefix = 'YOU: ';
        if (sender === 'JARVIS') prefix = 'JARVIS: ';

        msgDiv.textContent = `${prefix}${text}`;
        consoleOutput.appendChild(msgDiv);
    }

    /* ==========================================================================
       SPEECH RECOGNITION (WEB SPEECH API + BACKEND FALLBACK)
       ========================================================================== */
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            setListeningState(true);
            playSound(soundStart);
            updateExchange('SYS', 'Listening for voice command...');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            updateExchange('USER', transcript);
            setListeningState(false);
            executeCommand(transcript, 'Browser microphone');
        };

        recognition.onerror = (event) => {
            console.warn('Speech recognition error:', event.error);
            setListeningState(false);
            if (event.error !== 'no-speech') {
                updateExchange('SYS', `Speech error: ${event.error}`);
            } else {
                updateExchange('SYS', 'No speech detected. Ready.');
            }
        };

        recognition.onend = () => {
            setListeningState(false);
        };
    }

    // Mic Click Listener
    micBtn.addEventListener('click', () => {
        if (isSpeaking) {
            window.speechSynthesis.cancel();
            setSpeakingState(false);
            return;
        }

        if (isListening) {
            if (recognition) recognition.stop();
            setListeningState(false);
        } else {
            if (recognition) {
                try {
                    recognition.start();
                } catch (e) {
                    console.log('Recognition starting:', e);
                }
            } else {
                // Fallback to backend microphone
                setListeningState(true);
                playSound(soundStart);
                fetch('/api/listen', { method: 'POST' })
                    .then(res => res.json())
                    .then(data => {
                        setListeningState(false);
                        if (data.recognized_text) {
                            updateExchange('USER', data.recognized_text);
                            executeCommand(data.recognized_text);
                        } else {
                            updateExchange('SYS', 'No speech captured.');
                        }
                    })
                    .catch(() => setListeningState(false));
            }
        }
    });

    function setListeningState(active) {
        isListening = active;
        if (active) {
            micBtn.classList.add('listening');
            pillStatusText.textContent = 'LISTENING';
            hudStatusBadge.innerHTML = '<span class="hud-dot" style="background:#ff0055;box-shadow:0 0 6px #ff0055"></span> LISTENING';
            hudInputVal.textContent = 'Active listening...';
        } else {
            micBtn.classList.remove('listening');
            if (!isSpeaking) {
                pillStatusText.textContent = 'READY';
                hudStatusBadge.innerHTML = '<span class="hud-dot"></span> READY';
                hudInputVal.textContent = 'Browser microphone';
            }
        }
    }

    function setSpeakingState(active) {
        isSpeaking = active;
        if (active) {
            micBtn.classList.add('speaking');
            aiGlowOverlay.classList.add('active-speaking');
            pillStatusText.textContent = 'SPEAKING';
            hudStatusBadge.innerHTML = '<span class="hud-dot" style="background:#14f195"></span> SPEAKING';
        } else {
            micBtn.classList.remove('speaking');
            aiGlowOverlay.classList.remove('active-speaking');
            pillStatusText.textContent = 'READY';
            hudStatusBadge.innerHTML = '<span class="hud-dot"></span> READY';
        }
    }


    /* ==========================================================================
       REMOTE BROWSER ACTIONS
       The Python server cannot open the visitor's local browser. These actions
       are therefore executed client-side after a user-initiated command.
       ========================================================================== */
    function triggerBrowserAction(command) {
        const normalized = command.toLowerCase().trim();

        const websites = {
            google: 'https://www.google.com',
            youtube: 'https://www.youtube.com',
            facebook: 'https://www.facebook.com',
            instagram: 'https://www.instagram.com',
            linkedin: 'https://www.linkedin.com',
            chat: 'https://www.chatgpt.com',
            whatsapp: 'https://www.whatsapp.com',
            spotify: 'https://www.spotify.com',
            amazon: 'https://www.amazon.com',
            flipkart: 'https://www.flipkart.com',
            github: 'https://github.com'
        };

        for (const [keyword, url] of Object.entries(websites)) {
            if (normalized === keyword || normalized === `open ${keyword}`) {
                window.open(url, '_blank', 'noopener,noreferrer');
                return true;
            }
        }

        if (normalized.startsWith('search ')) {
            const query = normalized.replace(/^search\s+/, '').trim();
            if (query) {
                window.open(
                    `https://www.google.com/search?q=${encodeURIComponent(query)}`,
                    '_blank',
                    'noopener,noreferrer'
                );
                return true;
            }
        }

        if (normalized.startsWith('search for ')) {
            const query = normalized.replace(/^search for\s+/, '').trim();
            if (query) {
                window.open(
                    `https://www.google.com/search?q=${encodeURIComponent(query)}`,
                    '_blank',
                    'noopener,noreferrer'
                );
                return true;
            }
        }

        if (normalized.startsWith('play ')) {
            const song = normalized.replace(/^play\s+/, '').trim();
            if (song) {
                window.open(
                    `https://www.youtube.com/results?search_query=${encodeURIComponent(song)}`,
                    '_blank',
                    'noopener,noreferrer'
                );
                return true;
            }
        }

        return false;
    }

    /* ==========================================================================
       COMMAND EXECUTION API & AUDIO CUE SYNC
       ========================================================================== */
    function executeCommand(commandText, inputSource = 'AI Text Console') {
        if (!commandText || !commandText.trim()) return;

        // Execute browser-only actions immediately from the visitor's browser.
        // This must happen before the async fetch so popup blockers are less likely.
        triggerBrowserAction(commandText);

        // Play start chime immediately on transmission
        playSound(soundStart);

        hudInputVal.textContent = inputSource;
        pillStatusText.textContent = 'PROCESSING';
        hudStatusBadge.innerHTML = '<span class="hud-dot" style="background:#00f0ff"></span> PROCESSING';

        fetch('/api/process_command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: commandText })
        })
        .then(res => res.json())
        .then(data => {
            const resp = data.response || 'Command executed.';
            updateExchange('JARVIS', resp);

            // Play end chime right when response arrives & TTS begins
            playSound(soundEnd);
            speakJARVIS(resp);
        })
        .catch(err => {
            console.error('API Error:', err);
            updateExchange('SYS', 'Error connecting to Python JARVIS backend.');
            pillStatusText.textContent = 'ERROR';
        });
    }

    /* ==========================================================================
       TTS SYNTHESIS ENGINE (ACCELERATED HIGH-SPEED AI SPEECH)
       ========================================================================== */
    function speakJARVIS(text, onComplete) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.18; // Crisp, accelerated AI speech rate
            utterance.pitch = 0.98;

            utterance.onstart = () => setSpeakingState(true);
            utterance.onend = () => {
                setSpeakingState(false);
                if (onComplete) onComplete();
            };
            utterance.onerror = () => {
                setSpeakingState(false);
                if (onComplete) onComplete();
            };

            window.speechSynthesis.speak(utterance);
        } else {
            if (onComplete) onComplete();
        }
    }

    /* ==========================================================================
       INPUT FORM & CHIPS
       ========================================================================== */
    textCommandForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const cmd = textInput.value.trim();
        if (cmd) {
            updateExchange('USER', cmd);
            textInput.value = '';
            executeCommand(cmd, 'AI Text Console');
        }
    });

    // Handle Enter Key in Textarea
    textInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            textCommandForm.dispatchEvent(new Event('submit'));
        }
    });

    document.querySelectorAll('.chip-pill').forEach(chip => {
        chip.addEventListener('click', () => {
            const cmd = chip.getAttribute('data-cmd');
            if (cmd) {
                updateExchange('USER', cmd);
                executeCommand(cmd, 'Quick Command Chip');
            }
        });
    });

    /* ==========================================================================
       MODALS
       ========================================================================== */
    function openModal(modal) { modal.classList.add('open'); }
    function closeModal(modal) { modal.classList.remove('open'); }

    btnAbout.addEventListener('click', () => openModal(modalAbout));
    btnHowTo.addEventListener('click', () => openModal(modalHowTo));
    btnContact.addEventListener('click', () => openModal(modalContact));

    modalCloses.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-close');
            const modal = document.getElementById(targetId);
            if (modal) closeModal(modal);
        });
    });

    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal(modal);
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay.open').forEach(closeModal);
        }
    });

});
