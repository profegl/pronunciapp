from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import ffmpeg
from analisis.ipa_detector import analyze_ipa
from datetime import datetime
from analisis.rr_detector import analyze_rr

from database import (
    crear_db,
    guardar_muestra,
    obtener_muestras
)

from datetime import datetime

audio_guardado = (
    f"audios/{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
)

app = FastAPI()
crear_db()

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ENDPOINT
# -------------------------

@app.get("/muestras")
def listar_muestras():

    return obtener_muestras()

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):

    print("Archivo recibido:", file.filename)

    # Guardar WEBM recibido
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convertir WEBM -> WAV
    #wav_path = "temp_audio.wav"
    #audio_guardado = f"audios/{file.filename}.wav"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    audio_guardado = f"audios/guitarra_{timestamp}.wav"

    ffmpeg.input(file_path).output(
        audio_guardado,
        acodec="pcm_s16le",
        ac=1,
        ar="16000"
    ).run(overwrite_output=True)

    print("WAV generado:", os.path.exists(audio_guardado))

    # Analizar WAV
    result = analyze_rr(audio_guardado)
    result_ipa = analyze_ipa(audio_guardado)

    print("Guardando muestra...")

    guardar_muestra(
    palabra="guitarra",
    hnr=result["hnr"],
    pulsos=result["pulsos"],
    intensidad=result["intensidad_media"],
    clasificacion_sistema=result["clasificacion"],
    audio_path=audio_guardado
)
    
    print("Muestra guardada")

    # Limpiar archivos temporales
    if os.path.exists(file_path):
        os.remove(file_path)

    #if os.path.exists(wav_path):
    #    os.remove(wav_path)

    return {
        "filename": file.filename,
        "analysis": result,
        "ipa_module": result_ipa
    }