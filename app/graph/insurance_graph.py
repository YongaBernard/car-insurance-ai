from langgraph.graph import StateGraph, START, END

from app.models.assessment import ClaimAssessmentState

from app.agents.policy_agent import policy_agent
from app.agents.vision_agent import vision_agent
from app.agents.claims_agent import claims_agent
from app.agents.rag_agent import rag_agent
from app.agents.decision_agent import decision_agent


# =========================================================
# POLICY AGENT
# =========================================================

def policy_node(state: ClaimAssessmentState):

    result = policy_agent(
        state["claim_description"]
    )

    return {
        "policy_assessment": result
    }


# =========================================================
# VISION AGENT
# =========================================================

def vision_node(state: ClaimAssessmentState):

    result = vision_agent(
        state["image_path"]
    )

    return {
        "damage_assessment": result
    }


# =========================================================
# CLAIMS AGENT
# =========================================================

def claims_node(state: ClaimAssessmentState):

    result = claims_agent(
        state["claim_description"]
    )

    return {
        "claim_assessment": result
    }


# =========================================================
# RAG AGENT
# =========================================================

def rag_node(state: ClaimAssessmentState):

    result = rag_agent(
        state["claim_description"]
    )

    return {
        "rag_context": result
    }


# =========================================================
# DECISION AGENT
# =========================================================

def decision_node(state: ClaimAssessmentState):

    result = decision_agent(
        policy_assessment=state.get(
            "policy_assessment",
            ""
        ),
        damage_assessment=state.get(
            "damage_assessment",
            ""
        ),
        claim_description=state["claim_description"]
    )

    return {
        "final_decision": result,
        "status": "completed",
        "human_review_required": True
    }


# =========================================================
# BUILD MULTI-AGENT GRAPH
# =========================================================

def build_insurance_graph():

    graph = StateGraph(
        ClaimAssessmentState
    )

    # -----------------------------------------------------
    # Register agents
    # -----------------------------------------------------

    graph.add_node(
        "policy_agent",
        policy_node
    )

    graph.add_node(
        "vision_agent",
        vision_node
    )

    graph.add_node(
        "claims_agent",
        claims_node
    )

    graph.add_node(
        "rag_agent",
        rag_node
    )

    graph.add_node(
        "decision_agent",
        decision_node
    )

    # -----------------------------------------------------
    # Workflow
    # -----------------------------------------------------

    graph.add_edge(
        START,
        "policy_agent"
    )

    graph.add_edge(
        "policy_agent",
        "vision_agent"
    )

    graph.add_edge(
        "vision_agent",
        "claims_agent"
    )

    graph.add_edge(
        "claims_agent",
        "rag_agent"
    )

    graph.add_edge(
        "rag_agent",
        "decision_agent"
    )

    graph.add_edge(
        "decision_agent",
        END
    )

    # -----------------------------------------------------
    # Compile graph
    # -----------------------------------------------------

    return graph.compile()


# =========================================================
# APPLICATION GRAPH
# =========================================================

insurance_graph = build_insurance_graph()