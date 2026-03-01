import { motion } from "framer-motion";
import { Database, Brain, BarChart3, Cpu } from "lucide-react";

const stats = [
  { label: "Total Records", value: "7,043", icon: Database },
  { label: "Features", value: "21", icon: BarChart3 },
  { label: "ML Models", value: "3", icon: Brain },
  { label: "Best F1", value: "59.3%", icon: Cpu },
];

export function HeroSection() {
  return (
    <section className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary/90 to-primary p-8 md:p-12 text-primary-foreground mb-8">
      {/* Background decoration */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-0 right-0 w-96 h-96 rounded-full bg-accent blur-3xl" />
        <div className="absolute bottom-0 left-0 w-64 h-64 rounded-full bg-primary-foreground blur-3xl" />
      </div>

      <div className="relative z-10">
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-sm font-mono uppercase tracking-widest opacity-80 mb-2"
        >
          Machine Learning & Deep Learning
        </motion.p>
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-3xl md:text-5xl font-bold mb-3 leading-tight"
        >
          Customer Churn Prediction
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-lg opacity-80 max-w-2xl mb-8"
        >
          Predicting customer churn using Logistic Regression, Random Forest, and
          Neural Network on the Telco Customer Churn dataset.
        </motion.p>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stats.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 + i * 0.1 }}
              className="bg-primary-foreground/10 backdrop-blur-sm rounded-xl p-4 border border-primary-foreground/10"
            >
              <s.icon className="h-5 w-5 mb-2 opacity-70" />
              <p className="text-2xl font-bold font-mono">{s.value}</p>
              <p className="text-xs opacity-70">{s.label}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
