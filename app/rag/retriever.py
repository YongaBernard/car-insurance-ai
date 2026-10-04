import chromadb

from app.rag.embeddings import create_embedding


CHROMA_PATH = "chroma_db"


def retrieve_policy(query: str, top_k: int = 4) -> list[str]:
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_collection(
        name="insurance_policies"
    )

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]

    return documents


if __name__ == "__main__":
    query = "Is accidental front-end collision damage covered?"

    results = retrieve_policy(query)

    print("\nRelevant policy sections:\n")

    for index, result in enumerate(results, start=1):
        print(f"--- Result {index} ---")
        print(result)
        print()