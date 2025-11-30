from .llm_client import llm_client

def validate_target_user(target_user: str) -> dict:
    """
    Validates if the target user is concrete enough.
    Returns: { "is_valid": bool, "reason": str, "improved_target_user": str }
    """
    if not target_user or len(target_user.strip()) < 5:
        return {
            "is_valid": False,
            "reason": "Target user is missing or too short.",
            "improved_target_user": "Specific role in a specific industry (e.g., 'HR Managers in Series B Tech Companies')."
        }

    prompt = f"""
    Evaluate the concreteness of this target user definition: "{target_user}"
    
    Rules:
    1. It must define WHO (role/person).
    2. It must define WHERE (context/environment).
    3. It must define WHAT they are doing (behavior/job).
    
    Examples:
    - BAD: "anyone who uses the internet", "startups", "students".
    - GOOD: "early-stage B2B SaaS founders at seed/pre-seed preparing their first pitch deck".
    
    Output JSON:
    {{
        "is_valid": boolean,
        "reason": "explanation of why it is valid or invalid",
        "improved_target_user": "a more concrete version if invalid, else null"
    }}
    """
    
    return llm_client.generate_json(prompt)
