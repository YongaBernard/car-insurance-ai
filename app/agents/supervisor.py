from openai import OpenAI

from app.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def supervisor_agent(claim_description: str) -> str:
    """
    Supervisor Agent

    Determines which specialist agents should be involved
    in processing an insurance claim.

    The supervisor does not make the final insurance decision.
    """

    prompt = f"""
You are the Supervisor Agent in a multi-agent
car insurance claim assessment system.

Your job is to determine which specialist agents
should process the claim.

Available specialist agents:

1. policy_agent
   - Examines insurance coverage and policy conditions.

2. vision_agent
   - Examines accident photographs and visible vehicle damage.

3. claims_agent
   - Analyses the claim circumstances and identifies
     important claim information.

4. rag_agent
   - Retrieves relevant information from the insurance
     knowledge base and policy documents.

5. decision_agent
   - Produces the final assessment using the information
     gathered by the other agents.

Claim description:

{claim_description}

Return ONLY a comma-separated list containing the
agents that should be involved.

Example:

policy_agent, vision_agent, claims_agent, rag_agent, decision_agent

Rules:

- Normally include policy_agent.
- Include vision_agent when an accident photograph is available.
- Include claims_agent for claim circumstances.
- Include rag_agent when policy or knowledge-base information
  is required.
- decision_agent should normally be included last.
- Do not make the insurance decision yourself.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt,
    )

    return response.output_text.strip()