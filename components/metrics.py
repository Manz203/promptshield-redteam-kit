"""Security Metrics KPI Components (Member 3 - Frontend)."""

import streamlit as st
from typing import Dict, Any


def render_metric_card(
    label: str,
    value: str,
    subtext: str = "",
    delta: str = "",
    delta_color: str = "normal",
):
    """Render a styled security metric card."""
    delta_html = ""
    if delta:
        color = "#22C55E" if delta_color == "positive" else "#EF4444"
        delta_html = f"<span style='color: {color}; font-size: 0.8rem; font-weight: 600; margin-left: 0.5rem;'>{delta}</span>"

    html = f"""
    <div class="ps-metric-card">
        <div class="ps-metric-label">{label}</div>
        <div class="ps-metric-value">{value}{delta_html}</div>
        <div class="ps-metric-subtext">{subtext}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_security_kpis(metrics: Dict[str, Any]):
    """Render top-level security evaluation KPIs across 5 columns."""
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        render_metric_card(
            label="Total Attacks",
            value=str(metrics.get("total", 0)),
            subtext=f"{len(metrics.get('categories_tested', []))} categories tested",
        )

    with c2:
        render_metric_card(
            label="Likely Safe (Passed)",
            value=str(metrics.get("likely_safe", 0)),
            subtext="Pre-screen passed / refused",
        )

    with c3:
        render_metric_card(
            label="Suspected Violations",
            value=str(metrics.get("suspected_violations", 0)),
            subtext="Rule violation detected",
        )

    with c4:
        asr = metrics.get("asr_percent", 0.0)
        conclusive = metrics.get("conclusive_total", 0)
        render_metric_card(
            label="Attack Success Rate",
            value=f"{asr}%",
            subtext=f"Denominator: {conclusive} conclusive tests",
        )

    with c5:
        inconclusive = metrics.get("inconclusive", 0)
        errors = metrics.get("errors", 0)
        render_metric_card(
            label="Inconclusive / Errors",
            value=f"{inconclusive + errors}",
            subtext=f"{inconclusive} unclear, {errors} errors",
        )
