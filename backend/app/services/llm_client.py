import os
import json
import google.generativeai as genai
from typing import Any, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
# Expects GOOGLE_API_KEY in environment variables
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Use a model that supports JSON mode well
MODEL_NAME = "gemini-2.0-flash"
class LLMClient:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)

    def generate_json(self, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generates JSON output from the LLM.
        """
        try:
            full_prompt = f"{prompt}\n\nOutput strictly valid JSON."
            if schema:
                full_prompt += f"\nFollow this schema structure:\n{json.dumps(schema, indent=2)}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            return json.loads(response.text)
        except Exception as e:
            print(f"LLM Error: {e}")
            # Fallback or re-raise depending on severity
            raise e

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"LLM Error: {e}")
            raise e

llm_client = LLMClient()
