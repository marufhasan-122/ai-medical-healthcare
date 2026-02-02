def generate_doctor_report(symptoms, risk, advice):
    return f"""
🩺 MEDICAL SUMMARY REPORT
----------------------------

• Reported Symptoms:
{symptoms}

• Risk Level:
{risk['risk_level'].upper()} (Score: {risk['score']*100:.0f}%)

• General Medical Advice:
{advice}

• Recommendation:
- Monitor symptoms closely
- Consult a healthcare professional if symptoms worsen

⚠️ Disclaimer:
This is NOT a medical diagnosis.
"""
