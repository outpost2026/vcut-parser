import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from vcf_parser_v20 import RuidaVcfEngineV20
import os, io, json, hashlib, datetime

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("SYSTEQ // CAM Automation Platform")
    pwd = st.text_input("Přístupové heslo", type="password")
    if st.button("Přistoupit"):
        if pwd == "moodpasta-demo-2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Nesprávné heslo")
    st.stop()

st.set_page_config(
    page_title="SYSTEQ // CAM Automation Platform | v20 B2B",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Skrýt Streamlit nativní header/footer, aby custom header byl vidět */
    header[data-testid="stHeader"] { display: none !important; }
    .stApp { background-color: #0a0e14; color: #F1F5F9; margin-top: 0 !important; padding-top: 0 !important; }
    .main > div { margin-top: 0 !important; padding-top: 0 !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    .stApp > header { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    .stDeployButton { display: none !important; }
    h1, h2, h3, h4 { font-family: 'Inter', -apple-system, sans-serif !important; font-weight: 700 !important; color: #F1F5F9 !important; }

    /* ── HEADER BAR — +20 % (výjimka z +40 %) ── */
    .systeq-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: .8rem 0; border-bottom: 1px solid rgba(255,255,255,.055);
        background: rgba(10,14,20,.94); backdrop-filter: blur(10px);
        position: sticky; top: 0; z-index: 200;
    }
    .sh-logo { font-size: 1.56rem; font-weight: 700; letter-spacing: .12em; display: flex; align-items: center; text-decoration: none; }
    .sh-logo-sys { color: #0d9488; font-weight: 700; }
    .sh-logo-teq { color: #D35400; font-weight: 700; }
    .sh-logo-tag { font-size: 1.02rem; color: #94A3B8; font-weight: 400; letter-spacing: .08em; margin-left: .5rem; padding-left: .5rem; border-left: 1px solid rgba(255,255,255,.1); }
    .sh-nav { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
    .sh-pill { display: flex; align-items: center; gap: .4rem; font-size: .82rem; letter-spacing: .1em; color: #94A3B8; border: 1px solid rgba(255,255,255,.055); padding: .25rem .65rem; border-radius: 4px; }
    .sh-link { color: #94A3B8; text-decoration: none; font-size: .9rem; letter-spacing: .07em; transition: color .2s; display: flex; align-items: center; gap: .3rem; }
    .sh-link:hover { color: #F1F5F9; }
    .sh-link svg { flex-shrink: 0; }

    /* ── KPI SYSTEM ── */
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin: 16px 0; }
    .kpi-card { background: #111827; border: 1px solid #334155; border-radius: 10px; padding: 16px; }
    .kpi-card.t1 { border-left: 3px solid #10B981; }
    .kpi-card.t2 { border-left: 3px solid #F59E0B; }
    .kpi-value { font-size: 36px; font-weight: 800; color: #10B981; }
    .kpi-value-sm { font-size: 31px; font-weight: 800; color: #F59E0B; }
    .kpi-label { font-size: 18px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px; }
    .kpi-sub { font-size: 20px; color: #CBD5E1; margin-top: 2px; }
    .tier-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 17px; font-weight: 700; text-transform: uppercase; }
    .tier-badge.t1 { background: #064E3B; color: #10B981; }
    .tier-badge.t2 { background: #451A03; color: #F59E0B; }

    /* ── ROLE SWITCHER ── */
    .role-switcher { display: flex; gap: 8px; margin: 8px 0; }
    .role-btn {
        flex: 1; padding: 10px 20px; border-radius: 20px; border: 1px solid #334155;
        font-size: 16px; font-weight: 600; cursor: pointer; transition: all .2s;
        text-align: center; background: #111827; color: #94A3B8;
    }
    .role-btn:hover { border-color: #0d9488; color: #F1F5F9; }
    .role-btn.active { background: #0d9488; color: #0F172A; border-color: #0d9488; }

    /* ── RIZIKA ── */
    .riz-ok { background-color: #064E3B; border-left: 4px solid #10B981; border-radius: 6px; padding: 10px; margin-bottom: 12px; }
    .riz-warn { background-color: #1E2030; border-left: 4px solid #F59E0B; border-radius: 6px; padding: 10px; margin-bottom: 12px; }
    .riz-critical { background-color: #1E2030; border-left: 4px solid #F43F5E; border-radius: 6px; padding: 10px; margin-bottom: 12px; }
    .riz-critical h4, .riz-warn h4, .riz-ok h4 { font-size: 22px !important; margin-top: 0 !important; margin-bottom: 4px !important; }
    .riz-critical p, .riz-warn p, .riz-ok p { font-size: 18px !important; color: #CBD5E1 !important; }
    .riz-warn-text, .riz-critical-text { font-size: 18px !important; }

    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { color: #CBD5E1; font-weight: 600; }
    .stTabs [aria-selected="true"] { color: #10B981 !important; }
    .stButton > button { background-color: #0d9488; color: #0F172A; font-weight: 700; border: none; border-radius: 8px; }
    .stButton > button:hover { background-color: #0f9f92; }

    /* ── HASH BOX ── */
    .hash-box { background: #0F172A; border: 1px solid #334155; border-radius: 6px; padding: 6px 10px; font-family: monospace; font-size: 17px; color: #CBD5E1; word-break: break-all; }

    /* ── DOWNLOAD ── */
    .section-header { font-size: 20px; font-weight: 600; color: #CBD5E1; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.04em; }
    .download-section { margin-top: 16px; padding: 10px; background: #111827; border-radius: 8px; border: 1px solid #334155; }
    div[data-testid="stDownloadButton"] button {
        font-size: 18px !important; padding: 3px 14px !important; min-height: 36px !important;
    }
    div[data-testid="stDownloadButton"] button p { font-size: 18px !important; }

    /* ── HERO BLOCK (HUD Level 0) ── */
    .hero-block {
        background: linear-gradient(135deg, #111827 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 16px 0;
    }
    .hero-main {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        flex-wrap: wrap;
    }
    .hero-time-group {
        display: flex;
        align-items: center;
        gap: 24px;
    }
    .hero-time-main {
        display: flex;
        flex-direction: column;
    }
    .hero-time {
        font-size: 67px;
        font-weight: 800;
        color: #0d9488;
        line-height: 1;
        letter-spacing: -0.02em;
    }
    .hero-time-label {
        font-size: 18px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 6px;
    }
    .hero-time-side {
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding-left: 24px;
        border-left: 1px solid rgba(255,255,255,0.08);
    }
    .hero-time-side-item {
        font-size: 18px;
        color: #94A3B8;
        line-height: 1.4;
    }
    .hero-time-side-item span { color: #CBD5E1; font-weight: 600; }
    .hero-time-side-label { font-size: 12px; color: #64748b; }
    .hero-status-group {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }
    .hero-status-badge {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 17px;
        font-weight: 600;
        white-space: nowrap;
    }
    .hero-status-badge.ok {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .hero-status-badge.warn {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .hero-status-badge.critical {
        background: rgba(244, 63, 94, 0.15);
        color: #F43F5E;
        border: 1px solid rgba(244, 63, 94, 0.3);
    }
    .hero-stats {
        display: flex;
        gap: 28px;
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px solid rgba(255,255,255,0.06);
        flex-wrap: wrap;
    }
    .hero-stat {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .hero-stat-value {
        font-size: 25px;
        font-weight: 700;
        color: #F1F5F9;
    }
    .hero-stat-label {
        font-size: 17px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .hero-stat-sub {
        font-size: 13px;
        color: #64748b;
    }

    /* ── HUD → MFD SEPARATOR ── */
    .hud-separator {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
        margin: 24px 0;
    }

    .yield-bar { height: 8px; background: #334155; border-radius: 4px; overflow: hidden; margin: 8px 0; }
    .yield-fill { height: 100%; background: linear-gradient(90deg, #10B981, #3B82F6); border-radius: 4px; }

    /* ── FOOTER — +20 % (výjimka z +40 %) ── */
    .systeq-footer {
        display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: .75rem;
        border-top: 1px solid rgba(255,255,255,.08); padding: 1.4rem 0; margin-top: 2rem;
    }
    .sf-logo { font-size: 1.26rem; font-weight: 700; letter-spacing: .12em; color: #CBD5E1; }
    .sf-logo .sf-sys { color: #0d9488; font-weight: 700; }
    .sf-logo .sf-teq { color: #D35400; font-weight: 700; }
    .sf-meta { font-size: 1.02rem; color: #94A3B8; letter-spacing: .04em; }
    .sf-motto { font-size: 1.06rem; color: #94A3B8; font-style: italic; font-weight: 300; letter-spacing: .06em; }
    .sf-contact { font-size: 1.02rem; color: #94A3B8; letter-spacing: .04em; }
    .sf-contact a { color: #CBD5E1; text-decoration: none; }
    .sf-contact a:hover { color: #0d9488; }
</style>
""", unsafe_allow_html=True)

# ── SYSTEQ HEADER — bez blink pill, doraženo k okraji ──
st.markdown(f"""
<div class="systeq-header">
  <div class="sh-logo">
    <span class="sh-logo-sys">SYS</span><span class="sh-logo-teq">TEQ</span><span class="sh-logo-tag">CAM Automation</span>
  </div>
  <nav class="sh-nav">
    <div class="sh-pill">API ONLINE</div>
    <a class="sh-link hide-m" href="https://github.com/outpost2026" target="_blank" rel="noopener">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
      <span>GitHub</span>
    </a>
    <a class="sh-link hide-m" href="https://www.linkedin.com/in/ond%C5%99ej-sou%C5%A1ek-ba8490414/" target="_blank" rel="noopener">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
      <span>LinkedIn</span>
    </a>
    <a class="sh-link" href="tel:+420735045256">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.44 2 2 0 0 1 3.58 1h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.56a16 16 0 0 0 6 6l.92-.92a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
      +420 735 045 256
    </a>
  </nav>
</div>
""", unsafe_allow_html=True)

# ── HEADLINE ──
st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>CAM Automation Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 18px; margin-bottom: 10px;'>Deterministický parser CNC formátů. VCF → DXF → ERP/AI</p>", unsafe_allow_html=True)

if "role" not in st.session_state:
    st.session_state.role = "Dílna / CNC"

col_r1, col_r2 = st.columns(2)
with col_r1:
    if st.button("Dílna / CNC", key="role_cnc", use_container_width=True,
                 type="primary" if st.session_state.role == "Dílna / CNC" else "secondary"):
        st.session_state.role = "Dílna / CNC"
with col_r2:
    if st.button("Obchodní", key="role_obchod", use_container_width=True,
                 type="primary" if st.session_state.role == "Obchodní" else "secondary"):
        st.session_state.role = "Obchodní"

ROLE_SELECT = st.session_state.role
st.markdown("<style>.stButton button[data-testid='baseButton-secondary'] { border-radius: 20px !important; } .stButton button[data-testid='baseButton-primary'] { border-radius: 20px !important; }</style>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Nahrajte výrobní soubor .VCF", type=["vcf"], label_visibility="collapsed")

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_hash = hashlib.md5(file_bytes).hexdigest()
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    with st.spinner("Provádím nízkoúrovňový sémantický audit..."):
        try:
            engine = RuidaVcfEngineV20(file_bytes, filename=uploaded_file.name)
            item = engine.parsed_data

            time_formatted = item["erp_time_prediction"]["predicted_time_formatted"]
            total_length_m = item["erp_time_prediction"]["total_path_length_mm"] / 1000.0
            width = item.get("canvas_width_mm", 0.0)
            height = item.get("canvas_height_mm", 0.0)
            thickness = item.get("material_thickness_mm", 12.0)
            complexity = item.get("complexity_index", "Standardní")
            panel_format = item.get("detected_panel_format_name", "Atypický")
            mi = item.get("manufacturing_intelligence", {
                "enabled": False, "semantic_warnings": [],
                "risk_score": 0.0, "material_thickness_confidence": "LOW"
            })
            risk_score = mi.get("risk_score", 0.0)
            warnings_list = mi.get("semantic_warnings", [])
            criticals = [w for w in warnings_list if w.get("severity") == "CRITICAL"]
            warnings_w = [w for w in warnings_list if w.get("severity") == "WARNING"]
            warnings_i = [w for w in warnings_list if w.get("severity") == "INFO"]

            is_aggregated = item.get("is_aggregated_job", False)
            sub_jobs_count = len(item.get("sub_jobs", []))
            area_m2 = (width * height) / 1000000.0
            cas_min = item["erp_time_prediction"]["predicted_time_seconds"] / 60.0
            layers = item.get("layers", [])
            elements_all = item.get("elements", [])
            magic = item.get("magic", "N/A")
            engine_ver = getattr(engine, 'VERSION', 'v20')

            # ── 2D Vizualizace ──
            png_bytes = None
            fig_viz = None
            if elements_all:
                fig_viz, ax = plt.subplots(figsize=(19.2, 10.8), facecolor="#1E293B")
                ax.set_facecolor("#0F172A")
                color_map = {1: "#F43F5E", 5: "#F43F5E", 4: "#3B82F6", 3: "#10B981"}
                operation_map = {1: "Řez (Cut)", 5: "Řez (Cut)", 4: "Rytí (Engrave)", 3: "Skórování (Score)"}
                seen_ops = set()
                for el in elements_all[:600]:
                    vertices = el.get("vertices", [])
                    if vertices:
                        xs = [v[0] for v in vertices]
                        ys = [v[1] for v in vertices]
                        gid = el.get("geom_type_id", 1)
                        col = color_map.get(gid, "#64748B")
                        ax.plot(xs, ys, color=col, linewidth=0.9, alpha=0.85)
                        seen_ops.add(gid)
                for idx, layer in enumerate(layers):
                    zy_min = layer.get("travel_safety_height_mm", 0)
                    zy_max = layer.get("end_height_h2_mm", 0)
                    if zy_min and zy_max:
                        ax.axhline(y=idx * 50 + 10, color="#F59E0B", linewidth=0.6, linestyle=":", alpha=0.4)
                legend_patches = []
                for gid in sorted(seen_ops):
                    col = color_map.get(gid, "#64748B")
                    label = operation_map.get(gid, f"Type {gid}")
                    legend_patches.append(mlines.Line2D([0], [0], color=col, linewidth=2, label=label))
                if legend_patches:
                    ax.legend(handles=legend_patches, loc="upper right", fontsize=8,
                             facecolor="#1E293B", edgecolor="#334155", labelcolor="#F8FAFC")
                ax.set_title(f"2D Vizualizace: {uploaded_file.name}", color="#F8FAFC", fontsize=12)
                ax.tick_params(colors="#94A3B8")
                for spine in ax.spines.values():
                    spine.set_color("#334155")
                ax.set_aspect('equal', 'box')
                ax.set_xlabel("X (mm)", color="#94A3B8")
                ax.set_ylabel("Y (mm)", color="#94A3B8")
                fig_viz.tight_layout()
                buf = io.BytesIO()
                fig_viz.savefig(buf, format='png', dpi=100, facecolor="#1E293B")
                png_bytes = buf.getvalue()
            else:
                fig_viz = None

            # ── LLM PROMPT (definice před použitím) ──
            lc_lines = []
            for idx, layer in enumerate(layers):
                lc_lines.append(f"  - Vrstva {idx+1}: {layer.get('cutter_type','?')} | operace={layer.get('operation_type','?')} | speed={layer.get('speed_mms',0)} mm/s | H1={layer.get('travel_safety_height_mm',0)} mm | H2={layer.get('end_height_h2_mm',0)} mm | délka={layer.get('total_cut_length_mm',0):.0f} mm")
            layer_card_str = "\n".join(lc_lines) if lc_lines else "  (žádné vrstvy)"

            warning_summary = "\n".join(f"  - [{w['severity']}] {w['message']}" for w in warnings_list[:15]) if warnings_list else "  (žádné anomálie)"
            seq_ok = item["operation_sequence"]["sequence_is_correct"]

            llm_prompt = f"""# SEMANTIC EMBEDDING — VCF Deterministic Data Audit

## SOURCE
- File: {uploaded_file.name}
- MD5: {file_hash}
- Timestamp: {timestamp}
- Parser Version: {engine_ver}
- Magic: {magic}

## 1. PROSTOROVÝ LAYOUT
- Canvas: {width:.0f} × {height:.0f} mm
- Canvas Area: {area_m2:.3f} m²
- Element Count: {len(elements_all)}
- Layer Count: {len(layers)}
- Panel Format: {panel_format}
- Complexity: {complexity}
- Is Aggregated Job: {is_aggregated}
- Sub-jobs: {sub_jobs_count}

## 2. ČASOVÁ PREDIkCE
- Predicted Time: {time_formatted} ({cas_min:.1f} min)
- Total Path Length: {total_length_m:.2f} m
- Material Thickness: {thickness:.0f} mm (confidence: {mi.get('material_thickness_confidence','LOW')})

## 3. VRSTVY — Layer Card
{layer_card_str}

## 4. SÉMANTICKÝ AUDIT
- Risk Score: {risk_score:.2f}
- Sequence Correct: {seq_ok}
- Critical Issues: {len(criticals)}
- Warnings: {len(warnings_w)}
- Details:
{warning_summary}

## 5. OPERATION SEQUENCE
- Correct Order: {seq_ok}
"""

            # ═══════════════════════════════════════════════════════════
            # HUD (Level 0) — Head-Up Display, <2s scanning
            # ═══════════════════════════════════════════════════════════

            # ── Active layer/element filtering ──
            active_layers = [l for l in layers if l.get("is_output_yes", True)]
            inactive_count = len(layers) - len(active_layers)
            layer_count_display = f"{len(active_layers)}/{len(layers)}" if inactive_count > 0 else str(len(layers))
            active_elements = [el for el in elements_all if el.get("is_output_yes", True)]
            active_vslot = [l for l in active_layers if l.get("cutter_type") == "V-slot"]
            max_vslot_depth = max((l.get("end_height_h2_mm", 0) for l in active_vslot), default=0)
            vslot_layers = len(active_vslot)
            sub_label = f"{sub_jobs_count} panelů" if is_aggregated and sub_jobs_count > 0 else "1 panel"

            # ── HERO BLOCK: dominantní cut time + compact stats + status badge ──
            if criticals:
                status_class = "critical"
                status_text = "CRITICAL"
                risk_display = f"Risk: {risk_score:.2f}"
            elif warnings_w:
                status_class = "warn"
                status_text = "WARNING"
                risk_display = f"Risk: {risk_score:.2f}"
            else:
                status_class = "ok"
                status_text = "✓ OK"
                risk_display = "Risk: 0.00"

            st.markdown(f"""
<div class="hero-block">
  <div class="hero-main">
    <div class="hero-time-group">
      <div class="hero-time-main">
        <div class="hero-time">{time_formatted}</div>
        <div class="hero-time-label">Predikce času řezu · ±2–5 %</div>
      </div>
      <div class="hero-time-side">
        <div class="hero-time-side-item">Elementy: <span>{len(active_elements)}</span></div>
        <div class="hero-time-side-item">Panelů: <span>{sub_label}</span></div>
      </div>
    </div>
    <div class="hero-status-group">
      <div class="hero-status-badge {status_class}">{status_text}</div>
      <div class="hero-status-badge {status_class}" style="font-weight:400;">{risk_display}</div>
    </div>
  </div>
  <div class="hero-stats">
    <div class="hero-stat">
      <div class="hero-stat-value">{total_length_m:.1f} m</div>
      <div class="hero-stat-label">Dráha</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-value">{width:.0f}×{height:.0f}</div>
      <div class="hero-stat-label">Rozměry (mm)</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-value">{layer_count_display}</div>
      <div class="hero-stat-label">Vrstvy</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-value">{area_m2:.3f} m²</div>
      <div class="hero-stat-label">Plocha</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-value">{thickness:.0f} mm</div>
      <div class="hero-stat-label">Tloušťka</div>
      <div class="hero-stat-sub">conf: {mi.get('material_thickness_confidence', 'LOW')}</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-value">{max_vslot_depth:.0f} mm</div>
      <div class="hero-stat-label">V-slot hloubka</div>
      <div class="hero-stat-sub">{'aktivních {}'.format(vslot_layers) if vslot_layers > 1 else 'řez do materiálu'}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

            # ── 2D VIZUALIZACE (Level 0 — immediately below hero, universal across all roles) ──
            if fig_viz:
                st.markdown("#### 2D Digitální model drah")
                st.image(png_bytes, caption=f"{uploaded_file.name} — 1920×1080", use_column_width=True)
            else:
                st.warning("Žádná geometrie k vizualizaci.")

            # ── RIZIKA (pouze CNC; conditional — only when risk exists) ──
            if ROLE_SELECT == "Dílna / CNC" and (risk_score > 0 or criticals or warnings_w):
                st.markdown("### Rizika")
                if criticals:
                    st.markdown(f"""<div class="riz-critical"><h4 style="color: #F43F5E !important;">Kritická rizika (Index: {risk_score:.2f})</h4><p>Nalezené anomálie vyžadují zásah operátora.</p></div>""", unsafe_allow_html=True)
                    st.error(f"**[CRITICAL]** {criticals[0]['message']}", icon=None)
                    if len(criticals) > 1:
                        with st.expander(f"Dalších {len(criticals) - 1}"):
                            for w in criticals[1:]:
                                st.error(f"**[CRITICAL]** {w['message']}", icon=None)
                    if warnings_w:
                        with st.expander(f"{len(warnings_w)} WARNING"):
                            for w in warnings_w:
                                st.warning(f"**[WARNING]** {w['message']}", icon=None)
                elif warnings_w:
                    st.markdown(f"""<div class="riz-warn"><h4 style="color: #F59E0B !important;">Varování (Index: {risk_score:.2f})</h4></div>""", unsafe_allow_html=True)
                    st.warning(f"**[WARNING]** {warnings_w[0]['message']}", icon=None)
                    if len(warnings_w) > 1:
                        with st.expander(f"Dalších {len(warnings_w) - 1}"):
                            for w in warnings_w[1:]:
                                st.warning(f"**[WARNING]** {w['message']}", icon=None)

            # ═══════════════════════════════════════════════════════════
            # HUD → MFD SEPARATOR
            # ═══════════════════════════════════════════════════════════
            st.markdown("<div class='hud-separator'></div>", unsafe_allow_html=True)

            # ═══════════════════════════════════════════════════════════
            # MFD (Multi-Function Display) — expandery na vyžádání
            # ═══════════════════════════════════════════════════════════

            # ── TIER 2 KPI (v expanderu, mimo Level 0) ──
            with st.expander("TIER 2 — Sekundární parametry", expanded=False):
                conf_color = "#10B981" if mi.get("material_thickness_confidence") == "HIGH" else "#F59E0B"
                sub_label = f"{sub_jobs_count} panelů" if is_aggregated and sub_jobs_count > 0 else "1 panel"
                st.markdown(f"""
<div class='kpi-grid'>
  <div class='kpi-card t2'>
    <div class='kpi-value-sm'>{complexity}</div>
    <div class='kpi-label'>Složitost <span class='tier-badge t2'>T2</span></div>
    <div class='kpi-sub'>Complexity index</div>
  </div>
  <div class='kpi-card t2'>
    <div class='kpi-value-sm' style='color:{conf_color};'>{thickness:.0f} mm</div>
    <div class='kpi-label'>Odhad. tloušťka <span class='tier-badge t2'>T2</span></div>
    <div class='kpi-sub'>Confidence: {mi.get('material_thickness_confidence', 'LOW')}</div>
  </div>
  <div class='kpi-card t2'>
    <div class='kpi-value-sm'>{risk_score:.2f}</div>
    <div class='kpi-label'>Risk Score <span class='tier-badge t2'>T2</span></div>
    <div class='kpi-sub'>Sémantické riziko řezu</div>
  </div>
  <div class='kpi-card t2'>
    <div class='kpi-value-sm'>{sub_label}</div>
    <div class='kpi-label'>Sub-zakázky <span class='tier-badge t2'>T2</span></div>
    <div class='kpi-sub'>Agregovaná dávka</div>
  </div>
  <div class='kpi-card t2'>
    <div class='kpi-value-sm'>{panel_format}</div>
    <div class='kpi-label'>Panel formát <span class='tier-badge t2'>T2</span></div>
    <div class='kpi-sub'>Detekovaný standard</div>
  </div>
</div>
""", unsafe_allow_html=True)

            # ── LAYER CARD (pouze CNC) ──
            if ROLE_SELECT == "Dílna / CNC":
                with st.expander("Layer Card — Nástroje per vrstva", expanded=False):
                    lc_rows = []
                    for idx, layer in enumerate(active_layers):
                        ct = layer.get("cutter_type", "?")
                        ops = layer.get("operation_type", "?")
                        spd = layer.get("speed_mms", 0)
                        h1 = layer.get("travel_safety_height_mm", 0)
                        h2 = layer.get("end_height_h2_mm", 0)
                        llen = layer.get("total_cut_length_mm", 0)
                        sext = layer.get("starting_extension_mm", 0.0)
                        eext = layer.get("ending_extension_mm", 0.0)
                        lc_rows.append({
                            "Vrstva": idx + 1,
                            "Nástroj": ct,
                            "Operace": ops,
                            "Rychlost (mm/s)": spd,
                            "H1 (mm)": h1,
                            "H2 (mm)": h2,
                            "Start Ext (mm)": sext,
                            "End Ext (mm)": eext,
                            "Délka (mm)": round(llen, 1)
                        })
                    st.dataframe(pd.DataFrame(lc_rows), use_container_width=True, hide_index=True)

            # ── METADATA (v expanderu) ──
            with st.expander("Metadata & integrita", expanded=False):
                col_m1, col_m2, col_m3 = st.columns([1, 1, 2])
                with col_m1:
                    st.markdown(f"**Parser:** `{engine_ver}`")
                    st.markdown(f"**Magic:** `{magic}`")
                with col_m2:
                    st.markdown(f"**Timestamp:** `{timestamp}`")
                    st.markdown(f"**Soubor:** `{uploaded_file.name}`")
                with col_m3:
                    st.markdown(f"<div class='hash-box'><b>MD5:</b> {file_hash}</div>", unsafe_allow_html=True)

            # ═══════════════════════════════════════════════════════════
            # ROLE-SPECIFIC SECTIONS (2D viz removed — now at Level 0 for all)
            # ═══════════════════════════════════════════════════════════
            if ROLE_SELECT == "Dílna / CNC":
                st.markdown("#### Kontrola před řezem")
                seq = item["operation_sequence"]
                if seq["sequence_is_correct"]:
                    st.success("**Pořadí vrstev v pořádku.** Obvodový ořez je na konci.")
                else:
                    st.error("**CHYBA SEKVENCE!** Ořez probíhá před dekorativními operacemi.")
                if area_m2 < 1.67:
                    st.warning(f"**Malá plocha ({area_m2:.2f} m²):** Nutno olepit okraje páskou.")
                else:
                    st.success(f"**Standardní plocha ({area_m2:.2f} m²):** Přítlak stačí.")
                if is_aggregated and item.get("sub_jobs"):
                    st.markdown("---")
                    st.markdown("**Sub-zakázky:**")
                    sj_df = pd.DataFrame(item["sub_jobs"])[["sub_job_id", "width_mm", "height_mm", "total_length_mm"]]
                    st.dataframe(sj_df, use_container_width=True, hide_index=True)
                st.markdown("---")
                st.markdown("**Výrobní instrukce:**")
                st.info(f"Složitost: {complexity}")
                st.info(f"Panel: {panel_format}")
                if criticals:
                    st.error("**ZÁSADNÍ RIZIKO!** Před řezem konzultuj s technologem.")

            elif ROLE_SELECT == "Obchodní":
                st.markdown("#### Kalkulátor Nákladů & Marže na zakázku")
                col_cost1, col_cost2, col_cost3 = st.columns(3)
                strojni_minuta_kc = 18.5
                cena_material_m2 = 420.0
                naklady_stroj = cas_min * strojni_minuta_kc
                naklady_material = area_m2 * cena_material_m2
                celkove_naklady = naklady_stroj + naklady_material

                with col_cost1:
                    st.metric("Náklady na strojní čas", f"{naklady_stroj:,.0f} Kč", help=f"{cas_min:.1f} min × {strojni_minuta_kc} Kč/min")
                with col_cost2:
                    st.metric("Náklady na materiál", f"{naklady_material:,.0f} Kč", help=f"{area_m2:.3f} m² × {cena_material_m2} Kč/m²")
                with col_cost3:
                    st.metric("Celkové náklady", f"{celkove_naklady:,.0f} Kč")

                marze = st.slider("Požadovaná marže (%)", min_value=20, max_value=80, value=45, step=5)
                prodejni_cena = celkove_naklady * (1 + marze / 100)
                zisk = prodejni_cena - celkove_naklady

                st.markdown(f"""<div class="kpi-card t2" style="margin-top: 20px; border-left: 3px solid #F59E0B;"><div class="kpi-label" style="color: #F59E0B;">Doporučená prodejní cena ({marze}% marže)</div><div class="kpi-value-sm" style="color: #F59E0B; font-size: 52px;">{prodejni_cena:,.0f} Kč</div><div style="color: #CBD5E1; font-size: 20px;">Zisk: {zisk:,.0f} Kč</div></div>""", unsafe_allow_html=True)

                st.markdown("#### Odoo ERP Import")
                odoo_data = {
                    "Produkt": [f"Echoblock {thickness}mm"],
                    "Množství": [1],
                    "Jednotková cena": [round(prodejni_cena, 2)],
                    "Strojní čas (min)": [round(cas_min, 1)],
                    "Kód produktu": [uploaded_file.name.split(".")[0]],
                    "Plocha (m²)": [round(area_m2, 3)],
                    "Celková délka řezu (m)": [round(total_length_m, 2)]
                }
                df_odoo = pd.DataFrame(odoo_data)
                st.dataframe(df_odoo, use_container_width=True, hide_index=True)
                csv = df_odoo.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Stáhnout Odoo CSV import",
                    data=csv,
                    file_name=f"odoo_import_{uploaded_file.name.split('.')[0]}.csv",
                    mime="text/csv"
                )

            # ═══════════════════════════════════════════════════════════
            # LLM PROMPT GENERATOR (náhled v expanderu)
            # ═══════════════════════════════════════════════════════════
            st.markdown("---")
            st.markdown("<p class='section-header'>LLM Prompt — strukturovaná data pro AI</p>", unsafe_allow_html=True)
            with st.expander("🔍 Náhled — strukturovaná data AI", expanded=False):
                st.code(llm_prompt[:6000], language="markdown")
                if len(llm_prompt) > 6000:
                    st.caption(f"... a {len(llm_prompt) - 6000} dalších znaků")

            # ═══════════════════════════════════════════════════════════
            # DOWNLOAD ARTIFACTS (až po všech datech — Fitts' Law, Gestalt proximity)
            # ═══════════════════════════════════════════════════════════
            st.markdown("<p class='section-header' style='margin-top:16px;'>Stáhnout výstup</p>", unsafe_allow_html=True)
            stem = uploaded_file.name.split('.')[0]

            json_str = json.dumps(item, indent=2, ensure_ascii=False, default=str)

            csv_layers_buf = io.StringIO()
            csv_layers_buf.write("vrstva,nastroj,rychlost_mm_s,h1_mm,h2_mm,start_ext_mm,end_ext_mm,delka_mm,operace\n")
            for idx, layer in enumerate(active_layers):
                csv_layers_buf.write(f"{idx+1},{layer['cutter_type']},{layer['speed_mms']},{layer['travel_safety_height_mm']},{layer['end_height_h2_mm']},{layer.get('starting_extension_mm',0.0)},{layer.get('ending_extension_mm',0.0)},{layer['total_cut_length_mm']},{layer['operation_type']}\n")
            csv_layers_str = csv_layers_buf.getvalue()

            col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)
            with col_dl1:
                st.download_button("📦 JSON", json_str, f"{stem}_v20.json", "JSON — kompletní parsovaná data", type="primary")
            with col_dl2:
                md_report = engine.generate_markdown_output()
                st.download_button("📝 Markdown", md_report, f"report_v20_{stem}.md", "MD — technická zpráva")
            with col_dl3:
                st.download_button("📊 CSV vrstvy", csv_layers_str, f"{stem}_vrstvy.csv", "CSV — specifikace vrstev")
            with col_dl4:
                if png_bytes:
                    st.download_button("🖼 PNG 2D", png_bytes, f"{stem}_2d.png", "PNG — 1920×1080 vizualizace")

            col_dl5, col_dl6, _, _ = st.columns(4)
            with col_dl5:
                st.download_button("🧠 TXT výrobní data", llm_prompt, f"{stem}_vyrobni_data.txt", "TXT — strukturovaná data pro AI")
            with col_dl6:
                if png_bytes:
                    st.download_button("📦 ZIP", "ZIP dostupný v deploy verzi", f"{stem}_placeholder.zip", disabled=True)

            # ── FOOTER ──
            st.markdown(f"""
<div class="systeq-footer">
  <div class="sf-logo"><span class="sf-sys">SYS</span><span class="sf-teq">TEQ</span> © 2026</div>
  <div class="sf-contact"><a href="mailto:sousek@systeq.cz">sousek@systeq.cz</a> · <a href="tel:+420735045256">+420 735 045 256</a></div>
  <div class="sf-meta">Engine v20 deterministic · outpost2026</div>
  <div class="sf-motto">Hledám funkční řešení v balastu.</div>
</div>
""", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Chyba při vizualizaci dat: {str(e)}")
else:
    st.markdown("""
    <div style='text-align:center; color:#374151; margin-top:80px; padding:40px;'>
        <p style='font-size:60px;'>└✦┘</p>
        <p style='font-size:16px;'>Přetáhněte VCF soubor pro sémantickou analýzu</p>
    </div>
    """, unsafe_allow_html=True)
