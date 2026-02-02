def analyze_symptoms(user_input: str):
    """
    Analyze and normalize user symptoms.
    This module MUST stay LLM-free for safety and clarity.
    """
    return {
        "raw_text": user_input,
        "tokens": user_input.lower().split()
    }

