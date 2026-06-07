from allosaurus.app import read_recognizer

print("Cargando modelo...")

recognizer = read_recognizer()

print("Modelo cargado.")

resultado = recognizer.recognize(
    "audios/ejemplo2.wav",
    lang_id="spa"
)

print(resultado)