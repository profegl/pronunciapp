from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import ffmpeg

from analisis.rr_detector import analyze_rr

app = FastAPI()

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
@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):

    print("Archivo recibido:", file.filename)

    # Guardar WEBM recibido
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convertir WEBM -> WAV
    wav_path = "temp_audio.wav"

    ffmpeg.input(file_path).output(
        wav_path,
        acodec="pcm_s16le",
        ac=1,
        ar="16000"
    ).run(overwrite_output=True)

    print("WAV generado:", os.path.exists(wav_path))

    # Analizar WAV
    result = analyze_rr(wav_path)

    # Limpiar archivos temporales
    if os.path.exists(file_path):
        os.remove(file_path)

    if os.path.exists(wav_path):
        os.remove(wav_path)

    return {
        "filename": file.filename,
        "analysis": result
    }