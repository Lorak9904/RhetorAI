import { useState, useRef } from "react";
import { Upload, UserRound, ArrowLeft, Mic } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import { useNavigate } from "react-router-dom";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { AnalysisResult } from "@/types/analysis";
import AnalysisSections from "@/components/AnalysisSections";

const Index = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
  const [recordingError, setRecordingError] = useState<string | null>(null);
  const [analysisData, setAnalysisData] = useState<AnalysisResult | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const navigate = useNavigate();
  const { toast } = useToast();

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks: Blob[] = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data);
        }
      };

      recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        const file = new File([blob], "recording.webm", { type: 'audio/webm' });
        await handleFileAnalysis(file);
      };

      setMediaRecorder(recorder);
      setAudioChunks([]);
      recorder.start();
      setIsRecording(true);
      setRecordingError(null);
    } catch (error) {
      console.error("Error starting recording:", error);
      setRecordingError("Could not access microphone");
      toast({
        variant: "destructive",
        title: "Recording Error",
        description: "Could not access microphone. Please check permissions.",
      });
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
      mediaRecorder.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const handleRecordClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const handleFileAnalysis = async (file: File) => {
    try {
      setIsAnalyzing(true);
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("https://outside-abagail-agme-3605d15a.koyeb.app/audio", {
        method: "POST",
        mode: "cors",
        headers: {
          "Accept": "application/json",
        },
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Server response status:", response.status);
        console.error("Server error details:", errorText);
        
        let errorMessage = "There was an error analyzing your audio file";
        if (response.status === 413) {
          errorMessage = "File size too large";
        } else if (response.status === 415) {
          errorMessage = "Unsupported file type";
        } else if (response.status === 500) {
          errorMessage = `Server error: ${errorText}`;
        }
        
        throw new Error(errorMessage);
      }

      const data = await response.json();
      if (!data.analysis || !data.score || !data.tips) {
        throw new Error("Invalid response format from server");
      }
      
      setAnalysisData(data);
      toast({ 
        title: "Analysis complete", 
        description: "Your audio has been analyzed successfully" 
      });
    } catch (error) {
      console.error("Analysis error:", error);
      toast({
        variant: "destructive",
        title: "Analysis failed",
        description: error instanceof Error ? error.message : "There was an error analyzing your audio file",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    console.log("File type:", file.type);
    console.log("File name:", file.name);

    if (!file.name.endsWith(".webm")) {
      toast({
        variant: "destructive",
        title: "Invalid file type",
        description: "Please upload a file with .webm extension.",
      });
      return;
    }

    await handleFileAnalysis(file);
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-black via-black/95 to-slate-900/20">
      <nav className="px-6 py-4 backdrop-blur-sm border-b border-white/10">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-12">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="icon"
                className="rounded-full hover:bg-white/10"
                onClick={() => navigate(-1)}
              >
                <ArrowLeft className="h-6 w-6 text-white/70" />
              </Button>
              <div className="text-2xl font-bold text-white">RhetorAI</div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              className="rounded-full p-2 hover:bg-white/10" 
              onClick={() => toast({ title: "Profile", description: "Profile functionality coming soon!" })}
            >
              <UserRound className="h-6 w-6 text-white/70" />
            </Button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 pt-24 pb-12">
        <div className="text-center max-w-3xl mx-auto mb-36">
          <h1 className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white/90 via-white to-white/50 tracking-tight mb-6">
            Your Rhetoric, Enhanced
          </h1>
          <p className="text-xl text-white/70">Upload your WebM audio file for instant speech analysis</p>
        </div>

        <div className="max-w-4xl mx-auto">
          <div className="flex flex-col items-center gap-8 mb-12">
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleFileUpload} 
              accept=".webm" 
              className="hidden" 
            />
            <div className="flex gap-4">
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button 
                      onClick={handleRecordClick} 
                      className={`bg-white/10 hover:bg-white/20 text-white p-8 rounded-full ${isRecording ? 'animate-pulse bg-red-500/20' : ''}`}
                      disabled={isAnalyzing}
                    >
                      <Mic className="w-8 h-8" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{isRecording ? 'Stop Recording' : 'Start Recording'}</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button 
                      onClick={handleUploadClick} 
                      className="bg-white/10 hover:bg-white/20 text-white p-8 rounded-full" 
                      disabled={isAnalyzing || isRecording}
                    >
                      <Upload className="w-8 h-8" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Upload WebM audio</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
            {isRecording && <p className="text-white/70">Recording in progress...</p>}
            {isAnalyzing && <p className="text-white/70">Analyzing your audio...</p>}
            {recordingError && <p className="text-red-500">{recordingError}</p>}
          </div>
          {analysisData && <AnalysisSections data={analysisData} />}
        </div>
      </div>
    </div>
  );
};

export default Index;
