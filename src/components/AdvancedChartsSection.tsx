import { motion } from "framer-motion";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, ReferenceLine,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { confusionMatrices, rocCurveData, aucScores } from "@/data/churnData";

const COLORS = {
  LR: "hsl(250, 65%, 55%)",
  RF: "hsl(170, 60%, 45%)",
  NN: "hsl(35, 90%, 55%)",
};

function ConfusionMatrix({ name, short, matrix }: typeof confusionMatrices[0]) {
  const total = matrix.tn + matrix.fp + matrix.fn + matrix.tp;
  const accuracy = ((matrix.tn + matrix.tp) / total * 100).toFixed(1);

  const cells = [
    { label: "TN", value: matrix.tn, row: "Actual: No", col: "Pred: No", className: "bg-accent/20 text-accent-foreground" },
    { label: "FP", value: matrix.fp, row: "Actual: No", col: "Pred: Yes", className: "bg-destructive/15 text-destructive" },
    { label: "FN", value: matrix.fn, row: "Actual: Yes", col: "Pred: No", className: "bg-destructive/15 text-destructive" },
    { label: "TP", value: matrix.tp, row: "Actual: Yes", col: "Pred: Yes", className: "bg-accent/20 text-accent-foreground" },
  ];

  return (
    <Card className="h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-base flex items-center justify-between">
          <span>{name}</span>
          <Badge variant="outline" className="font-mono">{accuracy}%</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-[auto_1fr_1fr] gap-1 text-center text-sm">
          {/* Header row */}
          <div />
          <div className="font-medium text-muted-foreground text-xs py-1">Pred: No</div>
          <div className="font-medium text-muted-foreground text-xs py-1">Pred: Yes</div>

          {/* Row 1: Actual No */}
          <div className="font-medium text-muted-foreground text-xs flex items-center pr-2">Actual: No</div>
          <div className={`rounded-lg p-3 ${cells[0].className}`}>
            <div className="text-xs text-muted-foreground">TN</div>
            <div className="text-lg font-bold font-mono">{cells[0].value}</div>
          </div>
          <div className={`rounded-lg p-3 ${cells[1].className}`}>
            <div className="text-xs text-muted-foreground">FP</div>
            <div className="text-lg font-bold font-mono">{cells[1].value}</div>
          </div>

          {/* Row 2: Actual Yes */}
          <div className="font-medium text-muted-foreground text-xs flex items-center pr-2">Actual: Yes</div>
          <div className={`rounded-lg p-3 ${cells[2].className}`}>
            <div className="text-xs text-muted-foreground">FN</div>
            <div className="text-lg font-bold font-mono">{cells[2].value}</div>
          </div>
          <div className={`rounded-lg p-3 ${cells[3].className}`}>
            <div className="text-xs text-muted-foreground">TP</div>
            <div className="text-lg font-bold font-mono">{cells[3].value}</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export function AdvancedChartsSection() {
  return (
    <div className="space-y-6">
      {/* Confusion Matrices */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.65 }}>
        <h2 className="text-xl font-bold mb-4">🔢 Confusion Matrices</h2>
        <div className="grid md:grid-cols-3 gap-4">
          {confusionMatrices.map((cm) => (
            <ConfusionMatrix key={cm.short} {...cm} />
          ))}
        </div>
      </motion.div>

      {/* ROC Curve */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.75 }}>
        <Card>
          <CardHeader>
            <CardTitle className="text-xl flex items-center gap-2">
              📉 ROC Curves
              <div className="flex gap-2 ml-auto">
                {Object.entries(aucScores).map(([key, val]) => (
                  <Badge key={key} variant="outline" className="font-mono text-xs">
                    {key}: AUC {val}
                  </Badge>
                ))}
              </div>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={350}>
              <LineChart data={rocCurveData}>
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <XAxis
                  dataKey="fpr"
                  label={{ value: "False Positive Rate", position: "insideBottom", offset: -5 }}
                  tick={{ fontSize: 12 }}
                  domain={[0, 1]}
                />
                <YAxis
                  label={{ value: "True Positive Rate", angle: -90, position: "insideLeft" }}
                  tick={{ fontSize: 12 }}
                  domain={[0, 1]}
                />
                <Tooltip
                  formatter={(value: number, name: string) => [`${(value * 100).toFixed(1)}%`, name]}
                  labelFormatter={(label: number) => `FPR: ${(label * 100).toFixed(0)}%`}
                />
                <Legend />
                <ReferenceLine
                  segment={[{ x: 0, y: 0 }, { x: 1, y: 1 }]}
                  stroke="hsl(var(--muted-foreground))"
                  strokeDasharray="5 5"
                  strokeOpacity={0.5}
                />
                <Line type="monotone" dataKey="LR" name="Logistic Regression" stroke={COLORS.LR} strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="RF" name="Random Forest" stroke={COLORS.RF} strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="NN" name="Neural Network" stroke={COLORS.NN} strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
