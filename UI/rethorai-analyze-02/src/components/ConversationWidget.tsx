
import { useConversation } from "@11labs/react";
import { Mic, MicOff, Volume2, VolumeX } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";

const ConversationWidget = () => {
  const [isMuted, setIsMuted] = useState(false);
  const conversation = useConversation();
  const [isConnected, setIsConnected] = useState(false);

  const handleStartConversation = async () => {
    try {
      await conversation.startSession({
        agentId: "lmfUCktvNNNtqsQUg0ao"  // Using your provided agent ID
      });
      setIsConnected(true);
    } catch (error) {
      console.error("Failed to start conversation:", error);
    }
  };

  const handleEndConversation = async () => {
    await conversation.endSession();
    setIsConnected(false);
  };

  const toggleMute = async () => {
    await conversation.setVolume({ volume: isMuted ? 1 : 0 });
    setIsMuted(!isMuted);
  };

  return (
    <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
      <div className="flex flex-col space-y-4">
        <h3 className="text-2xl font-semibold text-white mb-2">AI Conversation Assistant</h3>
        <p className="text-white/70">
          Practice your speaking skills with our AI conversation assistant. Start a conversation
          to receive real-time feedback and guidance.
        </p>
        <div className="flex items-center space-x-4">
          {!isConnected ? (
            <Button
              onClick={handleStartConversation}
              className="bg-theme-red hover:bg-theme-red/90 text-white"
            >
              <Mic className="mr-2 h-4 w-4" />
              Start Conversation
            </Button>
          ) : (
            <Button
              onClick={handleEndConversation}
              variant="destructive"
            >
              <MicOff className="mr-2 h-4 w-4" />
              End Conversation
            </Button>
          )}
          <Button
            variant="ghost"
            className="text-white"
            onClick={toggleMute}
          >
            {isMuted ? (
              <VolumeX className="h-4 w-4" />
            ) : (
              <Volume2 className="h-4 w-4" />
            )}
          </Button>
        </div>
        {isConnected && (
          <div className="text-white/70 animate-pulse">
            Conversation active - Speak naturally...
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationWidget;
