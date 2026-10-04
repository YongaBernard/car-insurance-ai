import os
import chromadb

from app.rag.embeddings import create_embedding


POLICY_PATH = "data/policies/sample_car_insurance_policy.txt"
CHROMA_PATH = "chroma_db"


def ingest_policy():
    with open(POLICY_PATH, "r", encoding="utf-8") as file:
        policy_text = file.read()

    # Split the policy into manageable sections
    sections = [
        section.strip()
        for section in policy_text.split("\n\n")
        if section.strip()
    ]

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(
        name="insurance_policies"
    )

    for index, section in enumerate(sections):
        embedding = create_embedding(section)

        collection.upsert(
            ids=[f"policy_section_{index}"],
            documents=[section],
            embeddings=[embedding],
            metadatas=[{
                "source": "sample_car_insurance_policy.txt",
                "section": index,
            }],
        )

    print(f"Successfully ingested {len(sections)} policy sections.")


if __name__ == "__main__":
    ingest_policy()