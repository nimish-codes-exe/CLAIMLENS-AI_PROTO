def compute_trust_score(
        similarity_score,
        source_reliability,
        clickbait_penalty,
        manipulation_penalty,
        credibility_bonus):

    sim_component = similarity_score * 35
    reliability_component = source_reliability * 0.15

    score = (
        40 +
        sim_component +
        reliability_component +
        credibility_bonus -
        clickbait_penalty -
        manipulation_penalty
    )

    score = max(0, min(score, 100))

    return {
        "trust_score": score,
        "sim_component": sim_component,
        "reliability_component": reliability_component,
        "credibility_bonus": credibility_bonus,
        "clickbait_penalty": clickbait_penalty,
        "manipulation_penalty": manipulation_penalty
    }


def get_verdict(score):

    if score >= 85:
        return {
            "verdict": "VERIFIED",
            "icon": "✅",
            "confidence": "HIGH",
            "color": "#00e676",
            "bg_color": "rgba(0,230,118,0.08)",
            "explanation": "Claim strongly aligns with trusted evidence."
        }

    elif score >= 70:
        return {
            "verdict": "LIKELY TRUE",
            "icon": "🟡",
            "confidence": "MEDIUM",
            "color": "#ffd740",
            "bg_color": "rgba(255,215,64,0.08)",
            "explanation": "Claim appears credible but should be independently verified."
        }

    elif score >= 50:
        return {
            "verdict": "UNCERTAIN",
            "icon": "⚠️",
            "confidence": "MEDIUM",
            "color": "#ff9800",
            "bg_color": "rgba(255,152,0,0.08)",
            "explanation": "Insufficient evidence exists for a confident decision."
        }

    else:
        return {
            "verdict": "LIKELY FALSE",
            "icon": "❌",
            "confidence": "LOW",
            "color": "#ff1744",
            "bg_color": "rgba(255,23,68,0.08)",
            "explanation": "Strong misinformation indicators detected."
        }