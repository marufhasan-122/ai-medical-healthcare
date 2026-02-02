def assess_risk(symptoms: dict):
    text = symptoms["raw_text"].lower()

    if "fever" in text and "cough" in text:
        return {"risk_level": "medium", "score": 0.5}

    if "headache" in text:
        return {"risk_level": "low", "score": 0.2}

    return {"risk_level": "unknown", "score": 0.1}

