import { useState, useRef } from "react";
import { Mic, Square } from "lucide-react";
import { motion } from "framer-motion";

export default function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // -------------------------
  // INICIAR GRABACIÓN
  // -------------------------
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/webm",
        });

        const audioUrl = URL.createObjectURL(audioBlob);
        setAudioURL(audioUrl);

        const formData = new FormData();
        formData.append("file", audioBlob, "audio.webm");

        setLoading(true);
        setError(null);
        setResult(null);

        try {
          const response = await fetch(
            "http://127.0.0.1:8000/upload-audio",
            {
              method: "POST",
              body: formData,
            }
          );

          const data = await response.json();

          console.log("RESULTADO BACKEND:", data);

          setResult(data.analysis.clasificacion);

        } catch (err) {
          console.error("Error enviando audio:", err);
          setError("No se pudo conectar con el servidor");
        } finally {
          setLoading(false);
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accediendo al micrófono:", error);
      setError("No se pudo acceder al micrófono");
    }
  };

  // -------------------------
  // DETENER GRABACIÓN
  // -------------------------
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();

      mediaRecorderRef.current.stream
        .getTracks()
        .forEach((track) => track.stop());
    }

    setIsRecording(false);
  };

  // -------------------------
  // TOGGLE
  // -------------------------
  const handleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <div className="min-h-screen bg-[#ECECEC] flex flex-col items-center px-4 py-8">
      
      {/* TÍTULO */}
      <h1 className="text-center font-black uppercase leading-none text-black text-4xl md:text-6xl mt-4">
        PRÁCTICA DE
        <br />
        PRONUNCIACIÓN
      </h1>

      {/* PALABRA */}
      <motion.div
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        className="mt-20 bg-gradient-to-b from-fuchsia-500 to-purple-700 rounded-[24px] shadow-xl px-16 py-7"
      >
        <h2 className="text-white text-4xl font-bold">
          guitarra
        </h2>
      </motion.div>

      {/* BOTÓN MICRÓFONO */}
      <motion.button
        whileTap={{ scale: 0.92 }}
        whileHover={{ scale: 1.04 }}
        onClick={handleRecording}
        className={`mt-16 w-40 h-40 rounded-full flex items-center justify-center shadow-2xl transition-all duration-300 ${
          isRecording
            ? "bg-red-600 animate-pulse"
            : "bg-gradient-to-b from-purple-700 to-purple-900"
        }`}
      >
        {isRecording ? (
          <Square size={60} className="text-white fill-white" />
        ) : (
          <Mic size={70} className="text-white" />
        )}
      </motion.button>

      {/* ESTADO */}
      <p className="mt-6 text-gray-700 font-medium">
        {isRecording ? "Grabando..." : "Presiona para grabar"}
      </p>

      {/* AUDIO */}
      {audioURL && (
        <div className="mt-10 flex flex-col items-center gap-4">
          <p className="font-semibold">Tu grabación:</p>
          <audio controls src={audioURL}></audio>
        </div>
      )}

      {/* LOADING */}
      {loading && (
        <p className="mt-6 text-blue-600 font-bold animate-pulse">
          Analizando pronunciación...
        </p>
      )}

      {/* ERROR */}
      {error && (
        <p className="mt-6 text-red-600 font-bold">
          {error}
        </p>
      )}

      {/* RESULTADO */}
      {result && (
        <div className="mt-6 text-center">
          <p className="text-lg font-bold">Resultado:</p>

          <p
            className={`text-2xl font-black ${
              result === "RR correcta"
                ? "text-green-600"
                : result === "RR débil"
                ? "text-yellow-600"
                : "text-red-600"
            }`}
          >
            {result}
          </p>
        </div>
      )}
    </div>
  );
}