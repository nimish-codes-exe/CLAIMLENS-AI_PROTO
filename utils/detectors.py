def detect_clickbait(text):
    return {"score": 0, "count": 0, "penalty": 0, "terms_found": []}

def detect_manipulation(text):
    return {"score": 0, "count": 0, "penalty": 0, "terms_found": []}

def detect_credibility(text):
    return {"score": 50, "count": 0, "bonus": 0, "terms_found": []}

def analyze_text_metrics(text):
    return {
        "char_count": len(text),
        "word_count": len(text.split()),
        "sentence_count": text.count("."),
        "exclamation_count": text.count("!"),
        "caps_ratio": 0
    }

def find_similar_evidence(claim, top_k=5, evidence_path="evidence.csv"):
    return {
        "top_similarity": 0.75,
        "source_reliability": 80,
        "matches": []
    }

def compute_trust_score(
        similarity_score,
        source_reliability,
        clickbait_penalty,
        manipulation_penalty,
        credibility_bonus):

    score = (
        40 +
        similarity_score * 35 +
        source_reliability * 0.15 +
        credibility_bonus -
        clickbait_penalty -
        manipulation_penalty
    )

    score = max(0, min(100, score))

    return {
        "trust_score": score,
        "sim_component": similarity_score * 35,
        "reliability_component": source_reliability * 0.15,
        "credibility_bonus": credibility_bonus,
        "clickbait_penalty": clickbait_penalty,
        "manipulation_penalty": manipulation_penalty
    }

def get_verdict(score):
    if score >= 80:
        return {
            "verdict": "VERIFIED",
            "icon": "✅",
            "confidence": "HIGH",
            "color": "#00e676",
            "bg_color": "rgba(0,230,118,0.08)",
            "explanation": "Claim strongly matches trusted evidence."
        }

    elif score >= 60:
        return {
            "verdict": "LIKELY TRUE",
            "icon": "🟡",
            "confidence": "MEDIUM",
            "color": "#ffd740",
            "bg_color": "rgba(255,215,64,0.08)",
            "explanation": "Claim has moderate evidence support."
        }

    else:
        return {
            "verdict": "LIKELY FALSE",
            "icon": "❌",
            "confidence": "LOW",
            "color": "#ff1744",
            "bg_color": "rgba(255,23,68,0.08)",
            "explanation": "Claim lacks sufficient evidence."
        }