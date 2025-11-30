from typing import List
from .llm_client import llm_client

def enforce_channel(channel_text: str) -> dict:
    """
    Enforces a single primary channel and specific description.
    """
    if not channel_text:
        return {
            "primary_channel_type": None,
            "primary_channel_description": None,
            "other_channels": [],
            "issues": ["No distribution channel defined."]
        }

    prompt = f"""
    Analyze this distribution strategy: "{channel_text}"
    
    Allowed Types: ["cold_outreach", "community", "paid_ads", "partnerships", "marketplace", "product_led"]
    
    Task:
    1. Identify the ONE primary channel type.
    2. Extract a specific, executable description for it.
    3. List any other channels mentioned as 'other_channels'.
    4. Flag issues if the description is vague (e.g., "go viral", "social media" without platform/strategy).
    
    Output JSON:
    {{
        "primary_channel_type": "string (enum) or null",
        "primary_channel_description": "string",
        "other_channels": ["string"],
        "issues": ["string"]
    }}
    """
    
    return llm_client.generate_json(prompt)
