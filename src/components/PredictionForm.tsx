import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

type Result = { prediction: "Churn" | "No Churn"; confidence: number } | null;

export function PredictionForm() {
  const [tenure, setTenure] = useState("");
  const [monthly, setMonthly] = useState("");
  const [contract, setContract] = useState("");
  const [internet, setInternet] = useState("");
  const [result, setResult] = useState<Result>(null);

  const canSubmit = tenure && monthly && contract && internet;

  // Simple mock prediction logic based on real churn patterns
  const predict = () => {
    const t = Math.max(0, Math.min(72, Number(tenure) || 0));
    const m = Math.max(0, Math.min(200, Number(monthly) || 0));

    let score = 50; // base

    // Short tenure = higher churn risk
    if (t <= 6) score += 20;
    else if (t <= 18) score += 8;
    else if (t >= 36) score -= 15;

    // Month-to-month = highest risk
    if (contract === "month") score += 18;
    else if (contract === "one") score -= 8;
    else if (contract === "two") score -= 22;

    // Fiber optic = higher churn
    if (internet === "fiber") score += 12;
    else if (internet === "no") score -= 15;

    // High monthly charges = higher risk
    if (m > 80) score += 10;
    else if (m < 30) score -= 8;

    // Clamp between 10 and 95
    score = Math.max(10, Math.min(95, score));
    const isChurn = score >= 50;

    setResult({
      prediction: isChurn ? "Churn" : "No Churn",
      confidence: isChurn ? score : 100 - score,
    });
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.75 }}>
      <Card>
        <CardHeader>
          <CardTitle className="text-xl">🧪 Try It — Predict Customer Churn</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-8">
            {/* Form */}
            <div className="space-y-4">
              <div>
                <Label htmlFor="tenure">Tenure (months)</Label>
                <Input
                  id="tenure"
                  type="number"
                  min={0}
                  max={72}
                  placeholder="e.g. 12"
                  value={tenure}
                  onChange={(e) => setTenure(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="monthly">Monthly Charges ($)</Label>
                <Input
                  id="monthly"
                  type="number"
                  min={0}
                  max={200}
                  step={0.01}
                  placeholder="e.g. 65.50"
                  value={monthly}
                  onChange={(e) => setMonthly(e.target.value)}
                />
              </div>
              <div>
                <Label>Contract Type</Label>
                <Select value={contract} onValueChange={setContract}>
                  <SelectTrigger><SelectValue placeholder="Select contract" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="month">Month-to-month</SelectItem>
                    <SelectItem value="one">One year</SelectItem>
                    <SelectItem value="two">Two year</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Internet Service</Label>
                <Select value={internet} onValueChange={setInternet}>
                  <SelectTrigger><SelectValue placeholder="Select service" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="fiber">Fiber optic</SelectItem>
                    <SelectItem value="dsl">DSL</SelectItem>
                    <SelectItem value="no">No internet</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button onClick={predict} disabled={!canSubmit} className="w-full">
                Predict Churn
              </Button>
            </div>

            {/* Result */}
            <div className="flex items-center justify-center">
              <AnimatePresence mode="wait">
                {result ? (
                  <motion.div
                    key={result.prediction + result.confidence}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    className="text-center space-y-4 w-full max-w-xs"
                  >
                    <div className="text-6xl">{result.prediction === "Churn" ? "⚠️" : "✅"}</div>
                    <Badge
                      variant={result.prediction === "Churn" ? "destructive" : "outline"}
                      className={`text-lg px-4 py-1 ${result.prediction === "No Churn" ? "bg-accent/15 text-accent border-accent/30" : ""}`}
                    >
                      {result.prediction}
                    </Badge>
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">Confidence</p>
                      <Progress value={result.confidence} className="h-3" />
                      <p className="font-mono font-bold text-lg mt-1">{result.confidence}%</p>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {result.prediction === "Churn"
                        ? "This customer is likely to leave. Consider offering a retention deal."
                        : "This customer is likely to stay. Keep up the good service!"}
                    </p>
                  </motion.div>
                ) : (
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-muted-foreground text-sm text-center"
                  >
                    Fill in the details and click Predict to see the result.
                  </motion.p>
                )}
              </AnimatePresence>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
