"""Vulnerability Explorer and Table Components (Member 3 - Frontend).

Provides interactive, filterable, and searchable views into attack test results,
clearly distinguishing between preliminary heuristic screening and final evaluation.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any


def render_verdict_badge(verdict: str, eval_status: str) -> str:
    """Return colored HTML badge for a test's screening verdict and status."""
    if eval_status == "error":
        return '<span class="ps-badge badge-danger">⚠️ Error</span>'

    if verdict == "likely_safe":
        return '<span class="ps-badge badge-success">🟢 Likely Safe (Passed)</span>'
    elif verdict == "suspected_violation":
        return '<span class="ps-badge badge-danger">🔴 Suspected Violation</span>'
    elif verdict == "unclear":
        return '<span class="ps-badge badge-warning">🟡 Inconclusive</span>'
    else:
        return '<span class="ps-badge badge-neutral">⚪ Pending</span>'


def render_results_explorer(results: List[Dict[str, Any]]):
    """Render the filterable, searchable Vulnerability Explorer table and expandable detail cards."""
    if not results:
        st.markdown(
            """
            <div class="ps-card" style="text-align: center; padding: 3rem 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #F8FAFC;">No Evaluation Results Found</div>
                <div style="color: #94A3B8; font-size: 0.9rem; margin-top: 0.25rem;">
                    Run attacks from the <b>Test Execution</b> tab or load a saved experiment from the <b>Overview</b> page.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Filter Controls
    fc1, fc2, fc3 = st.columns([2, 1, 1])

    with fc1:
        search_term = st.text_input(
            "Search attacks, responses, or categories",
            placeholder="Type keyword (e.g., 'refund', 'override', 'order')...",
        ).strip().lower()

    with fc2:
        all_categories = sorted(list({r.get("category", "General") for r in results}))
        selected_cats = st.multiselect("Filter Category", options=all_categories, default=all_categories)

    with fc3:
        verdict_filter = st.selectbox(
            "Filter Verdict",
            options=["All Verdicts", "Likely Safe", "Suspected Violation", "Inconclusive", "Errors"],
            index=0,
        )

    # Apply Filters
    filtered = []
    for r in results:
        cat = r.get("category", "General")
        verdict = r.get("heuristic_verdict", "unclear")
        status = r.get("evaluation_status", "pending")

        # Category filter
        if cat not in selected_cats:
            continue

        # Verdict filter
        if verdict_filter == "Likely Safe" and verdict != "likely_safe":
            continue
        elif verdict_filter == "Suspected Violation" and verdict != "suspected_violation":
            continue
        elif verdict_filter == "Inconclusive" and verdict != "unclear":
            continue
        elif verdict_filter == "Errors" and status != "error":
            continue

        # Search filter
        if search_term:
            prompt_text = r.get("attack_prompt", "").lower()
            resp_text = r.get("target_response", "").lower()
            cat_text = cat.lower()
            if search_term not in prompt_text and search_term not in resp_text and search_term not in cat_text:
                continue

        filtered.append(r)

    st.markdown(
        f"<div style='font-size: 0.85rem; color: #94A3B8; margin-bottom: 0.75rem;'>Showing <b>{len(filtered)}</b> of {len(results)} test cases</div>",
        unsafe_allow_html=True,
    )

    if not filtered:
        st.info("No test cases match your selected filters.")
        return

    # Expandable Test Detail Cards
    for i, r in enumerate(filtered):
        attack_id = r.get("attack_id", str(i + 1))
        category = r.get("category", "Uncategorized")
        verdict = r.get("heuristic_verdict", "unclear")
        status = r.get("evaluation_status", "pending")
        badge = render_verdict_badge(verdict, status)

        with st.expander(f"Attack #{attack_id} — {category} | {verdict.replace('_', ' ').title()}", expanded=(i == 0)):
            col_left, col_right = st.columns([1, 1])

            with col_left:
                st.markdown(f"**Category:** `{category}` &nbsp; {badge}", unsafe_allow_html=True)
                st.markdown("**Adversarial Attack Prompt:**")
                st.markdown(f'<div class="ps-code-block">{r.get("attack_prompt", "")}</div>', unsafe_allow_html=True)

                st.markdown("**Expected Safe Behavior:**")
                st.caption(r.get("expected_safe_behavior", "None specified."))

            with col_right:
                st.markdown(f"**Target Model:** `{r.get('model', 'unknown')}`")
                st.markdown("**Actual Chatbot Response:**")
                response_content = r.get("target_response", "")
                if response_content:
                    st.markdown(f'<div class="ps-code-block">{response_content}</div>', unsafe_allow_html=True)
                else:
                    st.caption("*No response received (or error occurred)*")

                # Heuristic Flags
                flags = r.get("heuristic_flags", [])
                if flags:
                    st.markdown("**Heuristic Trigger Flags:**")
                    flag_badges = " ".join([f'<span class="ps-badge badge-warning">{f}</span>' for f in flags])
                    st.markdown(flag_badges, unsafe_allow_html=True)
                else:
                    st.markdown("<span style='font-size: 0.8rem; color: #94A3B8;'>No rule flags triggered</span>", unsafe_allow_html=True)

                # Error display if present
                if r.get("error"):
                    st.error(f"Execution Error: {r['error']}")
