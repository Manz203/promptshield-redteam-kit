"""Plotly Visualization Components (Member 3 - Frontend).

Dark-themed security charts using Plotly:
- Pass/Fail/Inconclusive donut chart
- Attack Success Rate by category bar chart
- A/B comparison grouped bar chart
- Version comparison chart
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any, List

THEME_BG = "#161F30"
THEME_TEXT = "#F8FAFC"
THEME_MUTED = "#94A3B8"
COLOR_SAFE = "#22C55E"        # Green
COLOR_VIOLATION = "#EF4444"   # Red
COLOR_UNCLEAR = "#F59E0B"     # Amber
COLOR_PRIMARY = "#8B5CF6"     # Purple
COLOR_CYAN = "#22D3EE"        # Cyan


def apply_dark_layout(fig: go.Figure, title: str, height: int = 350) -> go.Figure:
    """Apply consistent PromptShield dark theme styling to a Plotly figure."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(color=THEME_TEXT, size=15),
            x=0.02,
            y=0.96,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=THEME_MUTED, size=12),
        margin=dict(l=20, r=20, t=45, b=25),
        height=height,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color=THEME_TEXT),
        ),
    )
    return fig


def plot_verdict_donut(metrics: Dict[str, Any]) -> go.Figure:
    """Create a donut chart of screening verdicts: Likely Safe vs. Suspected Violation vs. Inconclusive."""
    labels = ["Likely Safe", "Suspected Violation", "Inconclusive / Unclear"]
    values = [
        metrics.get("likely_safe", 0),
        metrics.get("suspected_violations", 0),
        metrics.get("inconclusive", 0) + metrics.get("errors", 0),
    ]
    colors = [COLOR_SAFE, COLOR_VIOLATION, COLOR_UNCLEAR]

    # Filter out 0 values if everything is empty
    if sum(values) == 0:
        labels = ["No Data"]
        values = [1]
        colors = ["#334155"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.62,
                marker=dict(colors=colors, line=dict(color="#0B0F19", width=2)),
                textinfo="label+percent" if sum(values) > 1 else "none",
                hoverinfo="label+value+percent",
            )
        ]
    )

    asr = metrics.get("asr_percent", 0.0)
    fig.add_annotation(
        text=f"<b>{asr}%</b><br><span style='font-size:10px; color:{THEME_MUTED}'>ASR</span>",
        x=0.5,
        y=0.5,
        font=dict(size=18, color=THEME_TEXT),
        showarrow=False,
    )

    return apply_dark_layout(fig, "Safety Screening Distribution", height=320)


def plot_category_asr_bar(category_df: pd.DataFrame) -> go.Figure:
    """Create a horizontal or vertical bar chart showing Attack Success Rate by category."""
    if category_df.empty:
        fig = go.Figure()
        return apply_dark_layout(fig, "Attack Success Rate by Category (No Data)", height=320)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=category_df["Category"],
            y=category_df["ASR (%)"],
            marker_color=COLOR_PRIMARY,
            text=[f"{v}%" for v in category_df["ASR (%)"]],
            textposition="auto",
            name="ASR (%)",
            hovertemplate="<b>%{x}</b><br>Attack Success Rate: %{y}%<extra></extra>",
        )
    )

    fig.update_yaxes(
        range=[0, 100],
        title="ASR (%)",
        gridcolor="#1E293B",
        zerolinecolor="#1E293B",
    )
    fig.update_xaxes(gridcolor="#1E293B")

    return apply_dark_layout(fig, "Attack Success Rate by Category", height=320)


def plot_ab_comparison_bar(comparison_dict: Dict[str, Any]) -> go.Figure:
    """Create a grouped bar chart comparing Baseline vs. Improved prompt performance per category."""
    df = comparison_dict.get("category_comparison_df", pd.DataFrame())
    if df.empty or "ASR (%) (Baseline)" not in df.columns:
        fig = go.Figure()
        return apply_dark_layout(fig, "A/B Guardrail Benchmark (No Data)", height=340)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["Category"],
            y=df["ASR (%) (Baseline)"],
            name="Baseline Prompt ASR (%)",
            marker_color=COLOR_VIOLATION,
            text=[f"{v}%" for v in df["ASR (%) (Baseline)"]],
            textposition="auto",
        )
    )
    fig.add_trace(
        go.Bar(
            x=df["Category"],
            y=df["ASR (%) (Improved)"],
            name="Guardrailed Prompt ASR (%)",
            marker_color=COLOR_SAFE,
            text=[f"{v}%" for v in df["ASR (%) (Improved)"]],
            textposition="auto",
        )
    )

    fig.update_yaxes(
        range=[0, 100],
        title="ASR (%)",
        gridcolor="#1E293B",
        zerolinecolor="#1E293B",
    )
    fig.update_xaxes(gridcolor="#1E293B")

    return apply_dark_layout(fig, "Vulnerability Reduction: Baseline vs. Guardrailed", height=340)


def plot_version_comparison_summary(evaluation_summary: List[Dict[str, Any]]) -> go.Figure:
    """Plot prompt generator version comparison from evaluation_summary.json."""
    if not evaluation_summary:
        fig = go.Figure()
        return apply_dark_layout(fig, "Attack Generator Versions (No Data)", height=300)

    df = pd.DataFrame(evaluation_summary)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["version"].str.upper(),
            y=df["valid_attacks"],
            name="Valid Attacks",
            marker_color=COLOR_CYAN,
        )
    )
    fig.add_trace(
        go.Bar(
            x=df["version"].str.upper(),
            y=df["unique_prompts"],
            name="Unique Prompts",
            marker_color=COLOR_PRIMARY,
        )
    )

    fig.update_yaxes(gridcolor="#1E293B")
    fig.update_xaxes(gridcolor="#1E293B")

    return apply_dark_layout(fig, "Attack Generator Version Quality Benchmark", height=300)
