# main_agent.py

import logging
from ai_core.safety_guard import (
    rule_based_emergency,
    infant_emergency,
    ai_emergency_check
)
from ai_core.emergency_handler import handle_emergency
from ai_core.symptom_analyzer import analyze_symptoms
from ai_core.disease_risk_engine import assess_risk
from ai_core.llm_client import GroqLLM
from utils.rag_engine import MedicalRAG
from utils.helpers import save_record
from utils.report_generator import generate_doctor_report

logger = logging.getLogger(__name__)


class MedicalAgent:
    """
    Core medical intelligence orchestrator.
    Streamlit-independent business logic.
    """

    def __init__(self):
        try:
            self.llm = GroqLLM()
            self.rag = MedicalRAG()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize MedicalAgent: {e}")

    def process_query(self, user_input: str, user_type: str):
        """
        Main pipeline:
        - Emergency detection
        - Symptom analysis
        - Risk assessment
        - RAG + LLM response
        """
        
        # Input validation
        if not user_input or not user_input.strip():
            raise ValueError("User input cannot be empty")
        
        if len(user_input) > 5000:
            raise ValueError("Input exceeds maximum length of 5000 characters")
        
        if user_type not in ["Adult", "Infant"]:
            raise ValueError(f"Invalid user_type: {user_type}. Must be 'Adult' or 'Infant'")
        
        # Sanitize input
        user_input = user_input.strip()
        
        logger.info(f"Processing query for {user_type}: {user_input[:100]}...")

        try:
            # --- Emergency Checks ---
            if user_type == "Infant":
                if infant_emergency(user_input):
                    logger.critical(f"Infant emergency detected: {user_input[:100]}")
                    return {
                        "emergency": True,
                        "message": handle_emergency()
                    }
            else:
                if rule_based_emergency(user_input) or ai_emergency_check(self.llm, user_input):
                    logger.critical(f"Emergency detected: {user_input[:100]}")
                    return {
                        "emergency": True,
                        "message": handle_emergency()
                    }

            # --- Symptom & Risk Analysis ---
            symptoms = analyze_symptoms(user_input)
            risk = assess_risk(symptoms)

            # --- RAG Retrieval ---
            context = self.rag.retrieve(user_input)

            # --- LLM Response ---
            system_prompt = (
                f"You are a safe medical assistant for {user_type.lower()} patients. "
                "Do not diagnose. Provide general guidance only. "
                "Always recommend consulting a healthcare professional for proper diagnosis."
            )

            response = self.llm.generate(
                system_prompt=system_prompt,
                user_prompt=f"Context:\n{context}\n\nUser Symptoms:\n{user_input}"
            )

            # --- Save Record ---
            try:
                save_record(
                    user_input,
                    risk.get("risk_level", "Unknown"),
                    risk.get("score", 0)
                )
            except Exception as e:
                logger.error(f"Failed to save record: {e}")
                # Don't fail the whole request if saving fails

            return {
                "emergency": False,
                "symptoms": symptoms,
                "risk": risk,
                "response": response,
                "report": generate_doctor_report(user_input, risk, response)
            }
        
        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            raise RuntimeError(f"Failed to process medical query: {e}")