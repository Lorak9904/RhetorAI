
import { AnalysisResult } from "@/types/analysis";

const AnalysisSections = ({ data }: { data: AnalysisResult }) => {
  return (
    <div className="space-y-6">
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
        <h3 className="text-xl font-semibold text-white mb-3">Analysis Score</h3>
        <div className="text-4xl font-bold text-white mb-2">{data.score}/100</div>
        <p className="text-white/70">{data.filename}</p>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
        <h3 className="text-xl font-semibold text-white mb-3">Analysis</h3>
        <p className="text-white/70 leading-relaxed">{data.analysis}</p>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
        <h3 className="text-xl font-semibold text-white mb-3">Improvement Tips</h3>
        <ul className="space-y-2 text-white/70">
          {data.tips.map((tip, index) => (
            <li key={index}>• {tip}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AnalysisSections;
