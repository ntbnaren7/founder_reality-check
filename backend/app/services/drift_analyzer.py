from typing import List, Optional
from ..models import StartupSnapshot, DriftItem
from .llm_client import llm_client

def analyze_drift(old_snapshot: StartupSnapshot, new_snapshot: StartupSnapshot) -> List[DriftItem]:
    """
    Compares two snapshots and detects drift.
    """
    # Simple field comparison first
    fields_to_check = ["target_user", "problem", "solution", "primary_channel_type", "hypothesis"]
    drift_items = []
    
    for field in fields_to_check:
        old_val = getattr(old_snapshot, field)
        new_val = getattr(new_snapshot, field)
        
        if old_val != new_val:
            # Use LLM to classify the change
            prompt = f"""
            Compare these two values for the field '{field}':
            Old: "{old_val}"
            New: "{new_val}"
            
            Is this a "major_change" (pivot, completely different audience/problem) or a "minor_refinement" (clarification, rewording)?
            
            Output JSON:
            {{
                "classification": "major_change" | "minor_refinement",
                "comment": "Brief explanation of the change"
            }}
            """
            result = llm_client.generate_json(prompt)
            
            drift_items.append(DriftItem(
                field=field,
                before=str(old_val),
                after=str(new_val),
                classification=result["classification"],
                comment=result["comment"]
            ))
            
    return drift_items
