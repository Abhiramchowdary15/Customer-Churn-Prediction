import { motion } from "framer-motion";
import { preprocessingSteps } from "@/data/churnData";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function PreprocessingSection() {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
      <Card>
        <CardHeader>
          <CardTitle className="text-xl">🔧 Data Preprocessing Steps</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {preprocessingSteps.map((s, i) => (
              <div key={i} className="flex gap-4 items-start">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-sm">
                  {i + 1}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-sm">{s.step}</p>
                  <p className="text-muted-foreground text-sm">{s.reason}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
