import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def find_similar_evidence(claim, top_k=5, evidence_path="evidence.csv"):

    df = pd.read_csv(evidence_path)

    claim_emb = model.encode([claim])

    evidence_emb = model.encode(
        df["claim"].astype(str).tolist()
    )

    sims = cosine_similarity(
        claim_emb,
        evidence_emb
    )[0]

    df["similarity"] = sims

    top = df.sort_values(
        "similarity",
        ascending=False
    ).head(top_k)

    matches = []

    for _, row in top.iterrows():

        matches.append({
            "claim": row["claim"],
            "evidence": row["evidence"],
            "label": row["label"],
            "category": row["category"],
            "similarity": float(row["similarity"])
        })

    return {
        "top_similarity": float(top.iloc[0]["similarity"]),
        "source_reliability": 85,
        "matches": matches
    }