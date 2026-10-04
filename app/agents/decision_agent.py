from openai import OpenAI

from app.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def decision_agent(
    policy_assessment: str,
    damage_assessment: str,
    claim_description: str,
) -> str:
    """
    Produce a final insurance claim recommendation
    based on the outputs of other agents.
    """

    prompt = f"""
You are the final decision-support agent in a car insurance
claims assessment system.

You must evaluate the information provided by other AI agents
and produce a structured recommendation for a human insurance
professional.

CLAIM:
{claim_description}

POLICY ASSESSMENT:
{policy_assessment}

DAMAGE ASSESSMENT:
{damage_assessment}

Provide:

1. Overall assessment
2. Coverage status
3. Damage summary
4. Recommended action
5. Human review requirement
6. Confidence level
7. Reasoning

Possible recommended actions:
- APPROVE_FOR_REVIEW
- REQUEST_MORE_INFORMATION
- ESCALATE_TO_HUMAN
- POTENTIAL_FRAUD_REVIEW

IMPORTANT:
This is decision support only.
Do not make a legally binding insurance decision.
When information is incomplete or uncertain, recommend
human review.

Return a concise professional assessment.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt,
    )

    return response.output_text