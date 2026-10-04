from openai import OpenAI

from app.config import OPENAI_API_KEY
from app.rag.retriever import retrieve_policy


client = OpenAI(api_key=OPENAI_API_KEY)


def policy_agent(claim_description: str) -> str:
    """
    Analyse a car insurance claim using relevant policy
    information retrieved from ChromaDB.
    """

    # Retrieve the most relevant policy sections
    policy_sections = retrieve_policy(
        claim_description,
        top_k=4,
    )

    policy_context = "\n\n".join(policy_sections)

    prompt = f"""
You are an insurance policy analysis agent
in a car insurance claims assessment system.

Your task is to analyse whether a reported car insurance
claim appears to be covered based on the retrieved policy
information.

CLAIM:
{claim_description}

RELEVANT POLICY INFORMATION:
{policy_context}

Analyse:

1. Whether the claim appears to be covered.
2. Which policy conditions support your conclusion.
3. Any exclusions or limitations that may apply.
4. What additional information may be required.
5. Whether human review is required.

IMPORTANT:

- Use only the provided policy information.
- Do not invent policy terms.
- Do not make a legally binding insurance decision.
- If information is incomplete or uncertain, recommend human review.

Return a concise professional assessment.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt,
    )

    return response.output_text


if __name__ == "__main__":
    claim = (
        "My car was damaged in a road accident "
        "after colliding with another vehicle. "
        "The front bumper and headlight are damaged."
    )

    print(policy_agent(claim))