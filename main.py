from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from TTS.api import TTS
import os
import io
import tempfile
from pathlib import Path
import uuid

app = FastAPI(title="VoiceCraft AI - Offline TTS API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Available Coqui TTS models
AVAILABLE_MODELS = {
    "english": {
        "tts_models/en/ljspeech/tacotron2-DDC": "Standard English - High Quality",
        "tts_models/en/ljspeech/glow-tts": "English - GlowTTS",
        "tts_models/en/ljspeech/speedy-speech": "English - Fast Generation",
        "tts_models/en/ljspeech/tacotron2-DCA": "English - DCA",
        "tts_models/en/vctk/vits": "English - Multi-speaker (VCTK)",
        "tts_models/en/vctk/fast_pitch": "English - FastPitch",
    },
    "multilingual": {
        "tts_models/multilingual/multi-dataset/your_tts": "Multilingual - YourTTS",
        "tts_models/multilingual/multi-dataset/bark": "Multilingual - Bark",
    },
    "other": {
        "tts_models/de/thorsten/tacotron2-DDC": "German - Thorsten",
        "tts_models/fr/css10/vits": "French - CSS10",
        "tts_models/es/css10/vits": "Spanish - CSS10",
        "tts_models/ru/css10/vits": "Russian - CSS10",
        "tts_models/zh-CN/baker/tacotron2-DDC": "Chinese - Baker",
        "tts_models/ja/kokoro/tacotron2-DDC": "Japanese - Kokoro",
    }
}

# Default model for quick start
DEFAULT_MODEL = "tts_models/en/ljspeech/tacotron2-DDC"

@app.get("/")
async def root():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoiceCraft AI - Offline Text to Speech</title>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link rel="stylesheet" href="https://unpkg.com/lucide@latest/dist/umd/lucide.js" />
    <style>
        .hero-gradient {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .feature-card {
            transition: transform 0.2s ease-in-out;
        }
        .feature-card:hover {
            transform: translateY(-2px);
        }
    </style>
</head>
<body class="min-h-screen bg-base-100">
    <!-- Navigation -->
    <div class="navbar bg-base-100 border-b border-base-300">
        <div class="navbar-start">
            <a class="btn btn-ghost text-xl">
                <i data-lucide="mic" class="w-6 h-6 mr-2 text-primary"></i>
                VoiceCraft AI
            </a>
        </div>
        <div class="navbar-center hidden lg:flex">
            <ul class="menu menu-horizontal px-1">
                <li><a href="#features">Features</a></li>
                <li><a href="#playground">Playground</a></li>
                <li><a href="#models">Models</a></li>
                <li><a href="#api">API</a></li>
                <li><a href="#faq">FAQ</a></li>
            </ul>
        </div>
        <div class="navbar-end">
            <a href="#playground" class="btn btn-primary">Try Now</a>
        </div>
    </div>

    <!-- Hero Section -->
    <section class="hero-gradient text-white">
        <div class="hero min-h-96">
            <div class="hero-content text-center">
                <div class="max-w-2xl">
                    <h1 class="text-5xl font-bold mb-6">VoiceCraft AI</h1>
                    <p class="text-xl mb-8">
                        Offline Text-to-Speech API with 100% Free & Unlimited Usage
                    </p>
                    <p class="text-lg opacity-90 mb-8">
                        Powered by Coqui TTS • No Internet Required • Complete Privacy
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">
                        <a href="#playground" class="btn btn-secondary btn-lg">
                            <i data-lucide="play" class="w-5 h-5 mr-2"></i>
                            Launch Playground
                        </a>
                        <a href="#api" class="btn btn-outline btn-lg text-white border-white">
                            <i data-lucide="code" class="w-5 h-5 mr-2"></i>
                            API Documentation
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-16 bg-base-100">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">Why VoiceCraft AI?</h2>
            <p class="text-center text-lg text-base-content/70 mb-12 max-w-2xl mx-auto">
                Enterprise-grade text-to-speech with complete offline capability
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div class="card bg-base-200 feature-card">
                    <div class="card-body items-center text-center">
                        <i data-lucide="wifi-off" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">100% Offline</h3>
                        <p class="text-base-content/70">Works completely offline - no internet connection required after setup</p>
                    </div>
                </div>
                
                <div class="card bg-base-200 feature-card">
                    <div class="card-body items-center text-center">
                        <i data-lucide="infinity" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">Unlimited Free</h3>
                        <p class="text-base-content/70">Completely free forever with no usage limits or API restrictions</p>
                    </div>
                </div>
                
                <div class="card bg-base-200 feature-card">
                    <div class="card-body items-center text-center">
                        <i data-lucide="shield" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">Complete Privacy</h3>
                        <p class="text-base-content/70">Your data never leaves your server - maximum security and privacy</p>
                    </div>
                </div>
                
                <div class="card bg-base-200 feature-card">
                    <div class="card-body items-center text-center">
                        <i data-lucide="zap" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">Fast Generation</h3>
                        <p class="text-base-content/70">Optimized models for quick text-to-speech conversion</p>
                    </div>
                </div>
                
                <div class="card bg-base-200 feature-card">
                    <div class="card-body items-center text-center">
                        <i data-lucide="globe" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">Multiple Languages</h3>
                        <p class="text-base-content/70">Support for English, Spanish, French, German, and more</p>
                    </div>
                </div>
                
                <div class="card bg-base-200 feature-card">
                    <div class="card-body items-center text-center">
                        <i data-lucide="code" class="w-12 h-12 text-primary mb-4"></i>
                        <h3 class="card-title mb-2">Easy Integration</h3>
                        <p class="text-base-content/70">Simple REST API with clear documentation and examples</p>
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
                Test our offline text-to-speech engine with different models
            </p>
            
            <div class="max-w-4xl mx-auto">
                <div class="card bg-base-100">
                    <div class="card-body">
                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            <!-- Model Selection -->
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text font-bold">Select Model</span>
                                </label>
                                <select class="select select-bordered" id="modelSelect">
                                    <optgroup label="English Models">
                                        <option value="tts_models/en/ljspeech/tacotron2-DDC" selected>Standard English - High Quality</option>
                                        <option value="tts_models/en/ljspeech/glow-tts">English - GlowTTS</option>
                                        <option value="tts_models/en/ljspeech/speedy-speech">English - Fast Generation</option>
                                        <option value="tts_models/en/vctk/vits">English - Multi-speaker (VCTK)</option>
                                    </optgroup>
                                    <optgroup label="Other Languages">
                                        <option value="tts_models/es/css10/vits">Spanish - CSS10</option>
                                        <option value="tts_models/fr/css10/vits">French - CSS10</option>
                                        <option value="tts_models/de/thorsten/tacotron2-DDC">German - Thorsten</option>
                                        <option value="tts_models/ja/kokoro/tacotron2-DDC">Japanese - Kokoro</option>
                                    </optgroup>
                                </select>
                            </div>
                            
                            <!-- Text Input -->
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text font-bold">Enter Text</span>
                                    <span class="label-text-alt" id="charCount">0/500</span>
                                </label>
                                <textarea class="textarea textarea-bordered h-24" id="textInput" 
                                       placeholder="Enter text to convert to speech (max 500 characters)">Hello! Welcome to VoiceCraft AI - your free, unlimited, offline text-to-speech service.</textarea>
                            </div>
                        </div>
                        
                        <!-- Convert Button -->
                        <div class="form-control mt-6">
                            <button class="btn btn-primary btn-lg" id="convertBtn">
                                <i data-lucide="volume-2" class="w-5 h-5 mr-2"></i>
                                Generate Speech
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
                                    Download WAV
                                </a>
                                <div class="badge badge-success" id="generationInfo"></div>
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

    <!-- Models Section -->
    <section id="models" class="py-16 bg-base-100">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">Available Models</h2>
            <p class="text-center text-lg text-base-content/70 mb-12 max-w-2xl mx-auto">
                Choose from various pre-trained TTS models optimized for different use cases
            </p>
            
            <div class="max-w-6xl mx-auto">
                <!-- English Models -->
                <div class="mb-8">
                    <h3 class="text-2xl font-bold mb-4">🇺🇸 English Models</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="card bg-base-200">
                            <div class="card-body">
                                <h4 class="card-title">tts_models/en/ljspeech/tacotron2-DDC</h4>
                                <p class="text-sm text-base-content/70">Standard high-quality English TTS with good voice naturalness</p>
                                <div class="card-actions justify-end">
                                    <div class="badge badge-primary">Recommended</div>
                                </div>
                            </div>
                        </div>
                        <div class="card bg-base-200">
                            <div class="card-body">
                                <h4 class="card-title">tts_models/en/ljspeech/glow-tts</h4>
                                <p class="text-sm text-base-content/70">Glow-based model with fast inference and good quality</p>
                            </div>
                        </div>
                        <div class="card bg-base-200">
                            <div class="card-body">
                                <h4 class="card-title">tts_models/en/ljspeech/speedy-speech</h4>
                                <p class="text-sm text-base-content/70">Optimized for fast generation speed</p>
                            </div>
                        </div>
                        <div class="card bg-base-200">
                            <div class="card-body">
                                <h4 class="card-title">tts_models/en/vctk/vits</h4>
                                <p class="text-sm text-base-content/70">Multi-speaker English model with voice cloning</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Other Languages -->
                <div class="mb-8">
                    <h3 class="text-2xl font-bold mb-4">🌍 Other Languages</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        <div class="card bg-base-200">
                            <div class="card-body">
                                <h4 class="card-title">Spanish</h4>
                                <p class="text-sm text-base-content/70">tts_models/es/css10/vits</p>
                                <div class="badge badge-outline">CSS10 Dataset</div>
                            </div>
                        </div>
                        <div class="card bg-base-200">
                            <div class="card-body">
                                <h4 class="card-title">French</h4>
                                <p class="text-sm text-base-content/70">tts_models/fr/css10/vits</p>
                                <div class="badge badge-outline">CSS10 Dataset</div>
                            </div>
                        </div>
                        <div class="card bg-base-200">
                            <div class="card-body">
                                <h4 class="card-title">German</h4>
                                <p class="text-sm text-base-content/70">tts_models/de/thorsten/tacotron2-DDC</p>
                                <div class="badge badge-outline">Thorsten Dataset</div>
                            </div>
                        </div>
                        <div class="card bg-base-200">
                            <div class="card-body">
                                <h4 class="card-title">Japanese</h4>
                                <p class="text-sm text-base-content/70">tts_models/ja/kokoro/tacotron2-DDC</p>
                                <div class="badge badge-outline">Kokoro Dataset</div>
                            </div>
                        </div>
                        <div class="card bg-base-200">
                            <div class="card-body">
                                <h4 class="card-title">Chinese</h4>
                                <p class="text-sm text-base-content/70">tts_models/zh-CN/baker/tacotron2-DDC</p>
                                <div class="badge badge-outline">Baker Dataset</div>
                            </div>
                        </div>
                        <div class="card bg-base-200">
                            <div class="card-body">
                                <h4 class="card-title">Russian</h4>
                                <p class="text-sm text-base-content/70">tts_models/ru/css10/vits</p>
                                <div class="badge badge-outline">CSS10 Dataset</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- API Documentation -->
    <section id="api" class="py-16 bg-base-200">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">API Documentation</h2>
            <p class="text-center text-lg text-base-content/70 mb-12 max-w-2xl mx-auto">
                Simple REST API for integrating offline text-to-speech into your applications
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
                            <pre><code>https://voicecraft-ai.vercel.app</code></pre>
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
                            <pre><code>GET /api/tts?model=MODEL_NAME&text=YOUR_TEXT</code></pre>
                        </div>
                        <div class="mt-4">
                            <h4 class="font-bold mb-2">Parameters:</h4>
                            <ul class="list-disc list-inside space-y-1">
                                <li><code>model</code> (required) - TTS model name</li>
                                <li><code>text</code> (required) - Text to convert (max 500 characters)</li>
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
                                    <pre><code>const response = await fetch('/api/tts?model=tts_models/en/ljspeech/tacotron2-DDC&text=Hello world');
const audioBlob = await response.blob();
const audioUrl = URL.createObjectURL(audioBlob);
const audio = new Audio(audioUrl);
audio.play();</code></pre>
                                </div>
                            </div>
                            <div class="tab-pane hidden" id="python">
                                <div class="mockup-code bg-neutral text-neutral-content">
                                    <pre><code>import requests

url = 'https://voicecraft-ai.vercel.app/api/tts'
params = {
    'model': 'tts_models/en/ljspeech/tacotron2-DDC',
    'text': 'Hello world'
}

response = requests.get(url, params=params)
with open('audio.wav', 'wb') as f:
    f.write(response.content)</code></pre>
                                </div>
                            </div>
                            <div class="tab-pane hidden" id="curl">
                                <div class="mockup-code bg-neutral text-neutral-content">
                                    <pre><code>curl "https://voicecraft-ai.vercel.app/api/tts?model=tts_models/en/ljspeech/tacotron2-DDC&text=Hello%20world" -o audio.wav</code></pre>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- FAQ Section -->
    <section id="faq" class="py-16 bg-base-100">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-4">Frequently Asked Questions</h2>
            <p class="text-center text-lg text-base-content/70 mb-12 max-w-2xl mx-auto">
                Everything you need to know about VoiceCraft AI
            </p>
            
            <div class="max-w-4xl mx-auto space-y-4">
                <div class="collapse collapse-arrow bg-base-200">
                    <input type="radio" name="faq" />
                    <div class="collapse-title text-xl font-medium">
                        Is VoiceCraft AI really free and unlimited?
                    </div>
                    <div class="collapse-content">
                        <p>Yes! VoiceCraft AI is 100% free forever with no usage limits, no API keys, and no registration required. We believe in accessible AI for everyone.</p>
                    </div>
                </div>
                
                <div class="collapse collapse-arrow bg-base-200">
                    <input type="radio" name="faq" />
                    <div class="collapse-title text-xl font-medium">
                        How does the offline capability work?
                    </div>
                    <div class="collapse-content">
                        <p>VoiceCraft AI uses Coqui TTS, which runs completely offline. Once the models are downloaded, no internet connection is required for text-to-speech generation.</p>
                    </div>
                </div>
                
                <div class="collapse collapse-arrow bg-base-200">
                    <input type="radio" name="faq" />
                    <div class="collapse-title text-xl font-medium">
                        What audio format is generated?
                    </div>
                    <div class="collapse-content">
                        <p>All audio is generated in WAV format with high-quality 22.05kHz sampling rate, ensuring clear and natural-sounding speech.</p>
                    </div>
                </div>
                
                <div class="collapse collapse-arrow bg-base-200">
                    <input type="radio" name="faq" />
                    <div class="collapse-title text-xl font-medium">
                        Can I use this for commercial projects?
                    </div>
                    <div class="collapse-content">
                        <p>Absolutely! VoiceCraft AI is free for both personal and commercial use. There are no restrictions on how you use the generated audio.</p>
                    </div>
                </div>
                
                <div class="collapse collapse-arrow bg-base-200">
                    <input type="radio" name="faq" />
                    <div class="collapse-title text-xl font-medium">
                        What's the maximum text length?
                    </div>
                    <div class="collapse-content">
                        <p>Currently, we support up to 500 characters per request to ensure optimal performance and quick response times.</p>
                    </div>
                </div>
                
                <div class="collapse collapse-arrow bg-base-200">
                    <input type="radio" name="faq" />
                    <div class="collapse-title text-xl font-medium">
                        How do I get started with the API?
                    </div>
                    <div class="collapse-content">
                        <p>Simply make a GET request to our TTS endpoint with your chosen model and text. No setup or authentication required!</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer footer-center p-10 bg-base-300 text-base-content">
        <aside>
            <div class="flex items-center justify-center mb-4">
                <i data-lucide="mic" class="w-8 h-8 text-primary mr-2"></i>
                <p class="text-xl font-bold">VoiceCraft AI</p>
            </div>
            <p>Free • Unlimited • Offline Text-to-Speech</p>
            <p class="mt-2">Powered by Coqui TTS • Complete Privacy • No Internet Required</p>
        </aside>
    </footer>

    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <script>
        // Initialize Lucide icons
        lucide.createIcons();
        
        // Character counter
        const textInput = document.getElementById('textInput');
        const charCount = document.getElementById('charCount');
        
        textInput.addEventListener('input', () => {
            const length = textInput.value.length;
            charCount.textContent = `${length}/500`;
            if (length > 500) {
                charCount.classList.add('text-error');
            } else {
                charCount.classList.remove('text-error');
            }
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
            const model = document.getElementById('modelSelect').value;
            const text = document.getElementById('textInput').value;
            const convertBtn = document.getElementById('convertBtn');
            const audioSection = document.getElementById('audioSection');
            const errorAlert = document.getElementById('errorAlert');
            const generationInfo = document.getElementById('generationInfo');
            
            if (!text.trim()) {
                showError('Please enter some text to convert');
                return;
            }
            
            if (text.length > 500) {
                showError('Text must be 500 characters or less');
                return;
            }
            
            // Show loading state
            convertBtn.innerHTML = '<i data-lucide="loader" class="w-5 h-5 mr-2 animate-spin"></i>Generating...';
            convertBtn.disabled = true;
            errorAlert.classList.add('hidden');
            
            try {
                const response = await fetch(`/api/tts?model=${encodeURIComponent(model)}&text=${encodeURIComponent(text)}`);
                
                if (response.ok) {
                    const audioBlob = await response.blob();
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audioPlayer = document.getElementById('audioPlayer');
                    const downloadBtn = document.getElementById('downloadBtn');
                    
                    audioPlayer.src = audioUrl;
                    audioSection.classList.remove('hidden');
                    
                    // Set up download
                    const fileName = `voicecraft-${model.split('/').pop()}-${Date.now()}.wav`;
                    downloadBtn.href = audioUrl;
                    downloadBtn.download = fileName;
                    
                    // Show generation info
                    const sizeKB = (audioBlob.size / 1024).toFixed(1);
                    generationInfo.textContent = `${sizeKB} KB • Offline Generated`;
                    
                } else {
                    const errorData = await response.json();
                    showError(errorData.message || 'Failed to generate speech');
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            } finally {
                // Reset button
                convertBtn.innerHTML = '<i data-lucide="volume-2" class="w-5 h-5 mr-2"></i>Generate Speech';
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
async def text_to_speech_api(model: str = "", text: str = ""):
    if not model or not text or model.strip() == "" or text.strip() == "":
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": "Model and text parameters are required"
            },
            status_code=400
        )
    
    # Validate text length
    if len(text) > 500:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": "Text must be 500 characters or less"
            },
            status_code=400
        )
    
    # Check if model is available
    all_models = []
    for category in AVAILABLE_MODELS.values():
        all_models.extend(category.keys())
    
    if model not in all_models:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": f"Model '{model}' is not available. Please use one of the supported models."
            },
            status_code=400
        )
    
    try:
        # Initialize TTS with the specified model
        tts = TTS(model_name=model, progress_bar=False, gpu=False)
        
        # Create temporary file for audio output
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        # Generate TTS audio
        tts.tts_to_file(text=text, file_path=temp_path)
        
        # Read the generated audio file
        with open(temp_path, "rb") as audio_file:
            audio_data = audio_file.read()
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        # Create in-memory file-like object
        audio_buffer = io.BytesIO(audio_data)
        
        return StreamingResponse(
            audio_buffer,
            media_type="audio/wav",
            headers={
                "Content-Disposition": "inline; filename=voicecraft-audio.wav",
                "X-Generated-By": "VoiceCraft AI",
                "X-Model-Used": model
            }
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": f"Error generating speech: {str(e)}"
            },
            status_code=400
        )

@app.get("/api/models")
async def list_models_api():
    return JSONResponse(
        content={
            "status": True,
            "status_code": 200,
            "models": AVAILABLE_MODELS,
            "default_model": DEFAULT_MODEL,
            "total_models": sum(len(category) for category in AVAILABLE_MODELS.values())
        }
    )

@app.get("/api/health")
async def health_check():
    return JSONResponse(
        content={
            "status": True,
            "status_code": 200,
            "message": "VoiceCraft AI is healthy",
            "version": "1.0.0",
            "service": "Offline TTS API",
            "features": ["Free", "Unlimited", "Offline", "Multiple Languages"]
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
