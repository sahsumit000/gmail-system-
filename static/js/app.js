document.addEventListener('DOMContentLoaded', async () => {
    const voiceBtn = document.getElementById('voice-btn');
    const modeToggleBtn = document.getElementById('mode-toggle-btn');
    const transcriptDisplay = document.getElementById('transcript-display');
    const audioPlayer = document.getElementById('audio-player');
    
    let isVoiceMode = localStorage.getItem('voiceMode');
    if (isVoiceMode === null) {
        isVoiceMode = true;
        localStorage.setItem('voiceMode', true);
    } else {
        isVoiceMode = isVoiceMode === 'true';
    }

    let mediaRecorder = null;
    let audioChunks = [];
    let stream = null;
    let audioContext = null;
    let analyser = null;
    let silenceTimer = null;
    let ttsPlaying = false;
    let manualRecording = false;

    let composeState = 'INACTIVE';
    let composeData = { to: '', subject: '', body: '', action: '' };

    // Initialize UI
    updateModeUI();

    // Check if we need to speak a confirmation from the previous page load
    const speakText = localStorage.getItem('speakText');
    if (speakText) {
        localStorage.removeItem('speakText');
        await speakAloud(speakText);
    } else if (window.location.pathname === '/compose' && localStorage.getItem('startComposeFlow')) {
        localStorage.removeItem('startComposeFlow');
        setTimeout(async () => {
            composeState = 'ASK_RECIPIENT';
            await speakAloud("Tell me the email address whom you want to mail.");
        }, 500);
    } else if (isVoiceMode) {
        // If not speaking, start listening immediately if in auto mode
        startListening();
    }

    modeToggleBtn.addEventListener('click', () => {
        isVoiceMode = !isVoiceMode;
        localStorage.setItem('voiceMode', isVoiceMode);
        updateModeUI();
        if (isVoiceMode) {
            if (!ttsPlaying) startListening();
        } else {
            stopListening();
        }
    });

    voiceBtn.addEventListener('click', () => {
        if (isVoiceMode) {
            // In auto mode, clicking this acts as a forced stop/restart or manual trigger
            if (mediaRecorder && mediaRecorder.state === 'recording') {
                stopListening();
                transcriptDisplay.innerText = "Listening paused.";
            } else {
                startListening();
            }
        } else {
            // Manual mode
            if (manualRecording) {
                stopListening();
                manualRecording = false;
            } else {
                manualRecording = true;
                startListening(true); // true = disable VAD silence timeout
            }
        }
    });

    function updateModeUI() {
        modeToggleBtn.innerText = isVoiceMode ? "Mode: Voice (Auto)" : "Mode: Manual (Click)";
        modeToggleBtn.style.backgroundColor = isVoiceMode ? "#e8f0fe" : "transparent";
    }

    async function startListening(disableVAD = false) {
        if (ttsPlaying) return; // Don't listen while speaking!
        
        if (!stream) {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            } catch (err) {
                console.error("Mic error:", err);
                transcriptDisplay.innerText = "Mic access denied.";
                return;
            }
        }

        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioContext.createMediaStreamSource(stream);
            analyser = audioContext.createAnalyser();
            analyser.minDecibels = -70; // Sensible threshold
            source.connect(analyser);
        }

        if (mediaRecorder && mediaRecorder.state === 'recording') return;

        audioChunks = [];
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = e => { if (e.data.size > 0) audioChunks.push(e.data); };
        
        mediaRecorder.onstop = async () => {
            voiceBtn.classList.remove('recording');
            voiceBtn.innerText = isVoiceMode ? 'Listening (Auto)...' : '🎤 Voice Command';
            
            if (audioChunks.length === 0) {
                if (isVoiceMode && !ttsPlaying) startListening();
                return;
            }

            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            audioChunks = [];
            
            if (audioBlob.size > 1000) { // Only send if it's not a completely empty blip
                const formData = new FormData();
                formData.append('file', audioBlob, 'command.webm');
                transcriptDisplay.innerText = "Processing Voice...";
                
                try {
                    const response = await fetch('/api/transcribe', { method: 'POST', body: formData });
                    const data = await response.json();
                    
                    if (data.text && data.text.trim().length > 0) {
                        transcriptDisplay.innerText = `Heard: "${data.text}"`;
                        
                        if (composeState !== 'INACTIVE') {
                            handleComposeFlow(data.text);
                            return; // Bypass normal intent handling
                        }
                        
                        if (data.intent && data.intent !== 'UNKNOWN') {
                            handleIntent(data.intent, data.entities, data.text);
                            return; // Navigation will handle the rest
                        }
                    } else {
                        transcriptDisplay.innerText = "Silence detected.";
                    }
                } catch (err) {
                    console.error("Transcription error:", err);
                    transcriptDisplay.innerText = "Error parsing speech.";
                }
            }

            // Loop listening if in auto mode and not navigating away
            if (isVoiceMode && !ttsPlaying) {
                startListening();
            }
        };

        mediaRecorder.start();
        voiceBtn.classList.add('recording');
        voiceBtn.innerText = disableVAD ? 'Recording (Click to stop)' : 'Listening...';

        if (!disableVAD) {
            runVAD();
        }
    }

    function runVAD() {
        let speechDetected = false;
        const dataArray = new Uint8Array(analyser.frequencyBinCount);
        
        // Failsafe: Automatically stop after 8 seconds so it doesn't listen forever if it misses silence
        let maxRecordTimer = setTimeout(() => {
            if (mediaRecorder && mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
            }
        }, 8000);
        
        function checkSilence() {
            if (!mediaRecorder || mediaRecorder.state !== 'recording' || manualRecording) return;
            
            analyser.getByteFrequencyData(dataArray);
            let sum = dataArray.reduce((a, b) => a + b, 0);
            let average = sum / dataArray.length;
            
            if (average > 5) { // Lowered threshold (from 10 to 5) so it detects softer speech
                speechDetected = true;
                if (silenceTimer) {
                    clearTimeout(silenceTimer);
                    silenceTimer = null;
                }
            } else {
                if (speechDetected && !silenceTimer) {
                    // User stopped speaking. Wait 1.5s before submitting
                    silenceTimer = setTimeout(() => {
                        if (mediaRecorder && mediaRecorder.state === 'recording') {
                            clearTimeout(maxRecordTimer);
                            mediaRecorder.stop();
                        }
                    }, 1500);
                }
            }
            requestAnimationFrame(checkSilence);
        }
        checkSilence();
    }

    function stopListening() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            // We temporarily assign empty onstop so it doesn't process half-words when forcefully stopped
            mediaRecorder.onstop = () => {
                voiceBtn.classList.remove('recording');
                voiceBtn.innerText = isVoiceMode ? 'Listening Paused' : '🎤 Voice Command';
            };
            mediaRecorder.stop();
        }
        if (silenceTimer) clearTimeout(silenceTimer);
    }

    async function handleComposeFlow(text) {
        const raw = text.replace(/[.,!?]$/, '').trim(); // remove trailing punctuation
        const lower = raw.toLowerCase().replace(/[^a-z0-9\s@\.]/g, '');
        
        switch (composeState) {
            case 'ASK_RECIPIENT':
                let emailText = raw.replace(/\bat\b/gi, '@').replace(/\s+/g, '').toLowerCase();
                composeData.to = emailText;
                document.getElementById('recipient').value = emailText;
                composeState = 'CONFIRM_RECIPIENT';
                await speakAloud(`You said ${emailText}. Is this correct?`);
                break;
                
            case 'CONFIRM_RECIPIENT':
                if (lower.includes('yes') || lower.includes('yeah') || lower.includes('correct') || lower.includes('right')) {
                    composeState = 'ASK_SUBJECT';
                    await speakAloud("What should be the subject?");
                } else if (lower.includes('no') || lower.includes('wrong')) {
                    composeState = 'ASK_RECIPIENT';
                    document.getElementById('recipient').value = '';
                    await speakAloud("Okay, tell me the email address again.");
                } else {
                    await speakAloud("Please say yes or no.");
                }
                break;
                
            case 'ASK_SUBJECT':
                composeData.subject = raw;
                document.getElementById('subject').value = raw;
                composeState = 'CONFIRM_SUBJECT';
                await speakAloud(`The subject is ${raw}. Is this correct?`);
                break;
                
            case 'CONFIRM_SUBJECT':
                if (lower.includes('yes') || lower.includes('yeah') || lower.includes('correct') || lower.includes('right')) {
                    composeState = 'ASK_BODY';
                    await speakAloud("What should I write in the email?");
                } else if (lower.includes('no') || lower.includes('wrong')) {
                    composeState = 'ASK_SUBJECT';
                    document.getElementById('subject').value = '';
                    await speakAloud("Okay, tell me the subject again.");
                } else {
                    await speakAloud("Please say yes or no.");
                }
                break;
                
            case 'ASK_BODY':
                composeData.body = raw;
                document.getElementById('body').value = raw;
                composeState = 'CONFIRM_BODY';
                await speakAloud(`You wrote: ${raw}. Is this correct?`);
                break;
                
            case 'CONFIRM_BODY':
                if (lower.includes('yes') || lower.includes('yeah') || lower.includes('correct') || lower.includes('right')) {
                    composeState = 'ASK_ACTION';
                    await speakAloud("Do you want to send this email, save as draft, or discard?");
                } else if (lower.includes('no') || lower.includes('wrong')) {
                    composeState = 'ASK_BODY';
                    document.getElementById('body').value = '';
                    await speakAloud("Okay, what should I write in the email?");
                } else {
                    await speakAloud("Please say yes or no.");
                }
                break;
                
            case 'ASK_ACTION':
                if (lower.includes('send')) {
                    composeData.action = 'send';
                    composeState = 'CONFIRM_ACTION';
                    await speakAloud("Are you sure you want to send it?");
                } else if (lower.includes('save') || lower.includes('draft')) {
                    composeData.action = 'draft';
                    composeState = 'CONFIRM_ACTION';
                    await speakAloud("Are you sure you want to save as draft?");
                } else if (lower.includes('discard') || lower.includes('delete') || lower.includes('trash')) {
                    composeData.action = 'discard';
                    composeState = 'CONFIRM_ACTION';
                    await speakAloud("Are you sure you want to discard this email?");
                } else {
                    await speakAloud("Please say send, save as draft, or discard.");
                }
                break;
                
            case 'CONFIRM_ACTION':
                if (lower.includes('yes') || lower.includes('yeah') || lower.includes('correct') || lower.includes('right')) {
                    composeState = 'INACTIVE';
                    executeComposeAction(composeData.action);
                } else if (lower.includes('no') || lower.includes('wrong')) {
                    composeState = 'ASK_ACTION';
                    await speakAloud("Okay, do you want to send, save as draft, or discard?");
                } else {
                    await speakAloud("Please say yes or no.");
                }
                break;
        }
    }

    async function executeComposeAction(action) {
        if (action === 'discard') {
            localStorage.setItem('speakText', "Email discarded.");
            window.location.href = '/inbox';
            return;
        }
        
        const folder = action === 'send' ? 'sent' : 'drafts';
        
        try {
            const res = await fetch('/api/emails/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ 
                    recipient: document.getElementById('recipient').value, 
                    subject: document.getElementById('subject').value, 
                    body: document.getElementById('body').value, 
                    folder: folder 
                })
            });
            if (res.ok) {
                localStorage.setItem('speakText', action === 'send' ? "Email sent successfully." : "Draft saved successfully.");
                window.location.href = `/${folder}`;
            }
        } catch (err) {
            await speakAloud("Error saving email.");
        }
    }

    // Handle intents and redirect
    function handleIntent(intent, entities, rawText) {
        console.log(`Intent: ${intent}, Entities:`, entities);
        
        if (intent === 'OPEN_FOLDER') {
            const folder = entities.folder || 'inbox';
            localStorage.setItem('speakText', `Opened ${folder}`);
            window.location.href = `/${folder}`;
        } 
        else if (intent === 'SEARCH') {
            const query = entities.query || '';
            localStorage.setItem('speakText', `Searching for ${query}`);
            window.location.href = `/inbox?q=${encodeURIComponent(query)}`;
        } 
        else if (intent === 'CLEAR_SEARCH') {
            localStorage.setItem('speakText', `Cleared search`);
            window.location.href = '/inbox';
        } 
        else if (intent === 'COMPOSE' || intent === 'SEND') {
            if (window.location.pathname === '/compose') {
                composeState = 'ASK_RECIPIENT';
                speakAloud("Tell me the email address whom you want to mail.");
            } else {
                localStorage.setItem('startComposeFlow', 'true');
                window.location.href = '/compose';
            }
        } 
        else if (intent === 'GO_SETTINGS') {
            localStorage.setItem('speakText', `Opened settings`);
            window.location.href = '/settings';
        }
        else {
            // For operations that don't change the page, speak immediately
            speakAloud(`I heard you say ${rawText}, but I am not sure how to do that yet.`);
        }
    }

    async function speakAloud(text) {
        if (!text) return;
        ttsPlaying = true;
        stopListening(); // Stop mic while speaking to avoid hearing itself
        
        try {
            const response = await fetch('/api/speak', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const audioUrl = URL.createObjectURL(blob);
                audioPlayer.src = audioUrl;
                
                audioPlayer.onended = () => {
                    ttsPlaying = false;
                    if (isVoiceMode) startListening();
                };
                
                await audioPlayer.play();
            } else {
                ttsPlaying = false;
                if (isVoiceMode) startListening();
            }
        } catch (error) {
            console.error("TTS error:", error);
            ttsPlaying = false;
            if (isVoiceMode) startListening();
        }
    }

    // Attach event listeners for audio play buttons on emails
    document.querySelectorAll('.btn-read-aloud').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const text = e.target.dataset.text;
            await speakAloud(text);
        });
    });

    const composeForm = document.getElementById('compose-form');
    if (composeForm) {
        composeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const to = document.getElementById('recipient').value;
            const subject = document.getElementById('subject').value;
            const body = document.getElementById('body').value;
            
            try {
                const res = await fetch('/api/emails/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ recipient: to, subject: subject, body: body, folder: 'sent' })
                });
                if (res.ok) {
                    localStorage.setItem('speakText', `Email sent to ${to}`);
                    window.location.href = '/sent';
                }
            } catch (err) {
                alert('Error sending email');
            }
        });

        const saveDraftBtn = document.getElementById('save-draft-btn');
        if (saveDraftBtn) {
            saveDraftBtn.addEventListener('click', async () => {
                const to = document.getElementById('recipient').value;
                const subject = document.getElementById('subject').value;
                const body = document.getElementById('body').value;
                
                try {
                    const res = await fetch('/api/emails/', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ recipient: to, subject: subject, body: body, folder: 'drafts' })
                    });
                    if (res.ok) {
                        localStorage.setItem('speakText', `Draft saved`);
                        window.location.href = '/drafts';
                    }
                } catch (err) {
                    alert('Error saving draft');
                }
            });
        }
    }
});

async function updateEmail(id, data) {
    try {
        await fetch(`/api/emails/${id}`, {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        window.location.reload();
    } catch (err) {
        console.error('Error updating email', err);
    }
}

async function deleteEmail(id) {
    try {
        await fetch(`/api/emails/${id}`, { method: 'DELETE' });
        localStorage.setItem('speakText', `Email deleted`);
        window.location.reload();
    } catch (err) {
        console.error('Error deleting email', err);
    }
}
