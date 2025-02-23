
import { Mic } from "lucide-react";

interface RecordButtonProps {
  isRecording: boolean;
  onClick: () => void;
}

const RecordButton = ({ isRecording, onClick }: RecordButtonProps) => {
  return (
    <button
      onClick={onClick}
      className={`p-2 transition-colors ${
        isRecording
          ? "text-theme-red animate-pulse"
          : "text-white hover:text-white/70"
      }`}
    >
      <Mic size={48} />
    </button>
  );
};

export default RecordButton;
