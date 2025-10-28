from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import io
import urllib.parse

app = FastAPI(title="VoiceCraft Pro - SAPI4 TTS API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Available voices from Tetyys SAPI4
AVAILABLE_VOICES = [
    "Adult Female #1, American English (TruVoice)",
    "Adult Female #2, American English (TruVoice)",
    "Adult Male #1, American English (TruVoice)",
    "Adult Male #2, American English (TruVoice)",
    "Adult Male #3, American English (TruVoice)",
    "Adult Male #4, American English (TruVoice)",
    "Adult Male #5, American English (TruVoice)",
    "Adult Male #6, American English (TruVoice)",
    "Adult Male #7, American English (TruVoice)",
    "Adult Male #8, American English (TruVoice)",
    "Female Whisper",
    "Male Whisper",
    "Mary",
    "Mary (for Telephone)",
    "Mary in Hall",
    "Mary in Space",
    "Mary in Stadium",
    "Mike",
    "Mike (for Telephone)",
    "Mike in Hall",
    "Mike in Space",
    "Mike in Stadium",
    "RoboSoft Five",
    "RoboSoft Four",
    "RoboSoft One",
    "RoboSoft Six",
    "RoboSoft Three",
    "RoboSoft Two",
    "Sam",
    "Bonzi"
]

# Default settings
DEFAULT_VOICE = "Sam"
DEFAULT_PITCH = 150
DEFAULT_SPEED = 150

@app.get("/")
async def root():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoiceCraft Pro - High Quality TTS API</title>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link rel="stylesheet" href="https://unpkg.com/lucide@latest/dist/umd/lucide.js" />
    <style>
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 85vh;
            display: flex;
            align-items: center;
        }
        .voice-option {
            transition: all 0.2s ease;
        }
        .voice-option:hover {
            background-color: oklch(0.97 0.001 247.858);
        }
    </style>
