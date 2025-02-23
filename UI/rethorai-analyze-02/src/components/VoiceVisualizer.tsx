
import { useEffect, useRef } from "react";

interface VoiceVisualizerProps {
  isRecording: boolean;
  audioContext: AudioContext | null;
  mediaStream: MediaStream | null;
}

const VoiceVisualizer = ({ isRecording, audioContext, mediaStream }: VoiceVisualizerProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameRef = useRef<number>();
  const analyzerRef = useRef<AnalyserNode | null>(null);

  useEffect(() => {
    if (!isRecording || !audioContext || !mediaStream || !canvasRef.current) return;

    const analyzer = audioContext.createAnalyser();
    analyzerRef.current = analyzer;
    analyzer.fftSize = 256;
    
    const source = audioContext.createMediaStreamSource(mediaStream);
    source.connect(analyzer);

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d")!;
    const bufferLength = analyzer.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const draw = () => {
      if (!isRecording) return;
      
      animationFrameRef.current = requestAnimationFrame(draw);
      analyzer.getByteTimeDomainData(dataArray);

      // Clear canvas
      ctx.fillStyle = "rgb(0, 0, 0)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw the line
      ctx.lineWidth = 2;
      ctx.strokeStyle = "#ffffff";
      ctx.beginPath();

      const sliceWidth = canvas.width / bufferLength;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0;
        const y = (v * canvas.height) / 2;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }

        x += sliceWidth;
      }

      // Add subtle glow effect
      ctx.shadowBlur = 15;
      ctx.shadowColor = "rgba(255, 255, 255, 0.5)";
      ctx.stroke();

      // Reset shadow for next frame
      ctx.shadowBlur = 0;
    };

    draw();

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      source.disconnect();
      analyzer.disconnect();
    };
  }, [isRecording, audioContext, mediaStream]);

  return (
    <canvas
      ref={canvasRef}
      width={800}
      height={200}
      className="w-full h-48 rounded-lg bg-black"
    />
  );
};

export default VoiceVisualizer;
