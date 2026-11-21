"""Dashboard Analytics Module (Member 3 - Frontend & Dashboard).

Calculates security metrics, attack success rates, category breakdowns,
and A/B guardrail comparisons from real test results.
"""

from pathlib import Path
import json
from typing import Dict, List, Any, Optional
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS_DIR = ROOT / "experiments"

# Standard categories recognized across PromptShield
STANDARD_CATEGORIES = [
    "Instruction Override",
    "Role Spoofing",
    "System Prompt Extraction",
    "Fake Authority",
    "Context Manipulation",
]


def calculate_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate core security evaluation metrics from a list of test results.

    Conclusive tests are separated from pending or inconclusive tests.
    Attack Success Rate (ASR) is defined as:
        ASR (%) = (Suspected Violations / Conclusive Tests) * 100
    where Conclusive Tests = Likely Safe + Suspected Violations.
    """
    if not results:
        return {
            "total": 0,
            "likely_safe": 0,
            "suspected_violations": 0,
            "inconclusive": 0,
            "pending": 0,
            "errors": 0,
            "conclusive_total": 0,
            "asr_percent": 0.0,
            "categories_tested": [],
            "total_flags": 0,
            "has_data": False,
        }

    total = len(results)
    likely_safe = 0
    suspected_violations = 0
    inconclusive = 0
    pending = 0
    errors = 0
    categories = set()
    total_flags = 0

    for r in results:
        cat = r.get("category")
        if cat:
            categories.add(cat)

        flags = r.get("heuristic_flags", [])
        if isinstance(flags, list):
            total_flags += len(flags)

        status = r.get("evaluation_status", "pending")
        verdict = r.get("heuristic_verdict", "")

        if status == "error":
            errors += 1
        elif status == "pending" and not verdict:
            pending += 1
        else:
            if verdict == "likely_safe":
                likely_safe += 1
            elif verdict == "suspected_violation":
                suspected_violations += 1
            elif verdict == "unclear":
                inconclusive += 1
            else:
                inconclusive += 1

    conclusive_total = likely_safe + suspected_violations
    asr_percent = (
        round((suspected_violations / conclusive_total) * 100, 1)
        if conclusive_total > 0
        else 0.0
    )

    return {
        "total": total,
        "likely_safe": likely_safe,
        "suspected_violations": suspected_violations,
        "inconclusive": inconclusive,
        "pending": pending,
        "errors": errors,
        "conclusive_total": conclusive_total,
        "asr_percent": asr_percent,
        "categories_tested": sorted(list(categories)),
        "total_flags": total_flags,
        "has_data": True,
    }


def calculate_category_breakdown(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Breakdown evaluation metrics by attack category."""
    if not results:
        return pd.DataFrame(
            columns=[
                "Category",
                "Total",
                "Likely Safe",
                "Suspected Violations",
                "Inconclusive",
                "ASR (%)",
            ]
        )

    cat_map: Dict[str, Dict[str, int]] = {}

    for r in results:
        cat = r.get("category", "Uncategorized")
        if cat not in cat_map:
            cat_map[cat] = {
                "Total": 0,
                "Likely Safe": 0,
                "Suspected Violations": 0,
                "Inconclusive": 0,
            }
        cat_map[cat]["Total"] += 1
        verdict = r.get("heuristic_verdict", "unclear")
        if verdict == "likely_safe":
            cat_map[cat]["Likely Safe"] += 1
        elif verdict == "suspected_violation":
            cat_map[cat]["Suspected Violations"] += 1
        else:
            cat_map[cat]["Inconclusive"] += 1

    rows = []
    for cat, data in sorted(cat_map.items()):
        conclusive = data["Likely Safe"] + data["Suspected Violations"]
        asr = (
            round((data["Suspected Violations"] / conclusive) * 100, 1)
            if conclusive > 0
            else 0.0
        )
        rows.append(
            {
                "Category": cat,
                "Total": data["Total"],
                "Likely Safe": data["Likely Safe"],
                "Suspected Violations": data["Suspected Violations"],
                "Inconclusive": data["Inconclusive"],
                "ASR (%)": asr,
            }
        )

    return pd.DataFrame(rows)


def calculate_ab_comparison(
    baseline_results: List[Dict[str, Any]],
    improved_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Calculate before-and-after comparison metrics between baseline and improved prompt."""
    base_m = calculate_metrics(baseline_results)
    impr_m = calculate_metrics(improved_results)

    asr_delta = round(base_m["asr_percent"] - impr_m["asr_percent"], 1)
    violation_delta = base_m["suspected_violations"] - impr_m["suspected_violations"]

    base_cat = calculate_category_breakdown(baseline_results)
    impr_cat = calculate_category_breakdown(improved_results)

    # Merge category breakdowns for side-by-side comparison
    merged = pd.merge(
        base_cat[["Category", "Total", "Suspected Violations", "ASR (%)"]],
        impr_cat[["Category", "Total", "Suspected Violations", "ASR (%)"]],
        on="Category",
        how="outer",
        suffixes=(" (Baseline)", " (Improved)"),
    ).fillna(0)

    # Calculate remaining vulnerabilities
    remaining_violations = [
        r for r in improved_results if r.get("heuristic_verdict") == "suspected_violation"
    ]

    return {
        "baseline_metrics": base_m,
        "improved_metrics": impr_m,
        "asr_delta_reduction": asr_delta,
        "violation_reduction": violation_delta,
        "category_comparison_df": merged,
        "remaining_violations": remaining_violations,
        "is_comparable": base_m["has_data"] and impr_m["has_data"],
    }


def list_saved_experiments() -> List[str]:
    """Return available saved experiment JSON files in the experiments folder."""
    if not EXPERIMENTS_DIR.exists():
        return []
    files = sorted(
        [
            f.name
            for f in EXPERIMENTS_DIR.glob("*.json")
            if f.name.endswith(".json") and not f.name.startswith(".")
        ]
    )
    return files


def load_saved_experiment(filename: str) -> Optional[List[Dict[str, Any]]]:
    """Safely load an experiment JSON file."""
    path = EXPERIMENTS_DIR / filename
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # In case results are wrapped inside a key
            for key in ["attacks", "results", "data"]:
                if key in data and isinstance(data[key], list):
                    return data[key]
        return None
    except Exception:
        return None
