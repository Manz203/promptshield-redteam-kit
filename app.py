"""PromptShield — AI Prompt Injection Testing and Red-Teaming Toolkit.

Member 3: Frontend, Dashboard & UI Integration
"""

from pathlib import Path
import os
import sys
import streamlit as st

# Ensure repository root is on sys.path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from components.styles import apply_theme
from components.sidebar import render_sidebar
from components.metrics import render_security_kpis
from components.charts import (
    plot_verdict_donut,
    plot_category_asr_bar,
    plot_ab_comparison_bar,
    plot_version_comparison_summary,
)
from components.tables import render_results_explorer
from components.prompt_diff import render_prompt_diff_view
from components.export import render_export_section
from components.adapters import (
    BackendAdapter,
    DEFAULT_SYSTEM_PROMPT,
    PRESET_SYSTEM_PROMPTS,
)
from src.dashboard import (
    calculate_metrics,
    calculate_category_breakdown,
    calculate_ab_comparison,
    list_saved_experiments,
    load_saved_experiment,
    STANDARD_CATEGORIES,
)

# Streamlit Page Config
st.set_page_config(
    page_title="PromptShield — AI Red-Teaming Toolkit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom dark SaaS design system
apply_theme()


def init_session_state():
    """Initialize global session state variables with clean defaults."""
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Overview"
    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = DEFAULT_SYSTEM_PROMPT
    if "attacks" not in st.session_state:
        st.session_state["attacks"] = []
    if "results" not in st.session_state:
        # Preload v2 test results if available for instant overview data
        default_exp = load_saved_experiment("chatbot_test_results_v2.json")
        st.session_state["results"] = default_exp if default_exp else []
    if "improved_prompt" not in st.session_state:
        st.session_state["improved_prompt"] = ""
    if "guardrail_data" not in st.session_state:
        st.session_state["guardrail_data"] = {}
    if "improved_results" not in st.session_state:
        # Preload improved results if available for instant A/B demonstration
        impr_exp = load_saved_experiment("member4_improved_results.json")
        st.session_state["improved_results"] = impr_exp if impr_exp else []
    if "use_mock" not in st.session_state:
        st.session_state["use_mock"] = not BackendAdapter.is_api_key_set()


init_session_state()

# Render Sidebar Navigation
active_page = render_sidebar()

# Main Header Banner
st.markdown(
    """
    <div class="ps-header">
        <div class="ps-title">
            <span>🛡️</span> PromptShield Red-Team Dashboard
        </div>
        <div class="ps-subtitle">
            Automated Adversarial Testing, Vulnerability Evaluation & Guardrail Hardening for LLM Chatbots
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================================
# SECTION 1: OVERVIEW
# =========================================================================
if active_page == "Overview":
    st.markdown("### 📊 Security Posture Overview")

    # Experiment selector
    exp_col1, exp_col2 = st.columns([3, 1])
    with exp_col1:
        saved_files = list_saved_experiments()
        if saved_files:
            selected_exp = st.selectbox(
                "Active Test Run Source",
                options=["Current Session (Live/Cached)"] + saved_files,
                index=0,
                help="Inspect pre-recorded benchmark experiments or view current session test results.",
            )
            if selected_exp != "Current Session (Live/Cached)":
                loaded = load_saved_experiment(selected_exp)
                if loaded:
                    st.session_state["results"] = loaded
                    st.toast(f"Loaded experiment: {selected_exp}")

    with exp_col2:
        if st.button("Start New Test Run", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Attack Playground"
            st.rerun()

    results = st.session_state.get("results", [])
    metrics = calculate_metrics(results)
    cat_df = calculate_category_breakdown(results)

    # Render top-level KPI cards
    render_security_kpis(metrics)

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # Charts Row
    chart_col1, chart_col2 = st.columns([1, 1])
    with chart_col1:
        st.plotly_chart(plot_verdict_donut(metrics), use_container_width=True)

    with chart_col2:
        st.plotly_chart(plot_category_asr_bar(cat_df), use_container_width=True)

    # Summary analysis
    st.markdown("#### 🚨 Vulnerability Highlights")
    h1, h2 = st.columns(2)

    with h1:
        st.markdown("**Most Vulnerable Categories:**")
        if not cat_df.empty:
            vulnerable_cats = cat_df.sort_values(by="ASR (%)", ascending=False)
            for _, row in vulnerable_cats.iterrows():
                if row["ASR (%)"] > 0:
                    st.markdown(
                        f"- **{row['Category']}**: `{row['ASR (%)']}% ASR` ({row['Suspected Violations']}/{row['Total']} failed)"
                    )
                else:
                    st.markdown(f"- **{row['Category']}**: `0% ASR` (Protected)")
        else:
            st.caption("No category evaluation data available.")

    with h2:
        st.markdown("**Recent Suspected Violations:**")
        violations = [r for r in results if r.get("heuristic_verdict") == "suspected_violation"]
        if violations:
            for v in violations[:3]:
                st.markdown(
                    f"- `[{v.get('category')}]` Attack #{v.get('attack_id')}: *\"{v.get('attack_prompt')[:75]}...\"*"
                )
        else:
            st.markdown("<span style='color: #22C55E;'>✅ No active rule violations detected in this test run.</span>", unsafe_allow_html=True)


# =========================================================================
# SECTION 2: ATTACK PLAYGROUND
# =========================================================================
elif active_page == "Attack Playground":
    st.markdown("### ⚔️ Adversarial Attack Playground")
    st.markdown(
        "Define target chatbot instructions, configure red-teaming parameters, and generate targeted adversarial attacks."
    )

    # Target System Prompt Editor
    st.markdown("#### 1. Target System Prompt")
    current_prompt = st.session_state.get("system_prompt", DEFAULT_SYSTEM_PROMPT)

    prompt_input = st.text_area(
        "Chatbot Instructions",
        value=current_prompt,
        height=140,
        placeholder="Enter the system prompt governing your target chatbot...",
        help="The attack generator will target the specific constraints and permissions stated here.",
    )
    st.session_state["system_prompt"] = prompt_input

    char_col1, char_col2 = st.columns([1, 1])
    with char_col1:
        st.caption(f"Prompt Length: **{len(prompt_input)}** characters • **{len(prompt_input.split())}** words")
    with char_col2:
        if st.button("Reset to Default Prompt"):
            st.session_state["system_prompt"] = DEFAULT_SYSTEM_PROMPT
            st.rerun()

    st.markdown("<hr style='border-color: #1E293B; margin: 1.5rem 0;'>", unsafe_allow_html=True)

    # Attack Configuration
    st.markdown("#### 2. Attack Generation Parameters")
    cfg_col1, cfg_col2, cfg_col3 = st.columns(3)

    with cfg_col1:
        generator_version = st.selectbox(
            "Generator Prompt Version",
            options=["v3", "v2", "v1"],
            index=0,
            help="v3 contains refined negative constraints and few-shot examples.",
        )

    with cfg_col2:
        num_attacks = st.slider(
            "Number of Attacks",
            min_value=1,
            max_value=15,
            value=5,
            help="Number of adversarial test prompts to create.",
        )

    with cfg_col3:
        target_model_display = BackendAdapter.get_target_model()
        st.text_input("Active Target Model", value=target_model_display, disabled=True)

    # Attack Categories Filter
    selected_categories = st.multiselect(
        "Target Attack Categories",
        options=STANDARD_CATEGORIES,
        default=STANDARD_CATEGORIES,
        help="Select which adversarial attack vectors to include in the generated batch.",
    )

    # Generate Attacks Button
    if st.button("Generate Adversarial Attacks", type="primary", use_container_width=True):
        if not prompt_input.strip():
            st.error("Please enter a non-empty target system prompt.")
        else:
            with st.spinner("Generating adversarial test prompts via LLM..."):
                try:
                    generated = BackendAdapter.generate_attacks_safe(
                        system_prompt=prompt_input,
                        num_attacks=num_attacks,
                        version=generator_version,
                        use_mock=st.session_state.get("use_mock", False),
                    )
                    # Filter by selected categories if user customized them
                    if selected_categories:
                        filtered_gen = [a for a in generated if a.get("category") in selected_categories]
                        st.session_state["attacks"] = filtered_gen if filtered_gen else generated
                    else:
                        st.session_state["attacks"] = generated

                    st.toast(f"Successfully generated {len(st.session_state['attacks'])} attacks!")
                except Exception as exc:
                    st.error(f"Attack generation error: {exc}")

    # Preview Generated Attacks
    attacks = st.session_state.get("attacks", [])
    if attacks:
        st.markdown(f"#### 3. Generated Attack Cases ({len(attacks)})")
        for idx, atk in enumerate(attacks, start=1):
            with st.expander(f"Attack #{atk.get('attack_id', idx)} — [{atk.get('category')}]", expanded=(idx <= 2)):
                st.markdown(f"**Attack Vector:** `{atk.get('category')}`")
                st.markdown("**Adversarial Prompt:**")
                st.markdown(f'<div class="ps-code-block">{atk.get("attack_prompt")}</div>', unsafe_allow_html=True)
                st.markdown("**Expected Safe Behavior:**")
                st.caption(atk.get("expected_safe_behavior"))

        if st.button("Proceed to Test Execution ➔", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "Test Execution"
            st.rerun()


# =========================================================================
# SECTION 3: TEST EXECUTION
# =========================================================================
elif active_page == "Test Execution":
    st.markdown("### 🧪 Target Chatbot Test Execution")
    st.markdown("Send generated adversarial prompts against the sandboxed target chatbot and record live responses.")

    attacks = st.session_state.get("attacks", [])
    system_prompt = st.session_state.get("system_prompt", DEFAULT_SYSTEM_PROMPT)

    if not attacks:
        st.warning("No attacks found in the current session. Go to Attack Playground to generate or load attacks.")
        if st.button("Load Pre-Generated v2 Attack Suite"):
            sample = load_saved_experiment("attack_results_v2.json")
            if sample:
                st.session_state["attacks"] = sample
                st.rerun()

    # Pre-flight Check
    st.markdown(
        f"""
        <div class="ps-card">
            <div style="font-size: 0.9rem; font-weight: 600; color: #F8FAFC; margin-bottom: 0.5rem;">Pre-Flight Execution Summary</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">• Target Prompt Length: <b>{len(system_prompt)} chars</b></div>
            <div style="font-size: 0.85rem; color: #94A3B8;">• Attacks Queued: <b>{len(attacks)} test cases</b></div>
            <div style="font-size: 0.85rem; color: #94A3B8;">• Execution Mode: <b>{'Offline Mock (No API Calls)' if st.session_state.get('use_mock') else 'Live Groq API'}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    exec_col1, exec_col2 = st.columns([1, 1])
    with exec_col1:
        delay_slider = st.slider("Request Throttle Delay (seconds)", min_value=0.0, max_value=2.0, value=0.3, step=0.1)

    with exec_col2:
        retries_select = st.selectbox("Max Retries on Error", options=[0, 1, 2], index=1)

    # Execution Action
    if st.button("Execute Attacks Against Target Chatbot", type="primary", use_container_width=True, disabled=len(attacks) == 0):
        progress_bar = st.progress(0.0)
        status_box = st.empty()
        executed_records = []

        total_attacks = len(attacks)
        use_mock = st.session_state.get("use_mock", False)

        for curr_idx, total_count, record, err in BackendAdapter.run_tests_streaming(
            attacks=attacks,
            system_prompt=system_prompt,
            use_mock=use_mock,
            delay=delay_slider,
            retries=retries_select,
        ):
            progress_bar.progress(curr_idx / total_count)
            status_box.markdown(
                f"<div style='font-size: 0.85rem; color: #22D3EE;'>Running attack {curr_idx}/{total_count}: <b>{record.get('category')}</b> — Verdict: <b>{record.get('heuristic_verdict', 'evaluating')}</b></div>",
                unsafe_allow_html=True,
            )
            executed_records.append(record)

        st.session_state["results"] = executed_records
        status_box.markdown(
            f"<div style='font-size: 0.9rem; color: #22C55E; font-weight: 600;'>✅ Completed testing {len(executed_records)} attack prompts!</div>",
            unsafe_allow_html=True,
        )

    # Show execution results summary if available
    results = st.session_state.get("results", [])
    if results:
        st.markdown("<hr style='border-color: #1E293B; margin: 1.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("#### Execution Results Summary")
        m = calculate_metrics(results)
        render_security_kpis(m)

        if st.button("Inspect Detailed Results in Vulnerability Explorer ➔"):
            st.session_state["current_page"] = "Vulnerability Explorer"
            st.rerun()


# =========================================================================
# SECTION 4: VULNERABILITY EXPLORER
# =========================================================================
elif active_page == "Vulnerability Explorer":
    st.markdown("### 🔍 Vulnerability & Evaluation Explorer")
    st.markdown(
        "Audit detailed target chatbot responses against attack prompts, inspect heuristic screening flags, and evaluate safety violations."
    )

    results = st.session_state.get("results", [])
    render_results_explorer(results)


# =========================================================================
# SECTION 5: GUARDRAIL LAB
# =========================================================================
elif active_page == "Guardrail Lab":
    st.markdown("### 🛡️ Guardrail Hardening & A/B Benchmark")
    st.markdown(
        "Analyze failure modes from attack tests, inject safety constraints via Member 4's guardrail recommender, and compare baseline vs. improved system prompt performance."
    )

    results = st.session_state.get("results", [])
    system_prompt = st.session_state.get("system_prompt", DEFAULT_SYSTEM_PROMPT)

    if not results:
        st.warning("No evaluation results found to analyze. Load an experiment or run test attacks first.")
        if st.button("Load Member 4 Original Baseline Results"):
            baseline_sample = load_saved_experiment("member4_original_results.json")
            if baseline_sample:
                st.session_state["results"] = baseline_sample
                st.rerun()

    # Generate Guardrails
    if st.button("Generate Guardrail Recommendations (Member 4)", type="primary", use_container_width=True, disabled=len(results) == 0):
        with st.spinner("Analyzing vulnerabilities and generating guardrails..."):
            try:
                g_data = BackendAdapter.recommend_guardrails_safe(
                    system_prompt=system_prompt,
                    test_results=results,
                )
                st.session_state["guardrail_data"] = g_data
                st.session_state["improved_prompt"] = g_data.get("improved_system_prompt", "")
                st.toast("Guardrails generated successfully!")
            except Exception as exc:
                st.error(f"Guardrail error: {exc}")

    # Display Guardrail View
    g_data = st.session_state.get("guardrail_data", {})
    improved_prompt = st.session_state.get("improved_prompt", "")

    if improved_prompt:
        render_prompt_diff_view(
            original_prompt=system_prompt,
            improved_prompt=improved_prompt,
            recommendations=g_data.get("recommendations", []),
            findings=g_data.get("findings", []),
        )

        st.markdown("<hr style='border-color: #1E293B; margin: 1.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("#### Retest Attacks on Guardrailed Prompt")

        retest_col1, retest_col2 = st.columns([2, 1])
        with retest_col1:
            st.caption("Execute the identical attack test cases against the newly hardened prompt to evaluate ASR reduction.")

        with retest_col2:
            if st.button("Execute A/B Retest", type="primary", use_container_width=True):
                attacks_to_test = st.session_state.get("attacks", [])
                if not attacks_to_test:
                    # Use attacks from baseline results
                    attacks_to_test = [
                        {
                            "attack_id": r.get("attack_id"),
                            "category": r.get("category"),
                            "attack_prompt": r.get("attack_prompt"),
                            "expected_safe_behavior": r.get("expected_safe_behavior"),
                        }
                        for r in results
                    ]

                p_bar = st.progress(0.0)
                retest_records = []
                for idx, total, record, err in BackendAdapter.run_tests_streaming(
                    attacks=attacks_to_test,
                    system_prompt=improved_prompt,
                    use_mock=st.session_state.get("use_mock", False),
                ):
                    p_bar.progress(idx / total)
                    retest_records.append(record)

                st.session_state["improved_results"] = retest_records
                st.toast("Retest complete!")

        # A/B Comparison Visuals
        improved_results = st.session_state.get("improved_results", [])
        if improved_results:
            ab_comp = calculate_ab_comparison(results, improved_results)

            st.markdown("#### A/B Guardrail Benchmark Results")
            kpi_c1, kpi_c2, kpi_c3 = st.columns(3)
            with kpi_c1:
                st.metric(
                    label="Baseline Attack Success Rate",
                    value=f"{ab_comp['baseline_metrics']['asr_percent']}%",
                )
            with kpi_c2:
                st.metric(
                    label="Guardrailed Attack Success Rate",
                    value=f"{ab_comp['improved_metrics']['asr_percent']}%",
                    delta=f"-{ab_comp['asr_delta_reduction']}%",
                    delta_color="inverse",
                )
            with kpi_c3:
                st.metric(
                    label="Violations Mitigated",
                    value=str(ab_comp["violation_reduction"]),
                )

            st.plotly_chart(plot_ab_comparison_bar(ab_comp), use_container_width=True)


# =========================================================================
# SECTION 6: EXPORTS & REPORTS
# =========================================================================
elif active_page == "Export & Reports":
    st.markdown("### 📁 Export & Audit Reports")
    st.markdown(
        "Download test results, evaluation logs, and audit reports for academic submission or security reviews."
    )

    results = st.session_state.get("results", [])
    system_prompt = st.session_state.get("system_prompt", DEFAULT_SYSTEM_PROMPT)
    improved_prompt = st.session_state.get("improved_prompt", "")

    render_export_section(
        results=results,
        system_prompt=system_prompt,
        improved_prompt=improved_prompt,
    )

    # Prompt generator version benchmark display
    summary_path = ROOT / "experiments" / "evaluation_summary.json"
    if summary_path.exists():
        try:
            summary_data = json.loads(summary_path.read_text(encoding="utf-8"))
            if isinstance(summary_data, list):
                st.markdown("<hr style='border-color: #1E293B; margin: 1.5rem 0;'>", unsafe_allow_html=True)
                st.markdown("#### Historical Attack Generator Version Benchmark")
                st.plotly_chart(plot_version_comparison_summary(summary_data), use_container_width=True)
        except Exception:
            pass
