import { motion } from "framer-motion";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, PieChart, Pie, Cell,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { comparisonChartData, modelResults, churnByContract } from "@/data/churnData";
import { Badge } from "@/components/ui/badge";

const COLORS = {
  LR: "hsl(250, 65%, 55%)",
  RF: "hsl(170, 60%, 45%)",
  NN: "hsl(35, 90%, 55%)",
};

const pieData = [
  { name: "No Churn", value: 73.5, color: "hsl(170, 60%, 45%)" },
  { name: "Churn", value: 26.5, color: "hsl(0, 72%, 55%)" },
];

export function ChartsSection() {
  // Find best model
  const best = modelResults.reduce((a, b) => (a.f1 > b.f1 ? a : b));

  return (
    <div className="space-y-6">
      {/* Row 1: Pie + Contract bar */}
      <div className="grid md:grid-cols-2 gap-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}>
          <Card className="h-full">
            <CardHeader>
              <CardTitle className="text-lg">📈 Churn Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={pieData} cx="50%" cy="50%" outerRadius={90} innerRadius={50} dataKey="value" label={({ name, value }) => `${name}: ${value}%`} labelLine={false}>
                    {pieData.map((entry, i) => (
                      <Cell key={i} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.55 }}>
          <Card className="h-full">
            <CardHeader>
              <CardTitle className="text-lg">📋 Churn by Contract Type</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={churnByContract}>
                  <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                  <XAxis dataKey="contract" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Bar dataKey="churn" name="Churn %" fill="hsl(0, 72%, 55%)" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="noChurn" name="No Churn %" fill="hsl(170, 60%, 45%)" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Row 2: Model comparison */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }}>
        <Card>
          <CardHeader>
            <CardTitle className="text-xl flex items-center gap-2">
              🏆 Model Performance Comparison
              <Badge className="bg-accent text-accent-foreground">Best: {best.name} (F1: {best.f1}%)</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={comparisonChartData} barCategoryGap="20%">
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <XAxis dataKey="metric" tick={{ fontSize: 13 }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="LR" name="Logistic Regression" fill={COLORS.LR} radius={[4, 4, 0, 0]} />
                <Bar dataKey="RF" name="Random Forest" fill={COLORS.RF} radius={[4, 4, 0, 0]} />
                <Bar dataKey="NN" name="Neural Network" fill={COLORS.NN} radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
