SAFE_MEDICINES = ["Paracetamol", "ORS", "Zinc", "Antihistamine"]

def suggest_safe_medicine(text):
    return [m for m in SAFE_MEDICINES if m.lower() in text.lower()]
