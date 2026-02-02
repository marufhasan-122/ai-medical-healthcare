import logging

logger = logging.getLogger(__name__)

EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "stroke",
    "difficulty breathing", "unconscious",
    "severe bleeding", "seizure",
    "blue lips", "infant not feeding"
]

def is_emergency(symptoms: str) -> bool:
    if not symptoms:
        return False
    symptoms = symptoms.lower()
    return any(keyword in symptoms for keyword in EMERGENCY_KEYWORDS)

EMERGENCY_RULES = [
    "chest pain",
    "difficulty breathing",
    "loss of consciousness",
    "severe bleeding",
    "stroke symptoms",
    "seizure"
]

def rule_based_emergency(text):
    if not text or not isinstance(text, str):
        logger.warning("Invalid input to rule_based_emergency")
        return False
    
    text = text.lower()
    is_emerg = any(rule in text for rule in EMERGENCY_RULES)
    if is_emerg:
        logger.warning(f"Emergency detected: {text[:100]}")
    return is_emerg

def ai_emergency_check(llm, text):
    if not text or not isinstance(text, str):
        logger.warning("Invalid input to ai_emergency_check")
        return False
    
    try:
        prompt = f"""
You are a medical safety classifier.
Answer ONLY yes or no.

Is this a medical emergency:
{text[:500]}
"""
        response = llm.generate("Medical safety check", prompt)
        is_emerg = "yes" in response.lower()
        if is_emerg:
            logger.warning(f"AI detected emergency: {text[:100]}")
        return is_emerg
    except Exception as e:
        logger.error(f"AI emergency check failed: {e}")
        # Fail safe - treat errors as potential emergencies
        return False

INFANT_DANGER_SIGNS = [
    "not feeding",
    "lethargic",
    "blue lips",
    "fast breathing",
    "fever in infant",
    "convulsion"
]

def infant_emergency(text):
    if not text or not isinstance(text, str):
        logger.warning("Invalid input to infant_emergency")
        return False
    
    text = text.lower()
    is_emerg = any(sign in text for sign in INFANT_DANGER_SIGNS)
    if is_emerg:
        logger.warning(f"Infant emergency detected: {text[:100]}")
    return is_emerg
