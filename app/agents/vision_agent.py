import base64
from pathlib import Path

from openai import OpenAI

from app.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def vision_agent(image_path: str) -> str:
    """
    Analyse a vehicle accident image and identify visible damage.

    The agent provides an observational assessment only.
    It does not make a legally binding insurance decision.
    """

    # ---------------------------------------------------------
    # 1. Validate image path
    # ---------------------------------------------------------

    image_file = Path(image_path)

    if not image_file.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    # ---------------------------------------------------------
    # 2. Determine image MIME type
    # ---------------------------------------------------------

    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }

    extension = image_file.suffix.lower()
    mime_type = mime_types.get(extension)

    if mime_type is None:
        raise ValueError(
            "Unsupported image format. "
            "Use JPG, JPEG, PNG, or WEBP."
        )

    # ---------------------------------------------------------
    # 3. Convert image to Base64
    # ---------------------------------------------------------

    with open(image_file, "rb") as file:
        image_data = base64.b64encode(
            file.read()
        ).decode("utf-8")

    image_url = (
        f"data:{mime_type};base64,{image_data}"
    )

    # ---------------------------------------------------------
    # 4. Vision assessment instructions
    # ---------------------------------------------------------

    prompt = """
You are the Vision Agent in a professional
car insurance claims assessment system.

Analyse the provided vehicle accident photograph.

Identify:

1. Vehicle damage visible in the image
2. Damaged components or body panels
3. Apparent severity of the damage
4. Whether the visible damage appears consistent
   with a road traffic accident
5. Any visible safety concerns
6. Any uncertainty or limitations in the photograph
7. Whether a human inspection should be recommended

Important rules:

- Only describe what can reasonably be observed
  from the photograph.
- Do not invent damage that cannot be seen.
- Do not estimate an exact repair cost.
- Do not make a legally binding insurance decision.
- Do not determine whether the claim should be paid.
- If hidden structural or mechanical damage cannot be
  determined from the image, explicitly say so.
- Recommend human inspection when the photograph is
  insufficient to confidently assess the damage.

Return a concise professional damage assessment.
"""

    # ---------------------------------------------------------
    # 5. Send image to OpenAI Vision model
    # ---------------------------------------------------------

    response = client.responses.create(
        model="gpt-6-luna",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                    {
                        "type": "input_image",
                        "image_url": image_url,
                    },
                ],
            }
        ],
    )

    # ---------------------------------------------------------
    # 6. Return the model's assessment
    # ---------------------------------------------------------

    return response.output_text