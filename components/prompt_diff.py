"""Guardrail Prompt Diff Component (Member 3 - Frontend).

Displays side-by-side comparison between the original baseline system prompt
and the guardrail-enhanced system prompt.
"""

import streamlit as st


def render_prompt_diff_view(
    original_prompt: str,
    improved_prompt: str,
    recommendations: list,
    findings: list,
):
    """Render a side-by-side prompt comparison and security findings."""
    st.markdown("### 🛡️ System Prompt Security Hardening")

    # Metrics row for findings and recommendations
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""
            <div class="ps-card">
                <div style="font-size: 0.85rem; color: #94A3B8;">SECURITY FINDINGS DETECTED</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #EF4444;">{len(findings)}</div>
                <div style="font-size: 0.8rem; color: #94A3B8;">Identified failure modes during attack evaluation</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="ps-card">
                <div style="font-size: 0.85rem; color: #94A3B8;">GUARDRAIL RULES INJECTED</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #22C55E;">{len(recommendations)}</div>
                <div style="font-size: 0.8rem; color: #94A3B8;">Hardened constraint clauses added to prompt</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Detailed recommendations list
    if recommendations:
        with st.expander("View Injected Guardrail Rules", expanded=True):
            for idx, rule in enumerate(recommendations, start=1):
                st.markdown(f"**{idx}.** {rule}")

    # Side-by-side prompt comparison
    st.markdown("#### Side-by-Side Prompt Comparison")
    p1, p2 = st.columns(2)

    with p1:
        st.markdown("**Original Baseline Prompt**")
        st.markdown(
            f'<div class="ps-code-block" style="border-color: rgba(239, 68, 68, 0.4);">{original_prompt}</div>',
            unsafe_allow_html=True,
        )

    with p2:
        st.markdown("**Hardened Guardrail Prompt (Member 4)**")
        st.markdown(
            f'<div class="ps-code-block" style="border-color: rgba(34, 197, 94, 0.4);">{improved_prompt}</div>',
            unsafe_allow_html=True,
        )
