from openai import OpenAI

from app.config import OPENAI_API_KEY
from app.rag.retriever import retrieve_policy


client = OpenAI(api_key=OPENAI_API_KEY)


def rag_agent(claim_description: str) -> str:
    """
    Retrieve relevant insurance policy information and
    explain how it relates to the submitted claim.

    The RAG Agent provides policy evidence only.
    It does not make the final insurance decision.
    """

    # ---------------------------------------------------------
    # 1. Retrieve relevant policy sections
    # ---------------------------------------------------------

    policy_documents = retrieve_policy(
        claim_description,
        top_k=4,
    )

    # ---------------------------------------------------------
    # 2. Handle missing policy information
    # ---------------------------------------------------------

    if not policy_documents:
        return (
            "No relevant insurance policy information "
            "was found for this claim."
        )

    # ---------------------------------------------------------
    # 3. Combine retrieved policy sections
    # ---------------------------------------------------------

    policy_context = "\n\n".join(
        f"Policy Section {index + 1}:\n{document}"
        for index, document in enumerate(policy_documents)
    )

    # ---------------------------------------------------------
    # 4. Ask the AI to analyse the policy evidence
    # ---------------------------------------------------------

    prompt = f"""
You are the RAG Policy Evidence Agent in a professional
car insurance claims assessment system.

Your task is to analyse the retrieved insurance policy
information in relation to the customer's claim.

CLAIM DESCRIPTION:
{claim_description}

RETRIEVED POLICY INFORMATION:
{policy_context}

Provide a concise professional assessment covering:

1. Relevant policy coverage
2. Important policy conditions
3. Relevant exclusions
4. Excess or limitations if stated
5. Whether the claim appears potentially covered
6. What additional information is required
7. Whether human review is recommended

Important rules:

- Base your assessment only on the retrieved policy information.
- Do not invent policy terms.
- Do not invent coverage limits.
- Do not make a legally binding insurance decision.
- If the retrieved information is insufficient, clearly state this.
- Quote or reference the relevant policy wording where useful.
- Flag uncertainty and recommend human review when appropriate.
"""

    # ---------------------------------------------------------
    # 5. Generate policy assessment
    # ---------------------------------------------------------

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt,
    )

    # ---------------------------------------------------------
    # 6. Return the assessment
    # ---------------------------------------------------------

    return response.output_text