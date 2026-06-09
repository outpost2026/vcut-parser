import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from vcf_parser_v20 import RuidaVcfEngineV20
import json
import os

def _load_app_config():
    config_path = os.path.join(os.path.dirname(__file__), "app_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

APP_CONFIG = _load_app_config()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Moodpasta Parser Demo")
    pwd = st.text_input("Přístupové heslo", type="password")
    demo_password = APP_CONFIG.get("auth", {}).get("demo_password", "moodpasta-demo-2026")
    if st.button("Přistoupit"):
        if pwd == demo_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Nesprávné heslo")
    st.stop()

st.set_page_config(
    page_title="Moodpasta Manufacturing Intelligence v20 | B2B",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    h1, h2, h3, h4 { font-family: 'Inter', -apple-system, sans-serif !important; font-weight: 700 !important; color: #F8FAFC !important; }
    .metric-card { background-color: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 24px; text-align: center; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    .metric-value { font-size: 32px; font-weight: 800; color: #10B981; }
    .metric-label { font-size: 14px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; }
    .gatekeeper-ok { background-color: #064E3B; border-left: 6px solid #10B981; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
    .gatekeeper-warn { background-color: #1E2030; border-left: 6px solid #F59E0B; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
    .gatekeeper-critical { background-color: #1E2030; border-left: 6px solid #F43F5E; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { color: #94A3B8; font-weight: 600; }
    .stTabs [aria-selected="true"] { color: #10B981 !important; }
    .stButton > button { background-color: #10B981; color: #0F172A; font-weight: 700; border: none; border-radius: 8px; }
    .stButton > button:hover { background-color: #059669; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>Moodpasta Manufacturing Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 16px; margin-bottom: 10px;'>Sémantická validace a autonomní naceňování Ruida .VCF drah | v20 B2B</p>", unsafe_allow_html=True)

ROLE_SELECT = st.selectbox(
    "Přepínač rolí",
    options=["Dílna / CNC", "Obchodní", "MES"],
    index=0,
    label_visibility="collapsed"
)

uploaded_file = st.file_uploader("Nahrajte výrobní soubor .VCF", type=["vcf"], label_visibility="collapsed")

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()

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

            st.markdown("### Klíčové výrobní charakteristiky")
            kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

            with kpi1:
                st.markdown(f"""<div class="metric-card"><div class="metric-label">Odhadovaný čas řezu</div><div class="metric-value">{time_formatted}</div></div>""", unsafe_allow_html=True)
            with kpi2:
                st.markdown(f"""<div class="metric-card"><div class="metric-label">Aktivní dráha řezu</div><div class="metric-value">{total_length_m:.2f} m</div></div>""", unsafe_allow_html=True)
            with kpi3:
                st.markdown(f"""<div class="metric-card"><div class="metric-label">Rozměry (Š × V)</div><div class="metric-value">{width:.0f}×{height:.0f} mm</div></div>""", unsafe_allow_html=True)
            with kpi4:
                conf_color = "#10B981" if mi.get("material_thickness_confidence") == "HIGH" else "#F59E0B"
                st.markdown(f"""<div class="metric-card"><div class="metric-label">Odhad. tloušťka</div><div class="metric-value" style="color: {conf_color};">{thickness:.0f} mm <span style="font-size: 14px; color: #94A3B8;">({mi.get('material_thickness_confidence', 'LOW')})</span></div></div>""", unsafe_allow_html=True)
            with kpi5:
                if is_aggregated and sub_jobs_count > 0:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Sub-zakázky</div><div class="metric-value">{sub_jobs_count} panelů</div></div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Sub-zakázky</div><div class="metric-value">1 panel</div></div>""", unsafe_allow_html=True)
            with kpi6:
                ei = item.get("epistemic_confidence_index", 0.0)
                ei_color = "#10B981" if ei >= 0.4 else ("#F59E0B" if ei >= 0.2 else "#F43F5E")
                ei_label = "Důvěryhodnost" if ei >= 0.4 else ("Částečná" if ei >= 0.2 else "Nízká")
                st.markdown(f"""<div class="metric-card"><div class="metric-label">Epistem. index</div><div class="metric-value" style="color: {ei_color};">{ei*100:.0f} % <span style="font-size: 14px; color: #94A3B8;">({ei_label})</span></div></div>""", unsafe_allow_html=True)

            area_m2 = (width * height) / 1000000.0
            cas_min = item["erp_time_prediction"]["predicted_time_seconds"] / 60.0

            st.markdown("### Sémantický audit a analýza rizik (Gatekeeper)")

            if criticals:
                st.markdown(f"""<div class="gatekeeper-critical"><h4 style="color: #F43F5E !important; margin-top: 0;">Kritická rizika (Index: {risk_score:.2f})</h4><p style="color: #94A3B8; font-size: 14px;">Nalezené anomálie vyžadují zásah operátora.</p></div>""", unsafe_allow_html=True)
                st.error(f"**[CRITICAL]** {criticals[0]['message']}")
                if len(criticals) > 1:
                    with st.expander(f"Dalších {len(criticals) - 1} kritických varování"):
                        for w in criticals[1:]:
                            st.error(f"**[CRITICAL]** {w['message']}")
                if warnings_w:
                    with st.expander(f"{len(warnings_w)} varování (WARNING)"):
                        for w in warnings_w:
                            st.warning(f"**[WARNING]** {w['message']}")
            elif warnings_w:
                st.markdown(f"""<div class="gatekeeper-warn"><h4 style="color: #F59E0B !important; margin-top: 0;">Varování (Index: {risk_score:.2f})</h4></div>""", unsafe_allow_html=True)
                st.warning(f"**[WARNING]** {warnings_w[0]['message']}")
                if len(warnings_w) > 1:
                    with st.expander(f"Dalších {len(warnings_w) - 1} varování"):
                        for w in warnings_w[1:]:
                            st.warning(f"**[WARNING]** {w['message']}")
            else:
                st.markdown("""<div class="gatekeeper-ok"><h4 style="color: #10B981 !important; margin-top: 0;">100 % OK</h4><p style="color: #94A3B8;">Výkres splňuje veškerá fyzikální pravidla pro bezpečný řez.</p></div>""", unsafe_allow_html=True)

            # ----------------------------------------
            #  ROLE: Dílna / CNC
            # ----------------------------------------
            if ROLE_SELECT == "Dílna / CNC":
                st.markdown("#### Technická specifikace vrstev")
                layers_data = []
                for idx, layer in enumerate(item["layers"]):
                    layers_data.append({
                        "Vrstva": idx + 1, "Nástroj": layer["cutter_type"],
                        "Rychlost (mm/s)": layer["speed_mms"],
                        "H1 (mm)": layer["travel_safety_height_mm"],
                        "H2 (mm)": layer["end_height_h2_mm"],
                        "Start Ext (mm)": layer.get("starting_extension_mm", 0.0),
                        "End Ext (mm)": layer.get("ending_extension_mm", 0.0),
                        "Délka (mm)": layer["total_cut_length_mm"],
                        "Operace": layer["operation_type"]
                    })
                st.table(pd.DataFrame(layers_data))

                st.markdown("---")
                col_plot, col_check = st.columns([3, 2])
                with col_plot:
                    st.markdown("#### Digitální model drah")
                    elements = item.get("elements", [])
                    if elements:
                        aspect = width / height if height > 0 else 1.0
                        if aspect > 1.5:
                            fig_w = min(14, max(8, aspect * 3.5))
                            fig_h = fig_w / aspect
                        elif aspect < 0.67:
                            fig_h = min(14, max(8, 4 / aspect))
                            fig_w = fig_h * aspect
                        else:
                            fig_w = fig_h = 8

                        fig, ax = plt.subplots(figsize=(fig_w, fig_h), facecolor="#1E293B")
                        ax.set_facecolor("#0F172A")
                        color_map = {1: "#F43F5E", 5: "#F43F5E", 4: "#3B82F6", 3: "#10B981"}
                        for el in elements[:400]:
                            vertices = el.get("vertices", [])
                            if vertices:
                                xs = [v[0] for v in vertices]
                                ys = [v[1] for v in vertices]
                                col = color_map.get(el.get("geom_type_id", 1), "#64748B")
                                ax.plot(xs, ys, color=col, linewidth=1.2, alpha=0.8)
                        ax.set_title(f"Vizualizace: {uploaded_file.name}", color="#F8FAFC", fontsize=12)
                        ax.tick_params(colors="#94A3B8")
                        for spine in ax.spines.values():
                            spine.set_color("#334155")
                        ax.set_aspect('equal', 'box')
                        st.pyplot(fig)

                with col_check:
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
                    if item.get("is_aggregated_job") and item.get("sub_jobs"):
                        st.markdown("---")
                        st.markdown("**Sub-zakázky:**")
                        sj_df = pd.DataFrame(item["sub_jobs"])[["sub_job_id", "width_mm", "height_mm", "total_length_mm"]]
                        st.dataframe(sj_df, use_container_width=True, hide_index=True)
                    st.markdown("---")
                    st.markdown("**Výrobní instrukce:**")
                    st.info(f"Složitost: {complexity}")
                    st.info(f"Panel: {item.get('detected_panel_format_name', 'Atypický')}")

                    if criticals:
                        st.error("**ZÁSADNÍ RIZIKO!** Před řezem konzultuj s technologem.")

            # ----------------------------------------
            #  ROLE: Obchodní
            # ----------------------------------------
            elif ROLE_SELECT == "Obchodní":
                st.markdown("#### Margin & Cost Calculator")
                col_cost1, col_cost2, col_cost3 = st.columns(3)
                strojni_minuta_kc = APP_CONFIG.get("pricing", {}).get("machine_minute_cost_czk", 18.5)
                cena_material_m2 = APP_CONFIG.get("pricing", {}).get("material_cost_per_m2_czk", 420.0)
                naklady_stroj = cas_min * strojni_minuta_kc
                naklady_material = area_m2 * cena_material_m2
                celkove_naklady = naklady_stroj + naklady_material

                with col_cost1:
                    st.metric("Náklady na strojní čas", f"{naklady_stroj:,.0f} Kč", help=f"{cas_min:.1f} min × {strojni_minuta_kc} Kč/min")
                with col_cost2:
                    st.metric("Náklady na materiál", f"{naklady_material:,.0f} Kč", help=f"{area_m2:.3f} m² × {cena_material_m2} Kč/m²")
                with col_cost3:
                    st.metric("Celkové náklady", f"{celkove_naklady:,.0f} Kč")

                default_margin = APP_CONFIG.get("pricing", {}).get("default_margin_percent", 45)
                marze = st.slider("Požadovaná marže (%)", min_value=20, max_value=80, value=default_margin, step=5)
                prodejni_cena = celkove_naklady * (1 + marze / 100)
                zisk = prodejni_cena - celkove_naklady

                st.markdown(f"""<div class="metric-card" style="margin-top: 20px;"><div class="metric-label">Doporučená prodejní cena ({marze}% marže)</div><div class="metric-value" style="color: #10B981;">{prodejni_cena:,.0f} Kč</div><div style="color: #94A3B8; font-size: 14px;">Zisk: {zisk:,.0f} Kč</div></div>""", unsafe_allow_html=True)

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

            # ----------------------------------------
            #  ROLE: MES
            # ----------------------------------------
            else:
                st.markdown("#### GDrive Monitor (simulace)")
                st.info("Automatické sledování sdíleného disku `gdrive_moodpasta_RnD` je aktivní.")
                st.markdown("#### Historická kalibrace (Historical Calibration Engine)")
                dummy_history = pd.DataFrame({
                    "Datum": ["2026-05-28", "2026-05-29", "2026-05-30", "2026-05-31", "2026-06-01"],
                    "Predikovaný čas (min)": [12.5, 8.3, 15.1, 6.2, cas_min],
                    "Skutečný čas (min)": [13.1, 8.8, 14.7, 6.0, None],
                    "Odchylka (%)": [4.8, 6.0, -2.7, -3.2, None]
                })
                st.dataframe(dummy_history, use_container_width=True, hide_index=True)
                st.markdown("#### Manufacturing Intelligence Log")
                if warnings_list:
                    for w in warnings_list[:20]:
                        icon = "CRIT" if w["severity"] == "CRITICAL" else ("WARN" if w["severity"] == "WARNING" else "INFO")
                        st.text(f"[{icon}] [{w['rule_id']}] {w['message']}")
                    if len(warnings_list) > 20:
                        st.text(f"... a dalších {len(warnings_list) - 20} záznamů")
                else:
                    st.success("Žádné sémantické anomálie v logu.")
                csv_all = engine.generate_markdown_output()
                st.download_button(
                    "Stáhnout kompletní report (.md)",
                    data=csv_all.encode('utf-8'),
                    file_name=f"report_v20_{uploaded_file.name.split('.')[0]}.md",
                    mime="text/markdown"
                )

        except Exception as e:
            st.error(f"Chyba při vizualizaci dat: {str(e)}")
else:
    st.info("Nahrajte .VCF soubor pro spuštění sémantické analýzy.")
