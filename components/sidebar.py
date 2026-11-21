"""Sidebar Navigation and System Configuration Component (Member 3)."""

import streamlit as st
import os
from components.adapters import BackendAdapter, PRESET_SYSTEM_PROMPTS


def render_sidebar():
    """Render the PromptShield sidebar with navigation, credential controls, and preset selectors.

    Returns:
        selected_page: The active navigation section.
    """
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid #1E293B; margin-bottom: 1rem;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #F8FAFC; display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.4rem;">🛡️</span> PromptShield
                </div>
                <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px;">
                    AI Red-Teaming & Safety Toolkit
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Main Navigation
        nav_options = [
            "Overview",
            "Attack Playground",
            "Test Execution",
            "Vulnerability Explorer",
            "Guardrail Lab",
            "Export & Reports",
        ]
        selected_page = st.radio(
            "Navigation",
            options=nav_options,
            index=nav_options.index(st.session_state.get("current_page", "Overview")),
            label_visibility="collapsed",
        )
        st.session_state["current_page"] = selected_page

        st.markdown("<hr style='border-color: #1E293B; margin: 1.25rem 0;'>", unsafe_allow_html=True)

        # Execution Mode & API Key
        st.markdown("<div style='font-size: 0.85rem; font-weight: 600; color: #F8FAFC; margin-bottom: 8px;'>⚙️ Environment & API</div>", unsafe_allow_html=True)

        use_mock = st.toggle(
            "Offline / Mock Mode",
            value=st.session_state.get("use_mock", not BackendAdapter.is_api_key_set()),
            help="Run tests without API calls using the offline sandboxed mock chatbot and pre-generated attack fixtures.",
        )
        st.session_state["use_mock"] = use_mock

        if not use_mock:
            current_key = os.getenv("GROQ_API_KEY", "")
            entered_key = st.text_input(
                "Groq API Key",
                value=current_key if current_key else st.session_state.get("user_api_key", ""),
                type="password",
                placeholder="gsk_...",
                help="Your API key is kept in memory and never logged.",
            )
            if entered_key:
                os.environ["GROQ_API_KEY"] = entered_key
                st.session_state["user_api_key"] = entered_key
                st.markdown("<span class='ps-badge badge-success'>🟢 Key Active</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span class='ps-badge badge-warning'>⚠️ Key Missing — Switch to Mock</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='ps-badge badge-info'>🔵 Offline Sandbox Mode</span>", unsafe_allow_html=True)

        # Active Model
        target_model = BackendAdapter.get_target_model()
        st.caption(f"Target Model: `{target_model}`")

        st.markdown("<hr style='border-color: #1E293B; margin: 1.25rem 0;'>", unsafe_allow_html=True)

        # Quick System Prompt Presets
        st.markdown("<div style='font-size: 0.85rem; font-weight: 600; color: #F8FAFC; margin-bottom: 8px;'>📋 System Prompt Preset</div>", unsafe_allow_html=True)
        preset_choice = st.selectbox(
            "Load Preset",
            options=list(PRESET_SYSTEM_PROMPTS.keys()),
            index=0,
            label_visibility="collapsed",
        )
        if st.button("Apply Preset", use_container_width=True):
            st.session_state["system_prompt"] = PRESET_SYSTEM_PROMPTS[preset_choice]
            st.toast(f"Loaded preset: {preset_choice}")

        st.markdown(
            """
            <div style="margin-top: 2rem; font-size: 0.72rem; color: #64748B; text-align: center;">
                PromptShield v1.0 • C23 Project<br>Bennett University
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected_page
