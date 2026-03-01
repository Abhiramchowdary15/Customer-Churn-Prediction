import { motion } from "framer-motion";
import { columns } from "@/data/churnData";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export function DatasetSection() {
  const typeColor = (type: string) => {
    switch (type) {
      case "Numerical": return "bg-accent/15 text-accent border-accent/30";
      case "Categorical": return "bg-primary/15 text-primary border-primary/30";
      case "Target": return "bg-destructive/15 text-destructive border-destructive/30";
      case "Binary": return "bg-muted-foreground/15 text-muted-foreground border-muted-foreground/30";
      default: return "bg-muted text-muted-foreground";
    }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-xl">
            📊 Dataset Overview — Key Columns
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Column</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Description</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {columns.map((col) => (
                  <TableRow key={col.name}>
                    <TableCell className="font-mono font-medium text-sm">{col.name}</TableCell>
                    <TableCell>
                      <Badge variant="outline" className={typeColor(col.type)}>{col.type}</Badge>
                    </TableCell>
                    <TableCell className="text-muted-foreground text-sm">{col.description}</TableCell>
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
