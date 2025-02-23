
interface ScoreProps {
  category: string;
  score: number;
  maxScore: number;
}

const ScoreBar = ({ score, maxScore }: { score: number; maxScore: number }) => (
  <div className="w-full bg-white/5 rounded-full h-2">
    <div 
      className="h-full rounded-full transition-all duration-500"
      style={{ 
        width: `${(score / maxScore) * 100}%`,
        background: `linear-gradient(90deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,${score/100}) 100%)`
      }}
    />
  </div>
);

const ScoreItem = ({ category, score, maxScore }: ScoreProps) => (
  <div className="space-y-2">
    <div className="flex justify-between items-center">
      <span className="text-white/70">{category}</span>
      <span className="text-white font-mono">{score}/{maxScore}</span>
    </div>
    <ScoreBar score={score} maxScore={maxScore} />
  </div>
);

const DebateScoreCard = () => {
  const scores = [
    { category: "Argumentation", score: 85, maxScore: 100 },
    { category: "Evidence Use", score: 92, maxScore: 100 },
    { category: "Rebuttal Quality", score: 78, maxScore: 100 },
    { category: "Speaking Clarity", score: 88, maxScore: 100 },
    { category: "Time Management", score: 95, maxScore: 100 }
  ];

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-white">Speech Performance</h2>
      </div>
      <div className="space-y-4">
        {scores.map((score, index) => (
          <ScoreItem key={index} {...score} />
        ))}
        <div className="mt-6 pt-4 border-t border-white/10">
          <div className="flex justify-between items-center">
            <span className="text-white/70">Overall Score</span>
            <span className="text-white text-xl font-semibold">88%</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DebateScoreCard;
