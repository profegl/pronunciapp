import sqlite3

DB_NAME = "pronunciapp.db"


# ----------------------------------
# CREAR BASE DE DATOS
# ----------------------------------
def crear_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS muestras (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        palabra TEXT,

        hnr REAL,

        pulsos INTEGER,

        intensidad REAL,

        clasificacion_sistema TEXT,

        etiqueta_real TEXT,

        audio_path TEXT

    )
    """)

    conn.commit()
    conn.close()


# ----------------------------------
# GUARDAR MUESTRA
# ----------------------------------
def guardar_muestra(
    palabra,
    hnr,
    pulsos,
    intensidad,
    clasificacion_sistema,
    audio_path
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO muestras
    (
        palabra,
        hnr,
        pulsos,
        intensidad,
        clasificacion_sistema,
        audio_path
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        palabra,
        hnr,
        pulsos,
        intensidad,
        clasificacion_sistema,
        audio_path
    ))

    conn.commit()
    conn.close()


# ----------------------------------
# OBTENER TODAS LAS MUESTRAS
# ----------------------------------
def obtener_muestras():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM muestras
    ORDER BY id DESC
    """)

    filas = cursor.fetchall()

    conn.close()

    return filas


# ----------------------------------
# ETIQUETAR MUESTRA
# ----------------------------------
def actualizar_etiqueta(
    muestra_id,
    etiqueta_real
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE muestras
    SET etiqueta_real = ?
    WHERE id = ?
    """, (
        etiqueta_real,
        muestra_id
    ))

    conn.commit()
    conn.close()

    if __name__ == "__main__":
        crear_db()
        print("Base de datos creada")