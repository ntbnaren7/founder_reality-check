from .llm_client import llm_client

def enforce_hypothesis(snapshot_data: dict) -> dict:
    """
    Structures the hypothesis and checks for vanity metrics.
    """
    user = snapshot_data.get("target_user", "")
    solution = snapshot_data.get("solution", "")
    channel = snapshot_data.get("primary_channel_type", "")
    raw_hypothesis = snapshot_data.get("hypothesis", "")
    
    prompt = f"""
    Construct or refine a structured hypothesis for this startup.
    
    Context:
    - User: {user}
    - Solution: {solution}
    - Channel: {channel}
    - Raw Hypothesis: {raw_hypothesis}
    
    Template: "For <target_user>, if we offer <solution> through <channel>, then within <timeframe> we expect <measurable change in <metric>>."
    
    Task:
    1. Create a structured hypothesis sentence.
    2. Extract/Define the 'metric'.
    3. Extract/Define the 'timeframe'.
    4. Flag issues if the metric is a vanity metric (likes, views) or timeframe is unrealistic.
    
    Output JSON:
    {{
        "hypothesis": "string",
        "metric": "string",
        "timeframe": "string",
        "issues": ["string"]
    }}
    """
    
    return llm_client.generate_json(prompt)
