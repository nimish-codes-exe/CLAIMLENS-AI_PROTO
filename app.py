import sys, os

sys.path.insert(0, os.path.dirname(__file__))
import hashlib


import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="ClaimLens AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)
if "blockchain_records" not in st.session_state:
    st.session_state.blockchain_records = []

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;600;700;800&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background-color: #0f172a !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Sidebar headings */

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: white !important;
}

/* Radio labels */

[data-testid="stSidebar"] .stRadio label {
    color: #cbd5e1 !important;
}

/* Toggle labels */

[data-testid="stSidebar"] .stToggle label {
    color: #cbd5e1 !important;
}

/* Slider labels */

[data-testid="stSidebar"] .stSlider label {
    color: #cbd5e1 !important;
}

/* Metric text */

[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: #00e5ff !important;
    font-weight: 700;
}

[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

/* Titles */
h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    letter-spacing: -0.02em;
}

/* Cards */
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
    backdrop-filter: blur(8px);
}
.verdict-card {
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    text-align: center;
}
.metric-chip {
    background: rgba(0,229,255,0.12);
    border: 1px solid rgba(0,229,255,0.25);
    color: #67e8f9;
}
.term-badge {
    display: inline-block;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    margin: 2px;
}
.badge-red   { background: rgba(255,23,68,0.15);   border: 1px solid rgba(255,23,68,0.3);   color: #ff6090; }
.badge-amber { background: rgba(255,152,0,0.15);   border: 1px solid rgba(255,152,0,0.3);   color: #ffb74d; }
.badge-green { background: rgba(0,230,118,0.15);   border: 1px solid rgba(0,230,118,0.3);   color: #69f0ae; }
.badge-blue  { background: rgba(0,229,255,0.15);   border: 1px solid rgba(0,229,255,0.3);   color: #80d8ff; }

/* Pipeline steps */
.pipeline-step {
    background: rgba(0,229,255,0.06);
    border: 1px solid rgba(0,229,255,0.15);
    border-radius: 10px;
    padding: 10px 16px;
    margin: 4px 0;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.pipeline-step.active {
    background: rgba(0,229,255,0.15);
    border-color: rgba(0,229,255,0.5);
    color: #00e5ff;
}
.pipeline-step.done {
    background: rgba(0,230,118,0.08);
    border-color: rgba(0,230,118,0.3);
    color: #69f0ae;
}

/* Logo */
.logo-text {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.5rem;
    background: linear-gradient(135deg, #00e5ff, #7c4dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
}
.logo-sub {
    color: #94a3b8;
}

/* Evidence rows */
.evidence-row {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
/* Safe input styling */

textarea,
input {
    color: inherit !important;
    background-color: inherit !important;
}

/* Streamlit widgets */

[data-baseweb="input"] input {
    color: inherit !important;
}

[data-baseweb="textarea"] textarea {
    color: inherit !important;
}

[data-baseweb="select"] {
    color: inherit !important;
}

.stButton > button {
    background: linear-gradient(135deg, #00b8d4, #7c4dff) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    padding: 0.55rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}



/* Sidebar radio */
.stRadio > div { gap: 6px; }

/* Divider */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* Progress bars */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00b8d4, #7c4dff) !important;
    border-radius: 99px !important;
}

/* Alerts */
.stSuccess { background: rgba(0,230,118,0.08) !important; border-color: rgba(0,230,118,0.3) !important; }
.stWarning { background: rgba(255,152,0,0.08) !important; }
.stError   { background: rgba(255,23,68,0.08) !important; }

/* Hide Streamlit default hamburger */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

EVIDENCE_PATH = Path(__file__).parent / "evidence.csv"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

DEMO_CLAIMS = {
    "🟢 Vaccines & Clinical Trials": "COVID-19 vaccines have been tested in clinical trials with thousands of participants.",
    "🔴 5G Conspiracy": "BREAKING: 5G towers are SECRETLY spreading coronavirus and governments are covering it up! SHARE NOW!",
    "🟡 Economic Claim": "Inflation causes a reduction in the purchasing power of currency over time.",
    "🔴 Moon Landing Hoax": "EXPOSED: NASA SHOCKING secret — the moon landing was completely fabricated by the US government!",
    "🟢 Cybersecurity Fact": "Phishing is the most common cyberattack vector according to security research and data.",
    "🟡 AI Jobs": "Artificial intelligence will eventually replace many routine human job functions.",
    "🔴 Microchips in Vaccines": "URGENT: Government is injecting microchips through vaccines to track and control the population!",
    "🟢 Climate Science": "Arctic sea ice is declining based on satellite data from NASA and NSIDC.",
    "🟡 Crypto Anonymity": "Cryptocurrency transactions provide complete anonymity for users.",
    "🔴 Election Machines": "SHOCKING: Voting machines were hacked to steal the election — officials refuse to investigate!",
}

CATEGORY_ICONS = {
    "Health": "🏥", "Science": "🔬", "Technology": "💻",
    "Elections": "🗳️", "Finance": "💰", "Politics": "🏛️",
    "Cybersecurity": "🛡️", "Social Media": "📱",
    "Education": "📚", "Environment": "🌿",
}

with st.sidebar:
    st.markdown('<div class="logo-text">ClaimLens AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-sub">Misinformation Intelligence</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Demo mode
    demo_mode = st.toggle("🎯 Demo Mode", value=False,
                          help="Load predefined sample claims for stable demonstrations")

    st.markdown("---")
    st.markdown("#### 📥 Input Source")
    input_source = st.radio(
        "Select input type",
        ["Text / Claim", "News Headline", "Social Media Post", "URL (Simulated)", "Screenshot / Image"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("#### ⚙️ Analysis Settings")
    top_k = st.slider("Evidence matches to retrieve", 3, 10, 5)
    show_pipeline = st.toggle("Show processing pipeline", value=True)
    show_breakdown = st.toggle("Show score breakdown", value=True)

    st.markdown("---")
    st.markdown("#### 📊 Evidence Database")
    try:
        df_ev = pd.read_csv(EVIDENCE_PATH)
        cats = df_ev["category"].value_counts()
        st.metric("Total Evidence Entries", len(df_ev))
        for cat, count in cats.head(6).items():
            icon = CATEGORY_ICONS.get(cat, "📌")
            st.markdown(f'<span class="metric-chip">{icon} {cat}: {count}</span>', unsafe_allow_html=True)
    except Exception:
        st.warning("evidence.csv not found")

    st.markdown("---")
    st.caption("v1.0 · Built for Hackathon Demo · No external AI APIs")

col_logo, col_tagline = st.columns([3, 5])
with col_logo:
    st.markdown("""
    <h1 style="font-family:'Syne',sans-serif; font-weight:800; font-size:2.6rem;
               background:linear-gradient(135deg,#00e5ff,#7c4dff);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent;
               margin-bottom:0; letter-spacing:-0.03em;">
        🔬 ClaimLens AI
    </h1>
    <p style="color:#546e7a; font-family:'JetBrains Mono',monospace; font-size:0.78rem;
              letter-spacing:0.1em; text-transform:uppercase; margin-top:0;">
        MISINFORMATION DETECTION · SEMANTIC ANALYSIS · TRUST SCORING
    </p>
    """, unsafe_allow_html=True)
with col_tagline:
    st.markdown("""
    <div style="padding-top:18px;">
        <div style="background:rgba(0,229,255,0.06); border:1px solid rgba(0,229,255,0.15);
                    border-radius:12px; padding:12px 18px; font-size:0.85rem; color:#90a4ae;">
            Analyze claims using <strong style="color:#00e5ff">semantic embeddings</strong>,
            <strong style="color:#7c4dff">linguistic pattern detection</strong>, and a
            <strong style="color:#00e5ff">trust scoring engine</strong> — no external AI APIs required.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

PIPELINE_STEPS = [
    ("📝", "Claim Input"),
    ("🖼️", "OCR / Extraction"),
    ("🧠", "Semantic Analysis"),
    ("⚠️", "Risk Detection"),
    ("🎯", "Trust Scoring"),
    ("🗂️", "Evidence Matching"),
    ("📋", "Final Report"),
]


def render_pipeline(active_step: int = -1, done: bool = False):
    cols = st.columns(len(PIPELINE_STEPS))
    for i, (icon, label) in enumerate(PIPELINE_STEPS):
        with cols[i]:
            if done or i < active_step:
                cls = "done"
                prefix = "✓"
            elif i == active_step:
                cls = "active"
                prefix = "▶"
            else:
                cls = ""
                prefix = icon
            st.markdown(
                f'<div class="pipeline-step {cls}">'
                f'<span style="font-size:1rem">{prefix}</span>'
                f'<span style="font-size:0.8rem;font-weight:600">{label}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )




def make_gauge(value: float, title: str, color: str = "#00e5ff",
               max_val: float = 100, suffix: str = "") -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": suffix, "font": {"size": 26, "color": color, "family": "Syne"}},
        title={"text": title, "font": {"size": 12, "color": "#78909c", "family": "Syne"}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "#37474f",
                     "tickfont": {"color": "#546e7a", "size": 9}},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "rgba(0,0,0,0)",
            "bordercolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0, max_val * 0.4], "color": "rgba(255,23,68,0.12)"},
                {"range": [max_val * 0.4, max_val * 0.6], "color": "rgba(255,152,0,0.08)"},
                {"range": [max_val * 0.6, max_val * 0.8], "color": "rgba(255,215,64,0.08)"},
                {"range": [max_val * 0.8, max_val], "color": "rgba(0,230,118,0.10)"},
            ],
            "threshold": {
                "line": {"color": color, "width": 2},
                "thickness": 0.75,
                "value": value,
            },
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=10, l=10, r=10),
        height=170,
    )
    return fig


def make_bar_gauge(value: float, max_val: float, color: str, label: str):
    """Simple horizontal bar gauge using Plotly."""
    fig = go.Figure(go.Bar(
        x=[value], y=[label],
        orientation="h",
        marker_color=color,
        marker_line_width=0,
        width=0.5,
    ))
    fig.add_trace(go.Bar(
        x=[max_val - value], y=[label],
        orientation="h",
        marker_color="rgba(255,255,255,0.05)",
        marker_line_width=0,
        width=0.5,
    ))
    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(t=5, b=5, l=0, r=0),
        height=50,
        xaxis=dict(range=[0, max_val], showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False),
    )
    return fig


st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### 📝 Claim Input")

claim_text = ""

if demo_mode:
    st.info("🎯 **Demo Mode Active** — Select a predefined claim below for a stable demonstration.")
    selected_demo = st.selectbox("Select demo claim", list(DEMO_CLAIMS.keys()))
    claim_text = DEMO_CLAIMS[selected_demo]
    st.markdown(f"""
    <div style="background:rgba(0,229,255,0.06); border-left:3px solid #00e5ff;
                border-radius:8px; padding:12px 16px; font-family:'JetBrains Mono',monospace;
                font-size:0.85rem; color:#b0bec5; margin-top:8px;">
        {claim_text}
    </div>
    """, unsafe_allow_html=True)

elif input_source in ["Text / Claim", "News Headline", "Social Media Post"]:
    placeholder_map = {
        "Text / Claim": "Enter any claim, statement, or assertion to analyze...",
        "News Headline": "Paste a news headline here...",
        "Social Media Post": "Paste a tweet, post, or caption here...",
    }
    claim_text = st.text_area(
        placeholder_map[input_source],
        height=100,
        label_visibility="collapsed",
        key="main_input",
    )

elif input_source == "URL (Simulated)":
    url_input = st.text_input("Enter URL to analyze (simulation)", placeholder="https://example.com/article...")
    if url_input:
        claim_text = f"Article from {url_input}: Government officials deny new policy changes amid public pressure and growing concerns."
        st.info(f"🌐 Simulated extraction from URL: `{url_input}`")
        st.markdown(f'<div class="metric-chip">Extracted claim: {claim_text[:80]}...</div>', unsafe_allow_html=True)

elif input_source == "Screenshot / Image":
    uploaded_file = st.file_uploader(
        "Upload a screenshot or image",
        type=["png", "jpg", "jpeg", "webp", "bmp"],
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        from utils.ocr import extract_text_from_image

        img_bytes = uploaded_file.read()

        with st.spinner("🖼️ Running OCR extraction..."):
            ocr_result = extract_text_from_image(img_bytes)

        if ocr_result["success"] and ocr_result["text"].strip():
            claim_text = ocr_result["text"]
            st.success(
                f"✅ OCR extracted {ocr_result['word_count']} words from {ocr_result['image_width']}×{ocr_result['image_height']}px image")
            with st.expander("View extracted text"):
                st.code(claim_text, language=None)
        else:
            if ocr_result["error"]:
                st.error(f"OCR Error: {ocr_result['error']}")
            else:
                st.warning("No text extracted. Try a clearer image.")
                claim_text = ""

analyze_btn = st.button("🔬 Analyze Claim", use_container_width=True, type="primary")
st.markdown('</div>', unsafe_allow_html=True)

if analyze_btn and claim_text.strip():

    if show_pipeline:
        st.markdown("### ⚡ Processing Pipeline")
        pipeline_placeholder = st.empty()

    from utils.detectors import detect_clickbait, detect_manipulation, detect_credibility, analyze_text_metrics
    from utils.similarity import find_similar_evidence
    from utils.scoring import compute_trust_score, get_verdict

    if show_pipeline:
        with pipeline_placeholder.container():
            render_pipeline(active_step=0)
    time.sleep(0.3)

    if show_pipeline:
        with pipeline_placeholder.container():
            render_pipeline(active_step=1)
    time.sleep(0.25)

    if show_pipeline:
        with pipeline_placeholder.container():
            render_pipeline(active_step=2)

    with st.spinner("🧠 Running semantic analysis..."):
        sim_results = find_similar_evidence(claim_text, top_k=top_k, evidence_path=str(EVIDENCE_PATH))

    if show_pipeline:
        with pipeline_placeholder.container():
            render_pipeline(active_step=3)
    time.sleep(0.2)

    clickbait = detect_clickbait(claim_text)
    manipulation = detect_manipulation(claim_text)
    credibility = detect_credibility(claim_text)
    text_metrics = analyze_text_metrics(claim_text)

    if show_pipeline:
        with pipeline_placeholder.container():
            render_pipeline(active_step=4)
    time.sleep(0.2)

    score_data = compute_trust_score(
        similarity_score=sim_results["top_similarity"],
        source_reliability=sim_results["source_reliability"],
        clickbait_penalty=clickbait["penalty"],
        manipulation_penalty=manipulation["penalty"],
        credibility_bonus=credibility["bonus"],
    )
    trust_score = score_data["trust_score"]
    verdict = get_verdict(trust_score)

    claim_hash = hashlib.sha256(
        claim_text.encode()
    ).hexdigest()

    tx_record = {
        "claim_hash": claim_hash,
        "trust_score": round(trust_score, 2),
        "verdict": verdict["verdict"],
        "timestamp": time.time()
    }

    st.session_state.blockchain_records.append(tx_record)

    st.success(
        f"⛓ Claim fingerprint stored: {claim_hash[:16]}..."
    )

    if show_pipeline:
        with pipeline_placeholder.container():
            render_pipeline(active_step=5)
    time.sleep(0.2)

    # Step 7: Report
    if show_pipeline:
        with pipeline_placeholder.container():
            render_pipeline(done=True)
    time.sleep(0.15)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 📊 Analysis Dashboard")
    st.markdown("---")

    # ROW 1: Verdict card + main gauge + bar meters
    col_verdict, col_main_gauge, col_meters = st.columns([2, 2, 3])

    with col_verdict:
        vc = verdict
        st.markdown(f"""
        <div style="background:{vc['bg_color']}; border:1.5px solid {vc['color']}40;
                    border-radius:16px; padding:24px; text-align:center; height:100%;">
            <div style="font-size:3rem; margin-bottom:6px;">{vc['icon']}</div>
            <div style="font-family:'Syne',sans-serif; font-weight:800; font-size:1.7rem;
                        color:{vc['color']}; letter-spacing:-0.02em;">
                {vc['verdict']}
            </div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem;
                        color:{vc['color']}80; text-transform:uppercase; letter-spacing:0.12em;
                        margin-top:4px;">
                Confidence: {vc['confidence']}
            </div>
            <div style="margin-top:16px; font-size:0.82rem; color:#90a4ae; line-height:1.55;">
                {vc['explanation'][:220]}...
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_main_gauge:
        color_map = {
            "VERIFIED": "#00e676",
            "LIKELY TRUE": "#ffd740",
            "UNCERTAIN": "#ff9800",
            "LIKELY FALSE": "#ff1744",
        }
        gauge_color = color_map.get(verdict["verdict"], "#00e5ff")
        fig_trust = make_gauge(trust_score, "Trust Score", color=gauge_color)
        st.plotly_chart(fig_trust, use_container_width=True)

        # Similarity gauge
        sim_pct = sim_results["top_similarity"] * 100
        fig_sim = make_gauge(sim_pct, "Semantic Similarity", color="#7c4dff")
        st.plotly_chart(fig_sim, use_container_width=True)

    with col_meters:
        st.markdown("#### Signal Meters")

        meters = [
            ("Clickbait Risk", clickbait["score"], 100, "#ff1744"),
            ("Manipulation", manipulation["score"], 100, "#ff9800"),
            ("Credibility Score", credibility["score"], 100, "#00e676"),
            ("Source Reliability", sim_results["source_reliability"], 100, "#00e5ff"),
        ]
        for label, val, max_v, color in meters:
            col_label, col_bar = st.columns([2, 5])
            with col_label:
                st.markdown(
                    f'<div style="font-size:0.78rem; color:#78909c; padding-top:12px;">{label}</div>',
                    unsafe_allow_html=True
                )
            with col_bar:
                pct = val / max_v
                bar_color = color
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05); border-radius:99px;
                            height:10px; margin-top:16px; overflow:hidden;">
                    <div style="width:{pct * 100:.1f}%; height:100%; background:{bar_color};
                                border-radius:99px; transition:width 0.4s ease;"></div>
                </div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.75rem;
                            color:{bar_color}; text-align:right; margin-top:2px;">
                    {val:.1f}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if show_breakdown:
        col_breakdown, col_analytics = st.columns([3, 2])

        with col_breakdown:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Score Breakdown")

            components = [
                ("Base Score", "+40.0", "#78909c"),
                ("Semantic Similarity", f'+{score_data["sim_component"]:.2f}', "#7c4dff"),
                ("Source Reliability", f'+{score_data["reliability_component"]:.2f}', "#00e5ff"),
                ("Credibility Bonus", f'+{score_data["credibility_bonus"]:.2f}', "#00e676"),
                ("Clickbait Penalty", f'-{score_data["clickbait_penalty"]:.2f}', "#ff9800"),
                ("Manipulation Penalty", f'-{score_data["manipulation_penalty"]:.2f}', "#ff1744"),
            ]
            for comp, val, color in components:
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center;
                            padding:7px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
                    <span style="font-size:0.85rem; color:#90a4ae;">{comp}</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-size:0.88rem;
                                 color:{color}; font-weight:600;">{val}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                        padding:10px 0; margin-top:4px;">
                <span style="font-size:0.95rem; font-weight:700; color:#e0e6f0;">FINAL SCORE</span>
                <span style="font-family:'JetBrains Mono',monospace; font-size:1.1rem;
                             color:{gauge_color}; font-weight:700;">{trust_score:.1f} / 100</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_analytics:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📈 Text Analytics")
            analytics_items = [
                ("Claim Length", f'{text_metrics["char_count"]} chars'),
                ("Word Count", str(text_metrics["word_count"])),
                ("Sentence Count", str(text_metrics["sentence_count"])),
                ("Clickbait Terms", str(clickbait["count"])),
                ("Manipulation Terms", str(manipulation["count"])),
                ("Credibility Terms", str(credibility["count"])),
                ("Evidence Matches", str(len(sim_results["matches"]))),
                ("Exclamation Marks", str(text_metrics["exclamation_count"])),
                ("CAPS Ratio", f'{text_metrics["caps_ratio"] * 100:.1f}%'),
            ]
            for label, val in analytics_items:
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between;
                            padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.04);">
                    <span style="font-size:0.8rem; color:#78909c;">{label}</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-size:0.82rem;
                                 color:#b0bec5;">{val}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🔍 Detected Signal Terms")
    col_c, col_m, col_cr = st.columns(3)
    with col_c:
        st.markdown(
            f'<div class="glass-card"><b style="color:#ff6090">🚨 Clickbait Terms ({clickbait["count"]})</b><br>',
            unsafe_allow_html=True)
        if clickbait["terms_found"]:
            for t in clickbait["terms_found"]:
                st.markdown(f'<span class="term-badge badge-red">{t}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:#546e7a; font-size:0.82rem;">None detected</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_m:
        st.markdown(
            f'<div class="glass-card"><b style="color:#ffb74d">⚠️ Manipulation Terms ({manipulation["count"]})</b><br>',
            unsafe_allow_html=True)
        if manipulation["terms_found"]:
            for t in manipulation["terms_found"]:
                st.markdown(f'<span class="term-badge badge-amber">{t}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:#546e7a; font-size:0.82rem;">None detected</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_cr:
        st.markdown(
            f'<div class="glass-card"><b style="color:#69f0ae">✅ Credibility Terms ({credibility["count"]})</b><br>',
            unsafe_allow_html=True)
        if credibility["terms_found"]:
            for t in credibility["terms_found"]:
                st.markdown(f'<span class="term-badge badge-green">{t}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:#546e7a; font-size:0.82rem;">None detected</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🗂️ Top Matching Evidence")

    label_colors = {
        "TRUE": ("#00e676", "badge-green"),
        "FALSE": ("#ff6090", "badge-red"),
        "UNCERTAIN": ("#ffb74d", "badge-amber"),
    }

    for i, match in enumerate(sim_results["matches"]):
        lc, lbadge = label_colors.get(match["label"], ("#80d8ff", "badge-blue"))
        cat_icon = CATEGORY_ICONS.get(match["category"], "📌")
        sim_pct = match["similarity"] * 100

        st.markdown(f"""
        <div class="evidence-row">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                <span style="font-family:'JetBrains Mono',monospace; font-size:0.75rem;
                             color:#546e7a;">#{i + 1}</span>
                <span class="term-badge {lbadge}">{match['label']}</span>
                <span class="term-badge badge-blue">{cat_icon} {match['category']}</span>
                <span style="margin-left:auto; font-family:'JetBrains Mono',monospace;
                             font-size:0.78rem; color:#00e5ff;">
                    Similarity: {sim_pct:.1f}%
                </span>
            </div>
            <div style="font-size:0.82rem; color:#78909c; margin-bottom:6px;">
                <strong style="color:#90a4ae">Matched Claim:</strong> {match['claim'][:120]}
            </div>
            <div style="font-size:0.84rem; color:#b0bec5; line-height:1.5;">
                <strong style="color:#90a4ae">Evidence:</strong> {match['evidence'][:300]}
            </div>
            <div style="margin-top:8px; background:rgba(255,255,255,0.04);
                        border-radius:6px; height:5px; overflow:hidden;">
                <div style="width:{sim_pct:.1f}%; height:100%;
                            background:linear-gradient(90deg,#00b8d4,#7c4dff);
                            border-radius:6px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📋 AI Report")
    st.markdown(f"""
    <div style="background:{verdict['bg_color']}; border:1px solid {verdict['color']}30;
                border-radius:16px; padding:24px;">
        <div style="font-family:'Syne',sans-serif; font-weight:700; font-size:1.1rem;
                    color:{verdict['color']}; margin-bottom:12px;">
            {verdict['icon']} Verdict: {verdict['verdict']}
        </div>
        <div style="font-size:0.9rem; color:#b0bec5; line-height:1.65;">
            {verdict['explanation']}
        </div>
        <div style="margin-top:16px; padding-top:16px; border-top:1px solid rgba(255,255,255,0.07);
                    display:flex; gap:20px; flex-wrap:wrap;">
            <div>
                <span style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em; color:#546e7a;">Trust Score</span>
                <div style="font-family:'JetBrains Mono',monospace; font-size:1.4rem;
                            color:{verdict['color']}; font-weight:700;">{trust_score:.1f}</div>
            </div>
            <div>
                <span style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em; color:#546e7a;">Confidence</span>
                <div style="font-family:'JetBrains Mono',monospace; font-size:1.4rem;
                            color:{verdict['color']}; font-weight:700;">{verdict['confidence']}</div>
            </div>
            <div>
                <span style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em; color:#546e7a;">Top Similarity</span>
                <div style="font-family:'JetBrains Mono',monospace; font-size:1.4rem;
                            color:#7c4dff; font-weight:700;">{sim_results['top_similarity']:.3f}</div>
            </div>
            <div>
                <span style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em; color:#546e7a;">Evidence Count</span>
                <div style="font-family:'JetBrains Mono',monospace; font-size:1.4rem;
                            color:#00e5ff; font-weight:700;">{len(sim_results['matches'])}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📥 Export Report")

    from utils.report_generator import generate_pdf_report

    score_export = {
        "top_similarity": sim_results["top_similarity"],
        "sim_component": score_data["sim_component"],
        "reliability_component": score_data["reliability_component"],
        "source_reliability": sim_results["source_reliability"],
        "credibility_bonus": score_data["credibility_bonus"],
        "clickbait_penalty": score_data["clickbait_penalty"],
        "manipulation_penalty": score_data["manipulation_penalty"],
    }

    pdf_bytes = generate_pdf_report(
        claim=claim_text,
        trust_score=trust_score,
        verdict=verdict,
        score_breakdown=score_export,
        clickbait=clickbait,
        manipulation=manipulation,
        credibility=credibility,
        evidence_matches=sim_results["matches"],
        text_metrics=text_metrics,
    )

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        is_pdf = pdf_bytes[:4] == b"%PDF"
        st.download_button(
            label="📄 Download PDF Report" if is_pdf else "📄 Download Text Report",
            data=pdf_bytes,
            file_name=f"claimlens_report_{int(time.time())}.{'pdf' if is_pdf else 'txt'}",
            mime="application/pdf" if is_pdf else "text/plain",
            use_container_width=True,
        )
    with col_dl2:
        # CSV of evidence matches
        matches_df = pd.DataFrame(sim_results["matches"])
        csv_data = matches_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📊 Download Evidence CSV",
            data=csv_data,
            file_name=f"evidence_matches_{int(time.time())}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.success(f"✅ Analysis complete · Trust Score: **{trust_score:.1f}** · Verdict: **{verdict['verdict']}**")

elif analyze_btn:
    st.warning("⚠️ Please enter a claim to analyze.")
st.markdown("## ⛓ Blockchain Explorer")
if st.session_state.blockchain_records:

    blockchain_df = pd.DataFrame(
        st.session_state.blockchain_records
    )

    st.dataframe(
        blockchain_df,
        use_container_width=True
    )

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:16px 0;">
    <span style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#37474f;">
        ClaimLens AI · Hackathon Prototype · Semantic analysis powered by
        <span style="color:#546e7a">SentenceTransformers all-MiniLM-L6-v2</span> ·
        No external AI APIs · Built with Streamlit
    </span>
</div>
""", unsafe_allow_html=True)
