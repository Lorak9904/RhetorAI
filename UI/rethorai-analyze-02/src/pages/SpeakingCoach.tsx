
import { ArrowLeft, UserRound } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { useToast } from "@/components/ui/use-toast";
import { useEffect } from "react";

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'elevenlabs-convai': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> & {
        'agent-id': string;
      };
    }
  }
}

const SpeakingCoach = () => {
  const { toast } = useToast();

  useEffect(() => {
    // Add the ElevenLabs script
    const script = document.createElement('script');
    script.src = "https://elevenlabs.io/convai-widget/index.js";
    script.async = true;
    script.type = "text/javascript";
    
    // Create a style element for our CSS
    const style = document.createElement('style');
    style.textContent = `
      .convai-widget [data-testid="call-button"],
      .convai-widget .convai-call-button,
      .convai-widget button[aria-label="Call"],
      .convai-widget div[role="button"][aria-label="Call"],
      .convai-widget .phone-icon,
      .convai-widget [class*="call"],
      .convai-widget [class*="phone"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        position: absolute !important;
        pointer-events: none !important;
        clip: rect(0 0 0 0) !important;
        margin: -1px !important;
        padding: 0 !important;
        border: 0 !important;
      }
    `;
    
    // Add elements to the document
    document.head.appendChild(style);
    document.body.appendChild(script);

    // Create a MutationObserver to ensure our styles are applied even after dynamic updates
    const observer = new MutationObserver((mutations) => {
      const widget = document.querySelector('.convai-widget');
      if (widget) {
        const phoneElements = widget.querySelectorAll('[class*="call"], [class*="phone"], [aria-label="Call"]');
        phoneElements.forEach(element => {
          if (element instanceof HTMLElement) {
            element.style.display = 'none';
            element.style.visibility = 'hidden';
            element.style.opacity = '0';
            element.style.width = '0';
            element.style.height = '0';
            element.style.position = 'absolute';
            element.style.pointerEvents = 'none';
          }
        });
      }
    });

    // Start observing the document with the configured parameters
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });

    // Cleanup function
    return () => {
      observer.disconnect();
      if (script && script.parentNode) {
        script.parentNode.removeChild(script);
      }
      if (style && style.parentNode) {
        style.parentNode.removeChild(style);
      }
    };
  }, []);

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-black via-black/95 to-slate-900/20">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex justify-between items-center mb-8">
          <Link to="/">
            <Button variant="ghost" className="text-white/70 hover:text-white">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Home
            </Button>
          </Link>
          <Button
            variant="ghost"
            className="rounded-full p-2 hover:bg-white/10"
            onClick={() => toast({ title: "Profile", description: "Profile functionality coming soon!" })}
          >
            <UserRound className="h-6 w-6 text-white/70" />
          </Button>
        </div>
        
        <h1 className="text-4xl font-bold text-white mb-6">Speaking Coach</h1>
        <div className="grid gap-6">
          <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
            <h2 className="text-2xl font-semibold text-white mb-4">Welcome to Your Personal Speaking Coach</h2>
            <p className="text-white/70 mb-4">
              Here you'll find tools and resources to improve your public speaking skills:
            </p>
            <ul className="list-disc list-inside text-white/70 space-y-2 mb-6">
              <li>Real-time feedback on your speech patterns</li>
              <li>Personalized improvement suggestions</li>
              <li>Practice exercises and drills</li>
              <li>Progress tracking and analytics</li>
            </ul>
          </div>
          <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
            <elevenlabs-convai agent-id="lmfUCktvNNNtqsQUg0ao"></elevenlabs-convai>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpeakingCoach;
