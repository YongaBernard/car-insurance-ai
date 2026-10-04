from typing import TypedDict, Optional


class ClaimAssessmentState(TypedDict, total=False):
    claim_description: str
    image_path: Optional[str]

    # Supervisor routing
    selected_agents: str

    # Agent assessments
    policy_assessment: str
    damage_assessment: str
    claims_assessment: str
    rag_context: str

    # Final assessment
    final_decision: str
    status: str
    human_review_required: bool