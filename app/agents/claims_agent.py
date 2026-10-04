from openai import OpenAI

from app.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def claims_agent(claim_description: str) -> str:
    """
    Claims Agent

    Analyses the circumstances of an insurance claim
    and identifies important information for assessment.

    This agent does not make the final insurance decision.
    """

    prompt = f"""
You are the Claims Agent in a professional
car insurance claims assessment system.

Analyse the following claim description:

{claim_description}

Identify:

1. What happened according to the claimant
2. The type of incident
3. Important facts contained in the description
4. Information that may be missing
5. Potential inconsistencies or uncertainties
6. Additional evidence that should be requested
7. Whether human review may be required

Important rules:

- Only use information provided in the claim description.
- Do not invent facts.
- Do not determine whether the claim should be paid.
- Do not make a legally binding insurance decision.
- Clearly identify uncertainty.
- Recommend additional evidence when information is insufficient.

Return a concise professional claims analysis.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt,
    )

    return response.output_text.strip()