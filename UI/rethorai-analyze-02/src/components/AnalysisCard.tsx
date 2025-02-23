
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface AnalysisCardProps {
  title: string;
  children: React.ReactNode;
}

const AnalysisCard = ({ title, children }: AnalysisCardProps) => {
  return (
    <Card className="bg-white/5 backdrop-blur-lg border-white/10 rounded-2xl">
      <CardHeader>
        <CardTitle className="text-xl font-semibold text-white">{title}</CardTitle>
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
};

export default AnalysisCard;
