import parselmouth
import numpy as np


# -----------------------------
# 1. PULSOS (RR vibración)
# -----------------------------
def detectar_pulsos(sonido):
    intensidad = sonido.to_intensity()
    valores = intensidad.values[0]

    valores = np.nan_to_num(valores)

    max_val = np.max(valores)
    valores_norm = valores / max_val if max_val > 0 else valores

    picos = 0
    umbral = 0.6

    for i in range(1, len(valores_norm) - 1):
        if (
            valores_norm[i] > umbral and
            valores_norm[i] > valores_norm[i - 1] and
            valores_norm[i] > valores_norm[i + 1]
        ):
            picos += 1

    return picos


# -----------------------------
# 2. CLASIFICACIÓN RR
# -----------------------------
def clasificar_rr(hnr, pulsos, intensidad):
    
    if pulsos >= 25:
        return "RR correcta"

    elif pulsos >= 10:
        return "RR débil"

    else:
        return "R simple"
    #if hnr > 10 and pulsos > 5:
    #    return "RR correcta"

    #elif hnr > 5 and pulsos > 2:
    #    return "RR débil"

    #else:
    #    return "R simple"


# -----------------------------
# 3. FUNCIÓN PRINCIPAL
# -----------------------------
def analyze_rr(audio_path):

    sonido = parselmouth.Sound(audio_path)

    # duración
    duracion = sonido.get_total_duration()

    # intensidad
    intensidad = sonido.to_intensity()
    intensidad_media = np.nanmean(intensidad.values)

    # HNR (calidad vocal)
    harmonicity = sonido.to_harmonicity()
    hnr_media = np.nanmean(harmonicity.values)

    # pulsos vocales (RR vibración)
    pulsos = detectar_pulsos(sonido)

    # clasificación final
    clasificacion = clasificar_rr(
        hnr_media,
        pulsos,
        intensidad_media
    )

    print("HNR:", hnr_media)
    print("Pulsos:", pulsos)
    print("Intensidad:", intensidad_media)
    
    return {
        #"duracion_segundos": round(duracion, 2),
        #"intensidad_media": round(float(intensidad_media), 2),
        #"hnr": round(float(hnr_media), 2),
        #"pulsos": int(pulsos),
        #"clasificacion": clasificacion,
        #"diagnostico": "Audio procesado correctamente"
        
        "duracion_segundos": round(duracion, 2),
        "intensidad_media": round(float(intensidad_media), 2),
        "hnr": round(float(hnr_media), 2),
        "pulsos": int(pulsos),
        "clasificacion": clasificacion
}
# NOTA:
# El HNR se calcula únicamente con fines experimentales.
# Durante las pruebas se observaron valores inconsistentes
# para audios breves grabados desde navegador.
# En esta versión la clasificación utiliza únicamente
# la cantidad de pulsos detectados.    