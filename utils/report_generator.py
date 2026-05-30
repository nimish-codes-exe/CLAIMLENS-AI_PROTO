from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(
        claim,
        trust_score,
        verdict,
        score_breakdown,
        clickbait,
        manipulation,
        credibility,
        evidence_matches,
        text_metrics):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "ClaimLens AI Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            f"<b>Claim:</b> {claim}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Trust Score:</b> {trust_score:.2f}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Verdict:</b> {verdict['verdict']}",
            styles["BodyText"]
        )
    )

    doc.build(content)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf