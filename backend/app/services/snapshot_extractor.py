from ..models import StartupSnapshot
from .llm_client import llm_client
from datetime import datetime

def extract_snapshot(startup_id: str, input_text: str, current_version: int) -> StartupSnapshot:
    """
    Extracts a StartupSnapshot from raw text using the LLM.
    """
    prompt = f"""
    You are an expert startup analyst.
    Analyze the following text from a founder describing their startup idea.
    Extract key information into a structured JSON format.
    
    Input Text:
    "{input_text}"
    
    Extract the following fields:
    - problem: The core problem they are solving.
    - target_user: Who they think is the user (keep it close to their words).
    - job_to_be_done: What the user is trying to achieve.
    - solution: The proposed solution.
    - value_prop: The core value proposition.
    - primary_channel_type: One of ["cold_outreach", "community", "paid_ads", "partnerships", "marketplace", "product_led"]. If unsure or multiple, pick the most dominant one mentioned, or null if none.
    - primary_channel_description: Specific details about the channel.
    - hypothesis: Their core hypothesis if stated.
    - metric: Key metric they mentioned or implied.
    - timeframe: Timeframe mentioned or implied.
    - tech_feasibility_notes: Any technical risks or notes.
    - top_risks: List of top risks.
    - declared_next_steps: List of next steps they mentioned.

    If a field is not present, leave it null or empty.
    """
    
    # We don't enforce strict schema validation in the prompt for every field to allow flexibility,
    # but we cast it to the Pydantic model.
    data = llm_client.generate_json(prompt)
    
    # Ensure required fields for the model
    data["startup_id"] = startup_id
    data["version"] = current_version + 1
    data["timestamp"] = datetime.utcnow().isoformat()
    
    return StartupSnapshot(**data)
