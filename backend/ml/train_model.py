"""
Train a RandomForest model for customer churn prediction.
Uses synthetic data based on the Telco Customer Churn dataset patterns.
Run: python -m ml.train_model
"""
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

np.random.seed(42)
N = 5000

print("Generating synthetic Telco churn dataset...")

# Generate synthetic features
gender = np.random.choice([0, 1], N)
senior_citizen = np.random.choice([0, 1], N, p=[0.84, 0.16])
partner = np.random.choice([0, 1], N)
dependents = np.random.choice([0, 1], N, p=[0.7, 0.3])
tenure = np.random.randint(0, 73, N)
phone_service = np.random.choice([0, 1], N, p=[0.1, 0.9])
paperless_billing = np.random.choice([0, 1], N, p=[0.4, 0.6])
monthly_charges = np.round(np.random.uniform(18, 120, N), 2)
total_charges = np.round(monthly_charges * tenure + np.random.normal(0, 50, N), 2)
total_charges = np.maximum(total_charges, 0)

# Internet service (one-hot)
inet_choices = np.random.choice(['DSL', 'Fiber optic', 'No'], N, p=[0.35, 0.45, 0.20])
inet_dsl = (inet_choices == 'DSL').astype(int)
inet_fiber = (inet_choices == 'Fiber optic').astype(int)
inet_no = (inet_choices == 'No').astype(int)

# Contract (one-hot)
cont_choices = np.random.choice(['Month-to-month', 'One year', 'Two year'], N, p=[0.55, 0.25, 0.20])
cont_m2m = (cont_choices == 'Month-to-month').astype(int)
cont_1y = (cont_choices == 'One year').astype(int)
cont_2y = (cont_choices == 'Two year').astype(int)

# Payment method (one-hot)
pay_choices = np.random.choice(
    ['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'],
    N, p=[0.35, 0.20, 0.22, 0.23]
)
pay_echeck = (pay_choices == 'Electronic check').astype(int)
pay_mcheck = (pay_choices == 'Mailed check').astype(int)
pay_bank = (pay_choices == 'Bank transfer').astype(int)
pay_cc = (pay_choices == 'Credit card').astype(int)

# Satisfaction metrics
rating = np.random.choice([1, 2, 3, 4, 5], N, p=[0.08, 0.12, 0.25, 0.30, 0.25])
feedback_score = np.random.choice([0, 1, 2], N, p=[0.20, 0.35, 0.45])  # 0=Neg, 1=Neutral, 2=Pos
nps_score = np.random.randint(0, 11, N)  # 0-10

# Usage frequency
daily_logins = np.round(np.random.exponential(2.5, N), 1)  # right-skewed, many low
daily_logins = np.clip(daily_logins, 0, 20)
weekly_transactions = np.random.poisson(8, N)  # mostly 5-12
weekly_transactions = np.clip(weekly_transactions, 0, 50)
avg_session_minutes = np.round(np.random.exponential(20, N), 1)  # right-skewed
avg_session_minutes = np.clip(avg_session_minutes, 0, 120)
last_login_days = np.random.exponential(5, N).astype(int)  # most recent, some old
last_login_days = np.clip(last_login_days, 0, 90)

# Engineered features
engagement_score = np.clip(
    (np.minimum(daily_logins, 10) / 10 * 0.3) +
    (np.minimum(weekly_transactions, 30) / 30 * 0.3) +
    (np.minimum(avg_session_minutes, 120) / 120 * 0.4),
    0, 1
)
usage_decline = last_login_days / (tenure + 1)

# Build feature matrix
X = np.column_stack([
    gender, senior_citizen, partner, dependents, tenure, phone_service, paperless_billing,
    monthly_charges, total_charges,
    inet_dsl, inet_fiber, inet_no,
    cont_m2m, cont_1y, cont_2y,
    pay_echeck, pay_mcheck, pay_bank, pay_cc,
    rating, feedback_score, nps_score,
    daily_logins, weekly_transactions, avg_session_minutes, last_login_days,
    engagement_score, usage_decline
])

# Generate realistic churn labels based on known patterns
churn_score = (
    -0.04 * tenure +
    0.02 * monthly_charges +
    0.5 * cont_m2m +
    -0.8 * cont_2y +
    0.3 * inet_fiber +
    -0.5 * inet_no +
    0.4 * pay_echeck +
    0.3 * senior_citizen +
    -0.2 * partner +
    -0.3 * dependents +
    0.2 * paperless_billing +
    -0.4 * (rating - 3) +
    -0.5 * (feedback_score - 1) +
    -0.3 * (nps_score - 5) / 5 +
    -0.5 * (daily_logins - 2.5) / 2.5 +
    -0.3 * (weekly_transactions - 8) / 8 +
    -0.2 * (avg_session_minutes - 20) / 20 +
    0.6 * np.log1p(last_login_days) / 4 +
    -0.8 * engagement_score +
    0.5 * usage_decline +
    np.random.normal(0, 0.8, N)
)
churn_prob = 1 / (1 + np.exp(-churn_score))
y = (churn_prob > 0.5).astype(int)

print(f"Dataset shape: {X.shape}")
print(f"Churn rate: {y.mean():.2%}")

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train
print("Training RandomForest model...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train_scaled, y_train)

train_acc = model.score(X_train_scaled, y_train)
test_acc = model.score(X_test_scaled, y_test)
print(f"Train accuracy: {train_acc:.4f}")
print(f"Test accuracy:  {test_acc:.4f}")

# Save
ml_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(ml_dir, 'model.pkl')
scaler_path = os.path.join(ml_dir, 'scaler.pkl')

joblib.dump(model, model_path)
joblib.dump(scaler, scaler_path)

print(f"Model saved to {model_path}")
print(f"Scaler saved to {scaler_path}")
print("Done!")
