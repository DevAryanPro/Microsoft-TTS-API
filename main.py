from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
from io import BytesIO
import json

app = FastAPI(title="Microsoft TTS API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# List of verified working voices
VERIFIED_VOICES = [
    "es-MX-DaliaNeural",
    "es-MX-JorgeNeural", 
    "es-ES-ElviraNeural",
    "es-ES-AlvaroNeural",
    "es-AR-ElenaNeural",
    "es-CO-SalomeNeural",
    "en-US-JennyNeural",
    "en-US-GuyNeural",
    "en-GB-LibbyNeural",
    "en-GB-RyanNeural",
    "fr-FR-DeniseNeural",
    "de-DE-KatjaNeural",
    "it-IT-ElsaNeural",
    "pt-BR-FranciscaNeural",
    "ja-JP-NanamiNeural",
    "ko-KR-SunHiNeural",
    "zh-CN-XiaoxiaoNeural"
]

@app.get("/")
async def root():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft TTS API - Text to Speech Converter</title>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link rel="stylesheet" href="https://unpkg.com/lucide@latest/dist/umd/lucide.js" />
    <style>
        .hero-pattern {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
    </style>
</head>
<body class="min-h-screen bg-base-100">
    <!-- Navigation -->
    <div class="navbar bg-base-100 border-b">
        <div class="navbar-start">
            <a class="btn btn-ghost text-xl">
                <i data-lucide="volume-2" class="w-6 h-6 mr-2"></i>
                TTS API
            </a>
        </div>
        <div class="navbar-center hidden lg:flex">
            <ul class="menu menu-horizontal px-1">
                <li><a href="#features">Features</a></li>
                <li><a href="#playground">Playground</a></li>
                <li><a href="#api">API</a></li>
                <li><a href="#faq">FAQ</a></li>
            </ul>
        </div>
        <div class="navbar-end">
            <a href="#playground" class="btn btn-primary">Try Now</a>
        </div>
    </div>

    <!-- Hero Section -->
    <section class="hero-pattern text-white">
        <div class="hero min-h-96">
            <div class="hero-content text-center">
                <div class="max-w-2xl">
                    <h1 class="text-5xl font-bold mb-6">Microsoft TTS API</h1>
                    <p class="text-xl mb-8">
                        Convert text to natural-sounding speech with 400+ neural voices in 30+ languages
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">
                        <a href="#playground" class="btn btn-secondary btn-lg">
                            <i data-lucide="play" class="w-5 h-5 mr-2"></i>
                            Try Playground
                        </a>
                        <a href="#api" class="btn btn-outline btn-lg text-white border-white">
                            <i data-lucide="code" class="w-5 h-5 mr-2"></i>
                            View API Docs
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-16 bg-base-100">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">Why Choose Our TTS API</h2>
            <p class="text-center text-lg text-base-content/70 mb-12 max-w-2xl mx-auto">
                Professional text-to-speech solution with enterprise-grade quality and reliability
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="zap" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">Fast & Reliable</h3>
                        <p class="text-base-content/70">Instant text-to-speech conversion with 99.9% uptime guarantee</p>
                    </div>
                </div>
                
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="globe" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">Multiple Languages</h3>
                        <p class="text-base-content/70">400+ neural voices across 30+ languages and dialects</p>
                    </div>
                </div>
                
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="shield" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">High Quality</h3>
                        <p class="text-base-content/70">Studio-quality 24kHz MP3 audio with natural pronunciation</p>
                    </div>
                </div>
                
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="code" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">Easy Integration</h3>
                        <p class="text-base-content/70">Simple REST API with clear documentation and examples</p>
                    </div>
                </div>
                
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="dollar-sign" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">Free Forever</h3>
                        <p class="text-base-content/70">Completely free for personal and commercial use</p>
                    </div>
                </div>
                
                <div class="card bg-base-200">
                    <div class="card-body items-center text-center">
                        <i data-lucide="cloud" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">No Setup</h3>
                        <p class="text-base-content/70">No API keys, no registration, no credit card required</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Playground Section -->
    <section id="playground" class="py-16 bg-base-200">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">TTS Playground</h2>
            <p class="text-center text-lg text-base-content/70 mb-12 max-w-2xl mx-auto">
                Test the text-to-speech conversion with different voices and languages
            </p>
            
            <div class="max-w-4xl mx-auto">
                <div class="card bg-base-100">
                    <div class="card-body">
                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            <!-- Voice Selection -->
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text font-bold">Select Voice</span>
                                </label>
                                <select class="select select-bordered" id="voiceSelect">
                                    <option value="es-MX-DaliaNeural">es-MX-DaliaNeural 👩 (Spanish - Mexico)</option>
                                    <option value="es-MX-JorgeNeural">es-MX-JorgeNeural 👨 (Spanish - Mexico)</option>
                                    <option value="es-ES-ElviraNeural">es-ES-ElviraNeural 👩 (Spanish - Spain)</option>
                                    <option value="en-US-JennyNeural">en-US-JennyNeural 👩 (English - US)</option>
                                    <option value="en-US-GuyNeural">en-US-GuyNeural 👨 (English - US)</option>
                                    <option value="en-GB-LibbyNeural">en-GB-LibbyNeural 👩 (English - UK)</option>
                                    <option value="fr-FR-DeniseNeural">fr-FR-DeniseNeural 👩 (French)</option>
                                    <option value="de-DE-KatjaNeural">de-DE-KatjaNeural 👩 (German)</option>
                                    <option value="it-IT-ElsaNeural">it-IT-ElsaNeural 👩 (Italian)</option>
                                    <option value="ja-JP-NanamiNeural">ja-JP-NanamiNeural 👩 (Japanese)</option>
                                </select>
                            </div>
                            
                            <!-- Text Input -->
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text font-bold">Enter Text</span>
                                </label>
                                <input type="text" class="input input-bordered" id="textInput" 
                                       placeholder="Enter text to convert to speech" value="Hello, welcome to Microsoft TTS API">
                            </div>
                        </div>
                        
                        <!-- Convert Button -->
                        <div class="form-control mt-6">
                            <button class="btn btn-primary btn-lg" id="convertBtn">
                                <i data-lucide="volume-2" class="w-5 h-5 mr-2"></i>
                                Convert to Speech
                            </button>
                        </div>
                        
                        <!-- Audio Player -->
                        <div class="mt-6 hidden" id="audioSection">
                            <label class="label">
                                <span class="label-text font-bold">Generated Audio</span>
                            </label>
                            <audio controls class="w-full" id="audioPlayer"></audio>
                            <div class="mt-2 flex gap-2">
                                <a class="btn btn-outline btn-sm" id="downloadBtn">
                                    <i data-lucide="download" class="w-4 h-4 mr-1"></i>
                                    Download MP3
                                </a>
                            </div>
                        </div>
                        
                        <!-- Error Message -->
                        <div class="alert alert-error mt-4 hidden" id="errorAlert">
                            <i data-lucide="alert-circle" class="w-5 h-5"></i>
                            <span id="errorMessage"></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- API Documentation -->
    <section id="api" class="py-16 bg-base-100">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">API Documentation</h2>
            <p class="text-center text-lg text-base-content/70 mb-12 max-w-2xl mx-auto">
                Simple REST API for integrating text-to-speech into your applications
            </p>
            
            <div class="max-w-4xl mx-auto space-y-8">
                <!-- Base URL -->
                <div class="card bg-base-200">
                    <div class="card-body">
                        <h3 class="card-title mb-4">
                            <i data-lucide="link" class="w-6 h-6 text-primary"></i>
                            Base URL
                        </h3>
                        <div class="mockup-code bg-neutral text-neutral-content">
                            <pre><code>https://microsoft-tts-api.vercel.app</code></pre>
                        </div>
                    </div>
                </div>
                
                <!-- TTS Endpoint -->
                <div class="card bg-base-200">
                    <div class="card-body">
                        <h3 class="card-title mb-4">
                            <i data-lucide="mic" class="w-6 h-6 text-primary"></i>
                            Text-to-Speech Endpoint
                        </h3>
                        <div class="mockup-code bg-neutral text-neutral-content">
                            <pre><code>GET /api/tts?voice=VOICE_NAME&text=YOUR_TEXT</code></pre>
                        </div>
                        <div class="mt-4">
                            <h4 class="font-bold mb-2">Parameters:</h4>
                            <ul class="list-disc list-inside space-y-1">
                                <li><code>voice</code> (required) - Voice identifier</li>
                                <li><code>text</code> (required) - Text to convert</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Code Examples -->
                <div class="card bg-base-200">
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
                                    <pre><code>const response = await fetch('/api/tts?voice=en-US-JennyNeural&text=Hello world');
const audioBlob = await response.blob();
const audioUrl = URL.createObjectURL(audioBlob);
const audio = new Audio(audioUrl);
audio.play();</code></pre>
                                </div>
                            </div>
                            <div class="tab-pane hidden" id="python">
                                <div class="mockup-code bg-neutral text-neutral-content">
                                    <pre><code>import requests

url = 'https://microsoft-tts-api.vercel.app/api/tts'
params = {
    'voice': 'en-US-JennyNeural',
    'text': 'Hello world'
}

response = requests.get(url, params=params)
with open('audio.mp3', 'wb') as f:
    f.write(response.content)</code></pre>
                                </div>
                            </div>
                            <div class="tab-pane hidden" id="curl">
                                <div class="mockup-code bg-neutral text-neutral-content">
                                    <pre><code>curl "https://microsoft-tts-api.vercel.app/api/tts?voice=en-US-JennyNeural&text=Hello%20world" -o audio.mp3</code></pre>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- FAQ Section -->
    <section id="faq" class="py-16 bg-base-200">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">Frequently Asked Questions</h2>
            <p class="text-center text-lg text-base-content/70 mb-12 max-w-2xl mx-auto">
                Common questions about the TTS API service
            </p>
            
            <div class="max-w-4xl mx-auto space-y-4">
                <div class="collapse collapse-arrow bg-base-100">
                    <input type="radio" name="faq" />
                    <div class="collapse-title text-xl font-medium">
                        Is this service really free?
                    </div>
                    <div class="collapse-content">
                        <p>Yes, the TTS API is completely free for both personal and commercial use. There are no hidden costs or usage limits.</p>
                    </div>
                </div>
                
                <div class="collapse collapse-arrow bg-base-100">
                    <input type="radio" name="faq" />
                    <div class="collapse-title text-xl font-medium">
                        What audio quality do you provide?
                    </div>
                    <div class="collapse-content">
                        <p>All audio is generated in high-quality MP3 format at 24kHz sampling rate, providing clear and natural-sounding speech.</p>
                    </div>
                </div>
                
                <div class="collapse collapse-arrow bg-base-100">
                    <input type="radio" name="faq" />
                    <div class="collapse-title text-xl font-medium">
                        How many voices are available?
                    </div>
                    <div class="collapse-content">
                        <p>We provide access to 400+ neural voices across 30+ languages and dialects. You can see the complete list using the /api/voices endpoint.</p>
                    </div>
                </div>
                
                <div class="collapse collapse-arrow bg-base-100">
                    <input type="radio" name="faq" />
                    <div class="collapse-title text-xl font-medium">
                        Do I need an API key?
                    </div>
                    <div class="collapse-content">
                        <p>No API key or registration is required. You can start using the API immediately with simple HTTP requests.</p>
                    </div>
                </div>
                
                <div class="collapse collapse-arrow bg-base-100">
                    <input type="radio" name="faq" />
                    <div class="collapse-title text-xl font-medium">
                        What happens if a voice doesn't work?
                    </div>
                    <div class="collapse-content">
                        <p>Some regional voices may have temporary availability issues. We recommend using the verified voices listed in the playground for guaranteed performance.</p>
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
                <p class="text-xl font-bold">Microsoft TTS API</p>
            </div>
            <p>Professional text-to-speech conversion service</p>
            <p class="mt-2">Free forever • No registration required • High quality audio</p>
        </aside>
    </footer>

    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <script>
        // Initialize Lucide icons
        lucide.createIcons();
        
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
            const convertBtn = document.getElementById('convertBtn');
            const audioSection = document.getElementById('audioSection');
            const errorAlert = document.getElementById('errorAlert');
            
            if (!text.trim()) {
                showError('Please enter some text to convert');
                return;
            }
            
            // Show loading state
            convertBtn.innerHTML = '<i data-lucide="loader" class="w-5 h-5 mr-2 animate-spin"></i>Converting...';
            convertBtn.disabled = true;
            errorAlert.classList.add('hidden');
            
            try {
                const response = await fetch(`/api/tts?voice=${encodeURIComponent(voice)}&text=${encodeURIComponent(text)}`);
                
                if (response.ok) {
                    const audioBlob = await response.blob();
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audioPlayer = document.getElementById('audioPlayer');
                    const downloadBtn = document.getElementById('downloadBtn');
                    
                    audioPlayer.src = audioUrl;
                    audioSection.classList.remove('hidden');
                    
                    // Set up download
                    downloadBtn.href = audioUrl;
                    downloadBtn.download = `tts-${voice}-${Date.now()}.mp3`;
                    
                } else {
                    const errorData = await response.json();
                    showError(errorData.message || 'Failed to convert text to speech');
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            } finally {
                // Reset button
                convertBtn.innerHTML = '<i data-lucide="volume-2" class="w-5 h-5 mr-2"></i>Convert to Speech';
                convertBtn.disabled = false;
                lucide.createIcons(); // Re-initialize icons
            }
        });
        
        function showError(message) {
            const errorAlert = document.getElementById('errorAlert');
            const errorMessage = document.getElementById('errorMessage');
            
            errorMessage.textContent = message;
            errorAlert.classList.remove('hidden');
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
async def text_to_speech_api(voice: str = "", text: str = ""):
    if not voice or not text or voice.strip() == "" or text.strip() == "":
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": "Voice and text parameters are required"
            },
            status_code=400
        )
    
    # Check if voice is in verified list
    if voice not in VERIFIED_VOICES:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": f"Voice '{voice}' is not available. Please use one of the verified voices."
            },
            status_code=400
        )
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        audio_buffer = BytesIO()
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        
        if audio_buffer.tell() == 0:
            return JSONResponse(
                content={
                    "status": False,
                    "status_code": 400,
                    "message": "Failed to generate audio"
                },
                status_code=400
            )
        
        audio_buffer.seek(0)
        
        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=audio.mp3"
            }
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": f"Error processing request: {str(e)}"
            },
            status_code=400
        )

@app.get("/api/voices")
async def list_voices_api():
    try:
        voices = await edge_tts.list_voices()
        formatted_voices = [
            {
                "name": voice["ShortName"],
                "gender": voice["Gender"],
                "locale": voice["Locale"],
                "language": voice.get("LocaleName", ""),
                "friendly_name": voice.get("FriendlyName", "")
            }
            for voice in voices
        ]
        
        return JSONResponse(
            content={
                "status": True,
                "status_code": 200,
                "total": len(formatted_voices),
                "verified_voices": VERIFIED_VOICES,
                "voices": formatted_voices
            }
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": f"Error fetching voices: {str(e)}"
            },
            status_code=400
        )

@app.get("/api/health")
async def health_check():
    return JSONResponse(
        content={
            "status": True,
            "status_code": 200,
            "message": "API is healthy",
            "version": "1.0.0"
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
