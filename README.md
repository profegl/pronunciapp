# 🎤 PronunciApp

Aplicación web para la práctica de pronunciación del idioma español mediante análisis acústico de audio.

## Descripción

PronunciApp es un prototipo educativo que permite:

- Grabar audio desde el navegador.
- Enviar la grabación a un servidor FastAPI.
- Convertir el audio a formato WAV.
- Analizar características acústicas mediante Praat (Parselmouth).
- Clasificar experimentalmente la pronunciación de la vibrante múltiple "RR".

Actualmente el sistema devuelve una clasificación:

- RR correcta
- RR débil
- R simple

## Arquitectura

```text
Frontend (React)
        │
        ▼
Grabación WEBM
        │
        ▼
Backend (FastAPI)
        │
        ▼
FFmpeg
WEBM → WAV
        │
        ▼
Praat / Parselmouth
        │
        ▼
Análisis acústico
        │
        ▼
Clasificación RR
```

## Tecnologías utilizadas

### Frontend

- React
- Vite
- TailwindCSS
- Framer Motion
- Lucide React

### Backend

- Python 3.13
- FastAPI
- Uvicorn
- Parselmouth (Praat)
- FFmpeg

### Herramientas

- Git
- GitHub
- Visual Studio Code

---

# Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/TU_USUARIO/pronunciapp.git
```

```bash
cd pronunciapp
```

---

## 2. Backend

Ingresar a:

```bash
cd backend
```

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno:

### Windows

```bash
venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Iniciar servidor:

```bash
uvicorn main:app --reload
```

Servidor disponible en:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 3. Frontend

Abrir otra terminal:

```bash
cd frontend
```

Instalar dependencias:

```bash
npm install
```

Iniciar aplicación:

```bash
npm run dev
```

La aplicación estará disponible en:

```text
http://localhost:5173
```

---

# Cómo probar

1. Abrir la aplicación React.
2. Presionar el botón del micrófono.
3. Pronunciar la palabra mostrada.
4. Detener la grabación.
5. Esperar el procesamiento.
6. Visualizar el resultado.

Ejemplo:

```text
Resultado:
RR correcta
```

---

# Estado actual

## Implementado

- Grabación desde navegador
- Envío de audio al backend
- Conversión WEBM → WAV
- Procesamiento acústico con Praat
- Clasificación experimental de RR

## Experimental

- Detección de fonemas IPA
- Integración con Allosaurus
- Comparación automática de pronunciación

---

# Roadmap

## Versión 1.0

- Grabación de audio
- Procesamiento acústico
- Clasificación RR

## Versión 2.0

- Conversión Audio → IPA
- Integración Allosaurus
- Evaluación fonética avanzada

## Versión 3.0

- Historial de usuarios
- Gamificación
- Ejercicios personalizados

---

#  Autores

Proyecto desarrollado como trabajo académico para Trayecto Programador

Autora: Laura Mercado - @Glaurim


# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
