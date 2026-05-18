import { useState, useRef } from "react";
import { Mic, Square } from "lucide-react";
import { motion } from "framer-motion";

export default function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // INICIAR GRABACIÓN
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

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/wav",
        });

        const audioUrl = URL.createObjectURL(audioBlob);

        setAudioURL(audioUrl);
      };

      mediaRecorder.start();

      setIsRecording(true);
    } catch (error) {
      console.error("Error accediendo al micrófono:", error);
    }
  };

  // DETENER GRABACIÓN
  const stopRecording = () => {
    mediaRecorderRef.current.stop();

    setIsRecording(false);
  };

  // TOGGLE
  const handleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <div className="min-h-screen bg-[#ECECEC] flex flex-col items-center px-4 py-8">
      
      {/* Título */}
      <h1
        className="
          text-center
          font-black
          uppercase
          leading-none
          text-black
          text-4xl
          md:text-6xl
          mt-4
        "
      >
        PRÁCTICA DE
        <br />
        PRONUNCIACIÓN
      </h1>

      {/* Palabra */}
      <motion.div
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        className="
          mt-20
          bg-gradient-to-b
          from-fuchsia-500
          to-purple-700
          rounded-[24px]
          shadow-xl
          px-16
          py-7
        "
      >
        <h2 className="text-white text-4xl font-bold">
          guitarra
        </h2>
      </motion.div>

      {/* Botón micrófono */}
      <motion.button
        whileTap={{ scale: 0.92 }}
        whileHover={{ scale: 1.04 }}
        onClick={handleRecording}
        className={`
          mt-16
          w-40
          h-40
          rounded-full
          flex
          items-center
          justify-center
          shadow-2xl
          transition-all
          duration-300

          ${
            isRecording
              ? "bg-red-600 animate-pulse"
              : "bg-gradient-to-b from-purple-700 to-purple-900"
          }
        `}
      >
        {isRecording ? (
          <Square size={60} className="text-white fill-white" />
        ) : (
          <Mic size={70} className="text-white" />
        )}
      </motion.button>

      {/* Estado */}
      <p className="mt-6 text-gray-700 font-medium">
        {isRecording
          ? "Grabando..."
          : "Presiona para grabar"}
      </p>

      {/* Audio reproducible */}
      {audioURL && (
        <div className="mt-10 flex flex-col items-center gap-4">
          <p className="font-semibold">
            Tu grabación:
          </p>

          <audio controls src={audioURL}></audio>
        </div>
      )}
    </div>
  );
}