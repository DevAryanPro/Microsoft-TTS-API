from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
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

@app.get("/")
async def root():
    return JSONResponse(
        content={
            "status": True,
            "status_code": 200,
            "message": "Microsoft TTS API is running"
        }
    )

@app.get("/docs", response_class=HTMLResponse)
@app.get("/documentation", response_class=HTMLResponse)
async def documentation():
    html_content = """
<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft TTS API</title>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link href="https://fonts.googleapis.com/css2?family=Geist:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * { font-family: 'Geist', sans-serif; }
    </style>
</head>
<body class="min-h-screen bg-base-100">
    <!-- Navigation -->
    <div class="navbar bg-base-200 shadow-lg">
        <div class="navbar-start">
            <div class="dropdown">
                <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </div>
                <ul tabindex="0" class="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow">
                    <li><a href="#features">Características</a></li>
                    <li><a href="#usage">Uso</a></li>
                    <li><a href="#voices">Voces</a></li>
                    <li><a href="#examples">Ejemplos</a></li>
                </ul>
            </div>
            <a class="btn btn-ghost text-xl">🎙️ TTS API</a>
        </div>
        <div class="navbar-center hidden lg:flex">
            <ul class="menu menu-horizontal px-1">
                <li><a href="#features">Características</a></li>
                <li><a href="#usage">Uso</a></li>
                <li><a href="#voices">Voces</a></li>
                <li><a href="#examples">Ejemplos</a></li>
            </ul>
        </div>
        <div class="navbar-end">
            <label class="swap swap-rotate">
                <input type="checkbox" class="theme-controller" value="dark" />
                <svg class="swap-off w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                </svg>
                <svg class="swap-on w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"></path>
                </svg>
            </label>
        </div>
    </div>

    <!-- Hero Section -->
    <div class="hero min-h-screen bg-base-200">
        <div class="hero-content text-center">
            <div class="max-w-4xl">
                <h1 class="text-5xl font-bold">🎙️ Microsoft TTS API</h1>
                <p class="py-6 text-xl">
                    Convierte texto a audio con 400+ voces neuronales de Microsoft Edge
                </p>
                <div class="flex flex-col sm:flex-row gap-4 justify-center">
                    <a href="#usage" class="btn btn-primary btn-lg">Comenzar</a>
                    <a href="/api/tts?voice=es-MX-DaliaNeural&text=Hola, esta es una prueba de la API" 
                       class="btn btn-outline btn-lg" target="_blank">🎵 Probar Ahora</a>
                </div>
            </div>
        </div>
    </div>

    <!-- Features Section -->
    <div id="features" class="py-20 bg-base-100">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-12">✨ Características</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div class="card bg-base-200 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">💰 Totalmente Gratis</h3>
                        <p>Sin costos ocultos, sin límites de uso para proyectos personales</p>
                    </div>
                </div>
                <div class="card bg-base-200 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🔐 Sin Autenticación</h3>
                        <p>Usa la API directamente sin necesidad de API keys o registro</p>
                    </div>
                </div>
                <div class="card bg-base-200 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🎯 Alta Calidad</h3>
                        <p>Audio MP3 a 24kHz con voces neuronales de última generación</p>
                    </div>
                </div>
                <div class="card bg-base-200 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🌎 Múltiples Idiomas</h3>
                        <p>400+ voces en 30+ idiomas diferentes disponibles</p>
                    </div>
                </div>
                <div class="card bg-base-200 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">⚡ Respuesta Rápida</h3>
                        <p>Conversión de texto a voz en tiempo real con baja latencia</p>
                    </div>
                </div>
                <div class="card bg-base-200 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🔧 Fácil Integración</h3>
                        <p>API REST simple con parámetros claros y documentación completa</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Usage Section -->
    <div id="usage" class="py-20 bg-base-200">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-12">🚀 Cómo Usar</h2>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <!-- API Endpoint -->
                <div class="card bg-base-100 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">📋 Endpoint Principal</h3>
                        <div class="mockup-code bg-neutral text-neutral-content">
                            <pre><code>GET /api/tts?voice=es-MX-DaliaNeural&text=Hola mundo</code></pre>
                        </div>
                    </div>
                </div>

                <!-- Parameters -->
                <div class="card bg-base-100 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🔮 Parámetros</h3>
                        <div class="space-y-4">
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text font-bold">voice <span class="badge badge-primary">requerido</span></span>
                                </label>
                                <input type="text" class="input input-bordered" value="es-MX-DaliaNeural" readonly>
                                <label class="label">
                                    <span class="label-text-alt">Nombre de la voz neural</span>
                                </label>
                            </div>
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text font-bold">text <span class="badge badge-primary">requerido</span></span>
                                </label>
                                <input type="text" class="input input-bordered" value="Hola mundo" readonly>
                                <label class="label">
                                    <span class="label-text-alt">Texto a convertir</span>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Example URL -->
            <div class="card bg-primary text-primary-content mt-8">
                <div class="card-body">
                    <h3 class="card-title">💡 URL de Ejemplo</h3>
                    <div class="bg-primary-content text-primary p-4 rounded-lg">
                        <code class="break-all">https://your-app.vercel.app/api/tts?voice=es-MX-DaliaNeural&text=Buenos días, ¿cómo estás?</code>
                    </div>
                    <div class="card-actions justify-end">
                        <a href="/api/tts?voice=es-MX-DaliaNeural&text=Buenos días, ¿cómo estás?" 
                           class="btn btn-secondary" target="_blank">Probar Ejemplo</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Voices Section -->
    <div id="voices" class="py-20 bg-base-100">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-12">🎤 Voces Populares</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
                <!-- Spanish Voices -->
                <div class="card bg-base-200 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🇪🇸 Español</h3>
                        <div class="space-y-2">
                            <div class="badge badge-outline">es-MX-DaliaNeural 👩</div>
                            <div class="badge badge-outline">es-MX-JorgeNeural 👨</div>
                            <div class="badge badge-outline">es-ES-ElviraNeural 👩</div>
                            <div class="badge badge-outline">es-ES-AlvaroNeural 👨</div>
                            <div class="badge badge-outline">es-AR-ElenaNeural 👩</div>
                            <div class="badge badge-outline">es-CO-SalomeNeural 👩</div>
                        </div>
                    </div>
                </div>

                <!-- English Voices -->
                <div class="card bg-base-200 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🇺🇸 English</h3>
                        <div class="space-y-2">
                            <div class="badge badge-outline">en-US-JennyNeural 👩</div>
                            <div class="badge badge-outline">en-US-GuyNeural 👨</div>
                            <div class="badge badge-outline">en-GB-LibbyNeural 👩</div>
                            <div class="badge badge-outline">en-GB-RyanNeural 👨</div>
                        </div>
                    </div>
                </div>

                <!-- Other Languages -->
                <div class="card bg-base-200 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🌍 Otros Idiomas</h3>
                        <div class="space-y-2">
                            <div class="badge badge-outline">fr-FR-DeniseNeural 👩</div>
                            <div class="badge badge-outline">de-DE-KatjaNeural 👩</div>
                            <div class="badge badge-outline">it-IT-ElsaNeural 👩</div>
                            <div class="badge badge-outline">pt-BR-FranciscaNeural 👩</div>
                            <div class="badge badge-outline">ja-JP-NanamiNeural 👩</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="text-center">
                <a href="/api/voices" class="btn btn-primary btn-lg">
                    Ver todas las 400+ voces disponibles
                </a>
            </div>
        </div>
    </div>

    <!-- Code Examples -->
    <div id="examples" class="py-20 bg-base-200">
        <div class="container mx-auto px-4">
            <h2 class="text-4xl font-bold text-center mb-12">💻 Ejemplos de Código</h2>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <!-- JavaScript -->
                <div class="card bg-base-100 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🟨 JavaScript</h3>
                        <div class="mockup-code bg-neutral text-neutral-content">
                            <pre><code>const url = "/api/tts";
const params = "?voice=es-MX-DaliaNeural&text=Hola mundo";

fetch(url + params)
  .then(res => res.blob())
  .then(blob => {
    const audio = new Audio(URL.createObjectURL(blob));
    audio.play();
  });</code></pre>
                        </div>
                    </div>
                </div>

                <!-- Python -->
                <div class="card bg-base-100 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🐍 Python</h3>
                        <div class="mockup-code bg-neutral text-neutral-content">
                            <pre><code>import requests

url = "/api/tts"
params = {
    "voice": "es-MX-DaliaNeural",
    "text": "Hola mundo"
}

response = requests.get(url, params=params)
with open("audio.mp3", "wb") as f:
    f.write(response.content)</code></pre>
                        </div>
                    </div>
                </div>

                <!-- cURL -->
                <div class="card bg-base-100 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🖥️ cURL</h3>
                        <div class="mockup-code bg-neutral text-neutral-content">
                            <pre><code>curl "/api/tts?voice=es-MX-DaliaNeural&text=Hola" -o audio.mp3</code></pre>
                        </div>
                    </div>
                </div>

                <!-- PHP -->
                <div class="card bg-base-100 shadow-xl">
                    <div class="card-body">
                        <h3 class="card-title">🐘 PHP</h3>
                        <div class="mockup-code bg-neutral text-neutral-content">
                            <pre><code>$url = "/api/tts";
$params = "?voice=es-MX-DaliaNeural&text=Hola";

file_put_contents("audio.mp3", 
    file_get_contents($url . $params));</code></pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="footer footer-center p-10 bg-base-300 text-base-content">
        <aside>
            <p class="font-bold text-lg">Microsoft TTS API</p>
            <p>Conversor de texto a voz gratuito usando Microsoft Edge TTS</p>
            <p class="mt-2">Hecho con ❤️ para desarrolladores</p>
        </aside>
    </footer>

    <script>
        // Theme toggle
        const themeToggle = document.querySelector('.theme-controller');
        themeToggle.addEventListener('change', (e) => {
            document.documentElement.setAttribute('data-theme', e.target.checked ? 'dark' : 'light');
        });

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
                "message": "Se requieren los parámetros voice y text"
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
                    "message": "No se pudo generar el audio"
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
                "message": f"Error al procesar la solicitud: {str(e)}"
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
                "voices": formatted_voices
            }
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "status": False,
                "status_code": 400,
                "message": f"Error al obtener las voces: {str(e)}"
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
            "message": "Endpoint no encontrado"
        },
        status_code=404
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        content={
            "status": False,
            "status_code": 500,
            "message": "Error interno del servidor"
        },
        status_code=500
    )
