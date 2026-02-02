import os
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
logger = logging.getLogger(__name__)

class GroqLLM:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        try:
            self.client = ChatGroq(
                groq_api_key=api_key,
                model="llama-3.3-70b-versatile",
                temperature=0.2
            )
            logger.info("GroqLLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize GroqLLM: {e}")
            raise

    def generate(self, system_prompt, user_prompt):
        if not system_prompt or not user_prompt:
            raise ValueError("Both system_prompt and user_prompt are required")
        
        # Input validation - prevent extremely long prompts
        if len(user_prompt) > 10000:
            raise ValueError("User prompt exceeds maximum length of 10000 characters")
        
        try:
            messages = [
                ("system", system_prompt),
                ("human", user_prompt)
            ]
            response = self.client.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise RuntimeError(f"Failed to generate response: {e}")