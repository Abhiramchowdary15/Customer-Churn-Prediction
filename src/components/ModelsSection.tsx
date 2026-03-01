import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const models = [
  {
    name: "Logistic Regression",
    emoji: "📐",
    description: "A simple linear model that finds a line to separate churn vs no-churn customers. Fast and easy to explain.",
    code: `model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)`,
  },
  {
    name: "Random Forest",
    emoji: "🌲",
    description: "Builds many decision trees and combines their votes. Handles complex patterns well.",
    code: `model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)`,
  },
  {
    name: "Neural Network (Keras)",
    emoji: "🧠",
    description: "A deep learning model with multiple layers. Learns non-linear patterns from the data.",
    code: `model = Sequential([
  Dense(64, activation='relu', input_shape=(X.shape[1],)),
  Dropout(0.3),
  Dense(32, activation='relu'),
  Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy')
model.fit(X_train, y_train, epochs=50, batch_size=32)`,
  },
];

export function ModelsSection() {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.45 }}>
      <h2 className="text-xl font-bold mb-4">🤖 Models Used</h2>
      <div className="grid md:grid-cols-3 gap-4">
        {models.map((m) => (
          <Card key={m.name} className="flex flex-col">
            <CardHeader className="pb-2">
              <CardTitle className="text-base flex items-center gap-2">
                <span className="text-2xl">{m.emoji}</span>
                {m.name}
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col gap-3">
              <p className="text-sm text-muted-foreground">{m.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </motion.div>
  );
}
