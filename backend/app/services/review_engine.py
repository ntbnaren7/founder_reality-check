from typing import List, Tuple
from ..models import StartupSnapshot, DimensionReview, Experiment, DriftItem
from .llm_client import llm_client

def generate_reviews_and_experiments(snapshot: StartupSnapshot, validation_issues: dict) -> Tuple[List[DimensionReview], List[Experiment], str]:
    """
    Generates dimension reviews and experiments based on the snapshot and validation results.
    """
    
    # 1. Compile Reviews
    reviews = []
    status = "OK"
    
    # User Review
    user_valid = validation_issues.get("user", {}).get("is_valid", True)
    reviews.append(DimensionReview(
        dimension="User",
        severity="blocker" if not user_valid else "ok",
        issue=None if user_valid else validation_issues["user"].get("reason"),
        recommendation=None if user_valid else f"Try: {validation_issues['user'].get('improved_target_user')}"
    ))
    
    # Channel Review
    channel_issues = validation_issues.get("channel", {}).get("issues", [])
    reviews.append(DimensionReview(
        dimension="Distribution",
        severity="blocker" if channel_issues else "ok",
        issue="; ".join(channel_issues) if channel_issues else None,
        recommendation="Pick one concrete channel." if channel_issues else None
    ))
    
    # Hypothesis Review
    hypo_issues = validation_issues.get("hypothesis", {}).get("issues", [])
    reviews.append(DimensionReview(
        dimension="Hypothesis",
        severity="major" if hypo_issues else "ok",
        issue="; ".join(hypo_issues) if hypo_issues else None,
        recommendation="Refine metric and timeframe." if hypo_issues else None
    ))
    
    if any(r.severity == "blocker" for r in reviews):
        status = "BLOCKED"
        
    # 2. Generate Experiments (only if not completely blocked on user/channel basics)
    experiments = []
    if status != "BLOCKED":
        prompt = f"""
        Design 3 minimal, concrete experiments for this startup to validate their hypothesis.
        
        Context:
        - User: {snapshot.target_user}
        - Hypothesis: {snapshot.hypothesis}
        - Channel: {snapshot.primary_channel_type} ({snapshot.primary_channel_description})
        
        Output JSON:
        [
            {{
                "title": "string",
                "channel_type": "{snapshot.primary_channel_type}",
                "steps": ["step 1", "step 2"],
                "success_criteria": "string",
                "time_cost": "string"
            }}
        ]
        """
        exps_data = llm_client.generate_json(prompt)
        if isinstance(exps_data, list):
            for e in exps_data:
                experiments.append(Experiment(**e))
        elif isinstance(exps_data, dict) and "experiments" in exps_data:
             for e in exps_data["experiments"]:
                experiments.append(Experiment(**e))

    return reviews, experiments, status