</head>
<body class="min-h-screen bg-base-100">
    <!-- Navigation -->
    <div class="navbar bg-base-100 border-b border-base-300 sticky top-0 z-50">
        <div class="navbar-start">
            <a class="btn btn-ghost text-xl">
                <i data-lucide="volume-2" class="w-6 h-6 mr-2 text-primary"></i>
                VoiceCraft Pro
            </a>
        </div>
        <div class="navbar-center hidden lg:flex">
            <ul class="menu menu-horizontal px-1">
                <li><a href="#features">Features</a></li>
                <li><a href="#playground">Playground</a></li>
                <li><a href="#voices">Voices</a></li>
                <li><a href="#api">API</a></li>
            </ul>
        </div>
        <div class="navbar-end">
            <a href="#playground" class="btn btn-primary">Try Now</a>
        </div>
    </div>

    <!-- Hero Section -->
    <section class="hero-section text-white">
        <div class="hero-content text-center w-full">
            <div class="max-w-4xl">
                <h1 class="text-6xl font-bold mb-6">VoiceCraft Pro</h1>
                <p class="text-2xl mb-8 opacity-90">
                    High Quality Text-to-Speech API with SAPI4 Voices
                </p>
                <p class="text-xl opacity-80 mb-12 max-w-2xl mx-auto">
                    Free, unlimited TTS service with 30+ professional voices. Perfect for applications, videos, and audio content.
                </p>
                <div class="flex flex-col sm:flex-row gap-4 justify-center">
                    <a href="#playground" class="btn btn-secondary btn-lg text-lg px-8">
                        <i data-lucide="play" class="w-6 h-6 mr-2"></i>
                        Launch Playground
                    </a>
                    <a href="#api" class="btn btn-outline btn-lg text-lg px-8 text-white border-white">
                        <i data-lucide="code" class="w-6 h-6 mr-2"></i>
                        View API Docs
                    </a>
                </div>
                
                <!-- Stats -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
                    <div class="text-center">
                        <div class="text-4xl font-bold mb-2">30+</div>
                        <div class="text-lg opacity-80">Professional Voices</div>
                    </div>
                    <div class="text-center">
                        <div class="text-4xl font-bold mb-2">100%</div>
                        <div class="text-lg opacity-80">Free Forever</div>
                    </div>
                    <div class="text-center">
                        <div class="text-4xl font-bold mb-2">∞</div>
                        <div class="text-lg opacity-80">Unlimited Usage</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-20 bg-base-100">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">Why Choose VoiceCraft Pro?</h2>
            <p class="text-center text-lg text-base-content/70 mb-16 max-w-2xl mx-auto">
                Professional text-to-speech solution with enterprise-grade quality
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="zap" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2 text-center">Lightning Fast</h3>
                        <p class="text-base-content/70">Instant text-to-speech conversion with real-time processing</p>
                    </div>
                </div>
                
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="dollar-sign" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2 text-center">Completely Free</h3>
                        <p class="text-base-content/70">No costs, no limits, no registration required</p>
                    </div>
                </div>
                
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="music" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2 text-center">High Quality MP3</h3>
                        <p class="text-base-content/70">Studio-quality MP3 audio output for all voices</p>
                    </div>
                </div>
                
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="settings" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2 text-center">Customizable</h3>
                        <p class="text-base-content/70">Adjust pitch and speed for perfect audio output</p>
                    </div>
                </div>
                
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="cloud" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2 text-center">Reliable API</h3>
                        <p class="text-base-content/70">99.9% uptime with robust error handling</p>
                    </div>
                </div>
                
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="code" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2 text-center">Easy Integration</h3>
                        <p class="text-base-content/70">Simple REST API with clear documentation</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Playground Section -->
    <section id="playground" class="py-20 bg-base-200">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">TTS Playground</h2>
            <p class="text-center text-lg text-base-content/70 mb-12 max-w-2xl mx-auto">
                Test our text-to-speech engine with different voices and settings
            </p>
            
            <div class="max-w-6xl mx-auto">
                <div class="card bg-base-100">
                    <div class="card-body">
                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                            <!-- Left Column - Settings -->
                            <div class="space-y-6">
                                <!-- Voice Selection -->
                                <div class="form-control">
                                    <label class="label">
                                        <span class="label-text font-bold text-lg">Select Voice</span>
                                    </label>
                                    <select class="select select-bordered select-lg" id="voiceSelect">
                                        ${AVAILABLE_VOICES.map(voice => 
                                            `<option value="${voice}" ${voice === DEFAULT_VOICE ? 'selected' : ''}>${voice}</option>`
                                        ).join('')}
                                    </select>
                                </div>
                                
                                <!-- Pitch Control -->
                                <div class="form-control">
                                    <label class="label">
                                        <span class="label-text font-bold text-lg">Pitch: <span id="pitchValue">${DEFAULT_PITCH}</span></span>
                                    </label>
                                    <input type="range" min="50" max="250" value="${DEFAULT_PITCH}" class="range range-primary" id="pitchSlider" />
                                    <div class="flex justify-between text-xs px-2 mt-1">
                                        <span>Low</span>
                                        <span>Normal</span>
                                        <span>High</span>
                                    </div>
                                </div>
                                
                                <!-- Speed Control -->
                                <div class="form-control">
                                    <label class="label">
                                        <span class="label-text font-bold text-lg">Speed: <span id="speedValue">${DEFAULT_SPEED}</span></span>
                                    </label>
                                    <input type="range" min="50" max="250" value="${DEFAULT_SPEED}" class="range range-primary" id="speedSlider" />
                                    <div class="flex justify-between text-xs px-2 mt-1">
                                        <span>Slow</span>
                                        <span>Normal</span>
                                        <span>Fast</span>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Right Column - Text Input -->
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text font-bold text-lg">Enter Text</span>
                                    <span class="label-text-alt" id="charCount">0/1000</span>
                                </label>
                                <textarea class="textarea textarea-bordered h-48 text-lg" id="textInput" 
                                       placeholder="Enter text to convert to speech (max 1000 characters)">Hello! Welcome to VoiceCraft Pro - your free, unlimited text-to-speech service with high quality MP3 output.</textarea>
                            </div>
                        </div>
                        
                        <!-- Convert Button -->
                        <div class="form-control mt-8">
                            <button class="btn btn-primary btn-lg text-lg" id="convertBtn">
                                <i data-lucide="volume-2" class="w-6 h-6 mr-2"></i>
                                Generate MP3 Audio
                            </button>
                        </div>
                        
                        <!-- Audio Player -->
                        <div class="mt-8 hidden" id="audioSection">
                            <label class="label">
                                <span class="label-text font-bold text-lg">Generated Audio</span>
                            </label>
                            <div class="bg-base-200 p-6 rounded-lg">
                                <audio controls class="w-full" id="audioPlayer"></audio>
                                <div class="mt-4 flex flex-wrap gap-2">
                                    <a class="btn btn-outline btn-sm" id="downloadBtn">
                                        <i data-lucide="download" class="w-4 h-4 mr-1"></i>
                                        Download MP3
                                    </a>
                                    <div class="badge badge-success badge-lg" id="generationInfo"></div>
                                    <div class="badge badge-info badge-lg" id="voiceInfo"></div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Error Message -->
                        <div class="alert alert-error mt-6 hidden" id="errorAlert">
                            <i data-lucide="alert-circle" class="w-6 h-6"></i>
                            <span id="errorMessage"></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Voices Section -->
    <section id="voices" class="py-20 bg-base-100">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">Available Voices</h2>
            <p class="text-center text-lg text-base-content/70 mb-12 max-w-2xl mx-auto">
                Choose from 30+ professional SAPI4 voices with unique characteristics
            </p>
            
            <div class="max-w-6xl mx-auto">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    ${AVAILABLE_VOICES.map(voice => `
                        <div class="card bg-base-200 voice-option cursor-pointer" data-voice="${voice}">
                            <div class="card-body py-4">
                                <h3 class="card-title text-sm">${voice}</h3>
                                <div class="card-actions justify-end">
                                    <button class="btn btn-xs btn-outline try-voice" data-voice="${voice}">
                                        <i data-lucide="play" class="w-3 h-3 mr-1"></i>
                                        Try
                                    </button>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    </section>

    <!-- API Documentation -->
    <section id="api" class="py-20 bg-base-200">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">API Documentation</h2>
            <p class="text-center text-lg text-base-content/70 mb-12 max-w-2xl mx-auto">
                Simple REST API for integrating text-to-speech into your applications
            </p>
            
            <div class="max-w-4xl mx-auto space-y-8">
                <!-- Base URL -->
                <div class="card bg-base-100">
                    <div class="card-body">
                        <h3 class="card-title mb-4">
                            <i data-lucide="link" class="w-6 h-6 text-primary"></i>
                            Base URL
                        </h3>
                        <div class="mockup-code bg-neutral text-neutral-content">
                            <pre><code>https://voicecraft-pro.vercel.app</code></pre>
                        </div>
                    </div>
                </div>
                
                <!-- TTS Endpoint -->
                <div class="card bg-base-100">
                    <div class="card-body">
                        <h3 class="card-title mb-4">
                            <i data-lucide="mic" class="w-6 h-6 text-primary"></i>
                            Text-to-Speech Endpoint
                        </h3>
                        <div class="mockup-code bg-neutral text-neutral-content">
                            <pre><code>GET /api/tts?voice=VOICE_NAME&text=YOUR_TEXT&pitch=150&speed=150</code></pre>
                        </div>
                        <div class="mt-4">
                            <h4 class="font-bold mb-2">Parameters:</h4>
                            <ul class="list-disc list-inside space-y-1">
                                <li><code>voice</code> (required) - Voice name from available list</li>
                                <li><code>text</code> (required) - Text to convert (max 1000 characters)</li>
                                <li><code>pitch</code> (optional) - Pitch value 50-250 (default: 150)</li>
                                <li><code>speed</code> (optional) - Speed value 50-250 (default: 150)</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Code Examples -->
                <div class="card bg-base-100">
                    <div class="card-body">
                        <h3 class="card-title mb-4">
                            <i data-lucide="code" class="w-6 h-6 text-primary"></i>
                            Code Examples
                        </h3>
                        
                        <div class="tabs tabs-boxed mb-4">
                            <a class="tab tab-active" data-tab="javascript">JavaScript</a>
                            <a class="tab" data-tab="python">Python</a>
                            <a class="tab" data-tab="curl">cURL</a>
                        </div>
                        
                        <div class="tab-content">
                            <div class="tab-pane active" id="javascript">
                                <div class="mockup-code bg-neutral text-neutral-content">
                                    <pre><code>const response = await fetch('/api/tts?voice=Sam&text=Hello world&pitch=150&speed=150');
const audioBlob = await response.blob();
const audioUrl = URL.createObjectURL(audioBlob);
const audio = new Audio(audioUrl);
audio.play();</code></pre>
                                </div>
                            </div>
                            <div class="tab-pane hidden" id="python">
                                <div class="mockup-code bg-neutral text-neutral-content">
                                    <pre><code>import requests

url = 'https://voicecraft-pro.vercel.app/api/tts'
params = {
    'voice': 'Sam',
    'text': 'Hello world',
    'pitch': 150,
    'speed': 150
}

response = requests.get(url, params=params)
with open('audio.mp3', 'wb') as f:
    f.write(response.content)</code></pre>
                                </div>
                            </div>
                            <div class="tab-pane hidden" id="curl">
                                <div class="mockup-code bg-neutral text-neutral-content">
                                    <pre><code>curl "https://voicecraft-pro.vercel.app/api/tts?voice=Sam&text=Hello%20world&pitch=150&speed=150" -o audio.mp3</code></pre>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer footer-center p-10 bg-base-300 text-base-content">
        <aside>
            <div class="flex items-center justify-center mb-4">
                <i data-lucide="volume-2" class="w-8 h-8 text-primary mr-2"></i>
                <p class="text-xl font-bold">VoiceCraft Pro</p>
            </div>
            <p>Free • Unlimited • High Quality TTS Service</p>
            <p class="mt-2">Powered by SAPI4 • MP3 Output • Professional Voices</p>
        </aside>
    </footer>

    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <script>
        // Initialize Lucide icons
        lucide.createIcons();
        
        // Available voices array
        const AVAILABLE_VOICES = ${JSON.stringify(AVAILABLE_VOICES)};
        
        // Character counter
        const textInput = document.getElementById('textInput');
        const charCount = document.getElementById('charCount');
        
        textInput.addEventListener('input', () => {
            const length = textInput.value.length;
            charCount.textContent = `${length}/1000`;
            if (length > 1000) {
                charCount.classList.add('text-error');
            } else {
                charCount.classList.remove('text-error');
            }
        });
        
        // Pitch and speed sliders
        const pitchSlider = document.getElementById('pitchSlider');
        const pitchValue = document.getElementById('pitchValue');
        const speedSlider = document.getElementById('speedSlider');
        const speedValue = document.getElementById('speedValue');
        
        pitchSlider.addEventListener('input', () => {
            pitchValue.textContent = pitchSlider.value;
        });
        
        speedSlider.addEventListener('input', () => {
            speedValue.textContent = speedSlider.value;
        });
        
        // Voice selection cards
        document.querySelectorAll('.voice-option').forEach(card => {
            card.addEventListener('click', () => {
                const voice = card.getAttribute('data-voice');
                document.getElementById('voiceSelect').value = voice;
            });
        });
        
        // Try voice buttons
        document.querySelectorAll('.try-voice').forEach(button => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                const voice = button.getAttribute('data-voice');
                document.getElementById('voiceSelect').value = voice;
                document.getElementById('textInput').value = `This is a demonstration of the ${voice} voice.`;
                document.getElementById('convertBtn').click();
            });
        });
        
        // Tab functionality
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                // Remove active class from all tabs and panes
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('tab-active'));
                document.querySelectorAll('.tab-pane').forEach(p => p.classList.add('hidden'));
                
                // Add active class to clicked tab
                tab.classList.add('tab-active');
                
                // Show corresponding pane
                const tabId = tab.getAttribute('data-tab');
                document.getElementById(tabId).classList.remove('hidden');
            });
        });
        
        // TTS Conversion
        document.getElementById('convertBtn').addEventListener('click', async () => {
            const voice = document.getElementById('voiceSelect').value;
            const text = document.getElementById('textInput').value;
            const pitch = document.getElementById('pitchSlider').value;
            const speed = document.getElementById('speedSlider').value;
            const convertBtn = document.getElementById('convertBtn');
            const audioSection = document.getElementById('audioSection');
            const errorAlert = document.getElementById('errorAlert');
            const generationInfo = document.getElementById('generationInfo');
            const voiceInfo = document.getElementById('voiceInfo');
            
            if (!text.trim()) {
                showError('Please enter some text to convert');
                return;
            }
            
            if (text.length > 1000) {
                showError('Text must be 1000 characters or less');
                return;
            }
            
            // Show loading state
            convertBtn.innerHTML = '<i data-lucide="loader" class="w-6 h-6 mr-2 animate-spin"></i>Generating...';
            convertBtn.disabled = true;
            errorAlert.classList.add('hidden');
            
            try {
                const response = await fetch(`/api/tts?voice=${encodeURIComponent(voice)}&text=${encodeURIComponent(text)}&pitch=${pitch}&speed=${speed}`);
                
                if (response.ok) {
                    const audioBlob = await response.blob();
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audioPlayer = document.getElementById('audioPlayer');
                    const downloadBtn = document.getElementById('downloadBtn');
                    
                    audioPlayer.src = audioUrl;
                    audioSection.classList.remove('hidden');
                    
                    // Set up download
                    const fileName = `voicecraft-${voice.replace(/[^a-zA-Z0-9]/g, '-')}-${Date.now()}.mp3`;
                    downloadBtn.href = audioUrl;
                    downloadBtn.download = fileName;
                    
                    // Show generation info
                    const sizeKB = (audioBlob.size / 1024).toFixed(1);
                    generationInfo.textContent = `${sizeKB} KB • MP3`;
                    voiceInfo.textContent = voice;
                    
                    // Scroll to audio section
                    audioSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                } else {
                    const errorData = await response.json();
                    showError(errorData.message || 'Failed to generate speech');
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            } finally {
                // Reset button
                convertBtn.innerHTML = '<i data-lucide="volume-2" class="w-6 h-6 mr-2"></i>Generate MP3 Audio';
                convertBtn.disabled = false;
                lucide.createIcons(); // Re-initialize icons
            }
        });
        
        function showError(message) {
            const errorAlert = document.getElementById('errorAlert');
            const errorMessage = document.getElementById('errorMessage');
            
            errorMessage.textContent = message;
            errorAlert.classList.remove('hidden');
            errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        
        // Smooth scroll for navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/tts")
async def text_to_speech_api(voice: str = "", text: str = "", pitch: int = 150, speed: int = 150):
    if not voice or not text or voice.strip() == "" or text.strip() == "":
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": "Voice and text parameters are required"
            },
            status_code=400
        )
    
    # Validate text length
    if len(text) > 1000:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": "Text must be 1000 characters or less"
            },
            status_code=400
        )
    
    # Validate voice
    if voice not in AVAILABLE_VOICES:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": f"Voice '{voice}' is not available. Please use one of the supported voices."
            },
            status_code=400
        )
    
    # Validate pitch and speed ranges
    if pitch < 50 or pitch > 250 or speed < 50 or speed > 250:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": "Pitch and speed must be between 50 and 250"
            },
            status_code=400
        )
    
    try:
        # Encode parameters for URL
        encoded_voice = urllib.parse.quote(voice)
        encoded_text = urllib.parse.quote(text)
        
        # Build Tetyys API URL
        tetyys_url = f"https://www.tetyys.com/SAPI4/SAPI4?text={encoded_text}&voice={encoded_voice}&pitch={pitch}&speed={speed}"
        
        # Make request to Tetyys API
        response = requests.get(tetyys_url, timeout=30)
        
        if response.status_code == 200:
            # Get the audio content
            audio_content = response.content
            
            # Create in-memory file-like object
            audio_buffer = io.BytesIO(audio_content)
            
            return StreamingResponse(
                audio_buffer,
                media_type="audio/mpeg",
                headers={
                    "Content-Disposition": "inline; filename=voicecraft-audio.mp3",
                    "X-Generated-By": "VoiceCraft Pro",
                    "X-Voice-Used": voice,
                    "X-Pitch": str(pitch),
                    "X-Speed": str(speed)
                }
            )
        else:
            return JSONResponse(
                content={
                    "status": False,
                    "status_code": response.status_code,
                    "message": f"TTS service returned error: {response.status_code}"
                },
                status_code=response.status_code
            )
        
    except requests.exceptions.Timeout:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 408,
                "message": "TTS service timeout"
            },
            status_code=408
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 500,
                "message": f"Error generating speech: {str(e)}"
            },
            status_code=500
        )

@app.get("/api/voices")
async def list_voices_api():
    return JSONResponse(
        content={
            "status": True,
            "status_code": 200,
            "voices": AVAILABLE_VOICES,
            "total_voices": len(AVAILABLE_VOICES),
            "default_voice": DEFAULT_VOICE,
            "default_pitch": DEFAULT_PITCH,
            "default_speed": DEFAULT_SPEED
        }
    )

@app.get("/api/health")
async def health_check():
    return JSONResponse(
        content={
            "status": True,
            "status_code": 200,
            "message": "VoiceCraft Pro is healthy",
            "version": "1.0.0",
            "service": "SAPI4 TTS API",
            "features": ["Free", "Unlimited", "MP3 Output", "30+ Voices", "Customizable"]
        }
    )

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        content={
            "status": False,
            "status_code": 404,
            "message": "Endpoint not found"
        },
        status_code=404
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        content={
            "status": False,
            "status_code": 500,
            "message": "Internal server error"
        },
        status_code=500
    )
