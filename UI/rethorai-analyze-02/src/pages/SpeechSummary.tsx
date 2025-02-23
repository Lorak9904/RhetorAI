
import { ArrowLeft, UserRound } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { useToast } from "@/components/ui/use-toast";
import DebateScoreCard from "@/components/DebateScoreCard";

const SpeechSummary = () => {
  const { toast } = useToast();

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
        
        <h1 className="text-4xl font-bold text-white mb-6">Speech Summary</h1>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="h-full">
            <DebateScoreCard />
          </div>
          <div className="space-y-6">
            <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
              <h3 className="text-xl font-semibold text-white mb-3">Key Insights</h3>
              <ul className="space-y-2 text-white/70">
                <li>• Strong evidence presentation and logical flow</li>
                <li>• Excellent time management throughout</li>
                <li>• Room for improvement in rebuttal techniques</li>
                <li>• Consistent speaking clarity and pace</li>
              </ul>
            </div>
            <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
              <h3 className="text-xl font-semibold text-white mb-3">Recommendations</h3>
              <ul className="space-y-2 text-white/70">
                <li>• Practice anticipating counter-arguments</li>
                <li>• Focus on strengthening rebuttal responses</li>
                <li>• Maintain current time management strategies</li>
                <li>• Consider incorporating more varied evidence types</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpeechSummary;
