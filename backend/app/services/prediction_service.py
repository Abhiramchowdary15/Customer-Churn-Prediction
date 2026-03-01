import os
import json
import numpy as np
import joblib

# Paths
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ml')
MODEL_PATH = os.path.join(MODEL_DIR, 'model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

_model = None
_scaler = None


def _load_model():
    global _model, _scaler
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        if os.path.exists(SCALER_PATH):
            _scaler = joblib.load(SCALER_PATH)


def _get_retention_action(probability, risk_level):
    """Suggest a retention action based on churn probability."""
    if risk_level == 'High':
        actions = [
            "Offer a 20% discount on next 3 months",
            "Assign a dedicated account manager",
            "Provide a free service upgrade for 6 months",
            "Schedule an immediate satisfaction survey call",
        ]
    elif risk_level == 'Medium':
        actions = [
            "Send a personalized loyalty reward",
            "Offer contract upgrade with bonus features",
            "Provide exclusive access to premium support",
            "Send a targeted retention email campaign",
        ]
    else:
        actions = [
            "Continue standard engagement",
            "Send a thank-you email with referral bonus",
            "Include in quarterly satisfaction survey",
            "Offer early access to new features",
        ]
    idx = int(probability * 10) % len(actions)
    return actions[idx]


def make_prediction(data):
    """Run the ML model on input data and return prediction results."""
    _load_model()

    # Encode features
    gender = 1 if data.get('gender', 'Male') == 'Male' else 0
    senior = 1 if data.get('senior_citizen', False) else 0
    partner = 1 if data.get('partner', False) else 0
    dependents = 1 if data.get('dependents', False) else 0
    tenure = int(data.get('tenure', 0))
    phone = 1 if data.get('phone_service', True) else 0
    paperless = 1 if data.get('paperless_billing', True) else 0
    monthly = float(data.get('monthly_charges', 0))
    total = float(data.get('total_charges', 0))

    # Satisfaction metrics
    rating = max(1, min(5, int(data.get('rating', 3))))
    feedback = max(0, min(2, int(data.get('feedback_score', 1))))
    nps = max(0, min(10, int(data.get('nps_score', 7))))

    # Usage frequency
    daily_logins = max(0, float(data.get('daily_logins', 1.0)))
    weekly_trans = max(0, int(data.get('weekly_transactions', 5)))
    session_min = max(0, float(data.get('avg_session_minutes', 15.0)))
    last_login = max(0, int(data.get('last_login_days', 0)))

    # Engineered features
    engagement_score = min(1.0, (min(daily_logins, 10) / 10 * 0.3) +
                           (min(weekly_trans, 30) / 30 * 0.3) +
                           (min(session_min, 120) / 120 * 0.4))
    usage_decline = last_login / (tenure + 1)  # high = declining usage

    # Internet service encoding
    internet = data.get('internet_service', 'Fiber optic')
    inet_dsl = 1 if internet == 'DSL' else 0
    inet_fiber = 1 if internet == 'Fiber optic' else 0
    inet_no = 1 if internet == 'No' else 0

    # Contract encoding
    contract = data.get('contract', 'Month-to-month')
    cont_m2m = 1 if contract == 'Month-to-month' else 0
    cont_1y = 1 if contract == 'One year' else 0
    cont_2y = 1 if contract == 'Two year' else 0

    # Payment method encoding
    payment = data.get('payment_method', 'Electronic check')
    pay_echeck = 1 if payment == 'Electronic check' else 0
    pay_mcheck = 1 if payment == 'Mailed check' else 0
    pay_bank = 1 if payment == 'Bank transfer' else 0
    pay_cc = 1 if payment == 'Credit card' else 0

    features = np.array([[
        gender, senior, partner, dependents, tenure, phone, paperless,
        monthly, total,
        inet_dsl, inet_fiber, inet_no,
        cont_m2m, cont_1y, cont_2y,
        pay_echeck, pay_mcheck, pay_bank, pay_cc,
        rating, feedback, nps,
        daily_logins, weekly_trans, session_min, last_login,
        engagement_score, usage_decline
    ]])

    if _model is not None:
        if _scaler is not None:
            features = _scaler.transform(features)

        proba = _model.predict_proba(features)[0]
        churn_prob = round(float(proba[1]) * 100, 1)
        prediction = 'Churn' if churn_prob >= 50 else 'No Churn'
        confidence = round(float(max(proba)) * 100, 1)
    else:
        # Fallback heuristic when model is not available
        risk_score = 0
        if tenure < 6:
            risk_score += 30
        elif tenure < 12:
            risk_score += 15
        if monthly > 70:
            risk_score += 20
        if contract == 'Month-to-month':
            risk_score += 20
        if payment == 'Electronic check':
            risk_score += 10
        if internet == 'Fiber optic':
            risk_score += 10
        # Satisfaction impact
        if rating <= 2:
            risk_score += 25
        elif rating == 3:
            risk_score += 10
        if feedback == 0:  # Negative
            risk_score += 15
        if nps <= 6:  # Detractor
            risk_score += 20
        elif nps <= 8:  # Passive
            risk_score += 5
        # Usage frequency impact
        if daily_logins < 0.5:
            risk_score += 20
        elif daily_logins < 1:
            risk_score += 10
        if weekly_trans < 2:
            risk_score += 15
        if session_min < 5:
            risk_score += 15
        if last_login > 14:
            risk_score += 25
        elif last_login > 7:
            risk_score += 10
        if engagement_score < 0.2:
            risk_score += 20

        churn_prob = min(risk_score, 95)
        prediction = 'Churn' if churn_prob >= 50 else 'No Churn'
        confidence = 100 - abs(50 - churn_prob)

    # Risk level
    if churn_prob >= 70:
        risk_level = 'High'
    elif churn_prob >= 40:
        risk_level = 'Medium'
    else:
        risk_level = 'Low'

    retention_action = _get_retention_action(churn_prob / 100, risk_level)

    return {
        'prediction': prediction,
        'probability': churn_prob,
        'confidence': confidence,
        'risk_level': risk_level,
        'retention_action': retention_action,
    }
