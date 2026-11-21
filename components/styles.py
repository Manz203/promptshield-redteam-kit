"""Visual Design System and CSS Injection for PromptShield (Member 3).

Applies deep charcoal background (#0B0F19), dark slate sidebar (#111827),
elevated cards (#161F30), and purple/cyan security accents.
"""

import streamlit as st

CUSTOM_CSS = """
<style>
/* ---------------- Root Colors & Fonts ---------------- */
:root {
    --bg-main: #0B0F19;
    --bg-sidebar: #111827;
    --bg-card: #161F30;
    --border-subtle: #1E293B;
    --accent-primary: #8B5CF6;
    --accent-secondary: #22D3EE;
    --status-success: #22C55E;
    --status-danger: #EF4444;
    --status-warning: #F59E0B;
    --text-primary: #F8FAFC;
    --text-muted: #94A3B8;
}

/* Main Streamlit App Background */
.stApp {
    background-color: var(--bg-main);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar);
    border-right: 1px solid var(--border-subtle);
}

/* Card Container */
.ps-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
}

.ps-card:hover {
    border-color: rgba(139, 92, 246, 0.4);
    transition: border-color 0.2s ease;
}

/* Header Banner */
.ps-header {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(34, 211, 238, 0.1) 100%);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 12px;
    padding: 1.25rem 1.75rem;
    margin-bottom: 1.5rem;
}

.ps-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.025em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.ps-subtitle {
    font-size: 0.95rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
}

/* Metric KPI Card */
.ps-metric-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    text-align: left;
}

.ps-metric-label {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
}

.ps-metric-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
}

.ps-metric-subtext {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 0.35rem;
}

/* Badges */
.ps-badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 9999px;
    letter-spacing: 0.025em;
}

.badge-success {
    background-color: rgba(34, 197, 94, 0.15);
    color: #4ADE80;
    border: 1px solid rgba(34, 197, 94, 0.3);
}

.badge-danger {
    background-color: rgba(239, 68, 68, 0.15);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.badge-warning {
    background-color: rgba(245, 158, 11, 0.15);
    color: #FBBF24;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.badge-info {
    background-color: rgba(34, 211, 238, 0.15);
    color: #38BDF8;
    border: 1px solid rgba(34, 211, 238, 0.3);
}

.badge-neutral {
    background-color: rgba(148, 163, 184, 0.15);
    color: #CBD5E1;
    border: 1px solid rgba(148, 163, 184, 0.3);
}

/* Code & Pre Blocks */
.ps-code-block {
    background-color: #0F172A;
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.85rem 1rem;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 0.85rem;
    color: #E2E8F0;
    white-space: pre-wrap;
    word-break: break-word;
}

/* Streamlit Widget Tweaks */
div[data-baseweb="select"] {
    background-color: var(--bg-card);
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--border-subtle);
}

.stTabs [data-baseweb="tab"] {
    padding: 8px 16px;
    color: var(--text-muted);
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    color: var(--accent-secondary) !important;
    border-bottom: 2px solid var(--accent-secondary) !important;
}

/* Buttons */
.stButton>button {
    border-radius: 8px;
    font-weight: 600;
    border: 1px solid rgba(139, 92, 246, 0.4);
    background-color: #1E293B;
    color: #F8FAFC;
    transition: all 0.2s ease;
}

.stButton>button:hover {
    border-color: var(--accent-primary);
    background-color: rgba(139, 92, 246, 0.2);
    color: #FFFFFF;
}

.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
    border: 1px solid #7C3AED;
    color: #FFFFFF;
}

.stButton>button[kind="primary"]:hover {
    background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.35);
}
</style>
"""


def apply_theme():
    """Inject custom PromptShield security dashboard CSS into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
