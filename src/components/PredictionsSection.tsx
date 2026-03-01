import { motion } from "framer-motion";
import { samplePredictions } from "@/data/churnData";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Progress } from "@/components/ui/progress";

export function PredictionsSection() {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.7 }}>
      <Card>
        <CardHeader>
          <CardTitle className="text-xl">🔮 Sample Churn Predictions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>#</TableHead>
                  <TableHead>Gender</TableHead>
                  <TableHead>Tenure</TableHead>
                  <TableHead>Contract</TableHead>
                  <TableHead>Monthly ($)</TableHead>
                  <TableHead>Prediction</TableHead>
                  <TableHead>Confidence</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {samplePredictions.map((p) => (
                  <TableRow key={p.id}>
                    <TableCell className="font-mono text-sm">{p.id}</TableCell>
                    <TableCell>{p.gender}</TableCell>
                    <TableCell className="font-mono">{p.tenure} mo</TableCell>
                    <TableCell className="text-sm">{p.contract}</TableCell>
                    <TableCell className="font-mono">${p.monthlyCharges}</TableCell>
                    <TableCell>
                      <Badge
                        variant={p.prediction === "Churn" ? "destructive" : "outline"}
                        className={p.prediction === "No Churn" ? "bg-accent/15 text-accent border-accent/30" : ""}
                      >
                        {p.prediction}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2 min-w-[120px]">
                        <Progress value={p.confidence} className="h-2 flex-1" />
                        <span className="text-xs font-mono text-muted-foreground w-8">{p.confidence}%</span>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
