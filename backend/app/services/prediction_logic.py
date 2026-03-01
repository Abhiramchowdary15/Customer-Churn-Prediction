def calculate_churn(data):
    # Business Logic: If high charges and low tenure, high risk
    tenure = int(data.get('tenure', 0))
    charges = float(data.get('monthly_charges', 0))
    
    if tenure < 6 and charges > 70:
        return "High Risk"
    elif tenure < 12:
        return "Medium Risk"
    else:
        return "Low Risk"