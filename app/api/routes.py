from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.graph.insurance_graph import insurance_graph


router = APIRouter()


@router.post("/assess-claim")
async def assess_claim(
    customer_name: str = Form(...),
    policy_number: str = Form(...),
    vehicle_registration: str = Form(...),
    claim_description: str = Form(...),
    image: UploadFile = File(...),
):
    """
    Receive an insurance claim and accident photograph,
    save the image locally, and send the claim through
    the multi-agent insurance assessment graph.
    """

    # ---------------------------------------------------------
    # 1. Validate uploaded image
    # ---------------------------------------------------------

    allowed_types = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }

    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format. Use JPG, PNG, or WEBP.",
        )

    # ---------------------------------------------------------
    # 2. Create claims upload directory
    # ---------------------------------------------------------

    upload_directory = Path("data/claims")
    upload_directory.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # 3. Generate a unique filename
    # ---------------------------------------------------------

    extension = allowed_types[image.content_type]

    filename = f"{uuid.uuid4().hex}{extension}"

    image_path = upload_directory / filename

    # ---------------------------------------------------------
    # 4. Save uploaded image
    # ---------------------------------------------------------

    try:
        with image_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to save uploaded image: {exc}",
        )

    # ---------------------------------------------------------
    # 5. Run the insurance AI graph
    # ---------------------------------------------------------

    try:
        result = insurance_graph.invoke(
            {
                "customer_name": customer_name,
                "policy_number": policy_number,
                "vehicle_registration": vehicle_registration,
                "claim_description": claim_description,
                "image_path": str(image_path),
            }
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Claim assessment failed: {exc}",
        )

    # ---------------------------------------------------------
    # 6. Return structured assessment
    # ---------------------------------------------------------

    return {
        "status": result.get("status", "completed"),

        "customer_name": customer_name,

        "policy_number": policy_number,

        "vehicle_registration": vehicle_registration,

        "human_review_required": result.get(
            "human_review_required",
            True,
        ),

        "policy_assessment": result.get(
            "policy_assessment",
            "",
        ),

        "damage_assessment": result.get(
            "damage_assessment",
            "",
        ),

        "final_decision": result.get(
            "final_decision",
            "",
        ),
    }