"""Data Export and Report Generation Component (Member 3 - Frontend).

Provides CSV, JSON, and evaluation report exports conforming to stable schemas.
"""

import streamlit as st
import json
import pandas as pd
from typing import List, Dict, Any


def render_export_section(
    results: List[Dict[str, Any]],
    system_prompt: str,
    improved_prompt: str = "",
    filename_prefix: str = "promptshield_results",
):
    """Render export download buttons for test results in JSON and CSV formats."""
    st.markdown("### 📥 Export & Audit Reports")

    if not results:
        st.info("No test results to export. Run tests or load a saved experiment first.")
        return

    # Prepare JSON payload with metadata
    export_payload = {
        "metadata": {
            "tool": "PromptShield AI Red-Teaming Kit",
            "version": "1.0.0",
            "total_tests": len(results),
            "baseline_system_prompt": system_prompt,
            "improved_system_prompt": improved_prompt,
        },
        "results": results,
    }
    json_str = json.dumps(export_payload, indent=2, ensure_ascii=False)

    # Prepare DataFrame for CSV
    df = pd.DataFrame(results)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="ps-card">
                <div style="font-weight: 600; color: #F8FAFC; margin-bottom: 0.5rem;">Export as JSON</div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 1rem;">
                    Full structured evaluation dataset including prompt metadata, heuristic flags, and response records.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button(
            label="Download JSON Dataset",
            data=json_str,
            file_name=f"{filename_prefix}.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        st.markdown(
            """
            <div class="ps-card">
                <div style="font-weight: 600; color: #F8FAFC; margin-bottom: 0.5rem;">Export as CSV</div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 1rem;">
                    Tabular format ready for spreadsheet analysis, compliance reporting, and external red-team audits.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV Table",
            data=csv_data,
            file_name=f"{filename_prefix}.csv",
            mime="text/csv",
            use_container_width=True,
        )
