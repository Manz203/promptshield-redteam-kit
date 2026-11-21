
"""Member 4: PromptShield Guardrail Recommendation Pipeline."""

import argparse
from pathlib import Path

from src.target_chatbot import DEFAULT_SYSTEM_PROMPT
from src.guardrail_recommender import recommend_from_file


def run_pipeline(results_path, output_path, system_prompt):
    """Generate an improved system prompt from attack test results."""

    result = recommend_from_file(
        results_path,
        system_prompt
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        result["improved_system_prompt"],
        encoding="utf-8"
    )

    print("\nPromptShield Member 4 Pipeline")
    print("--------------------------------")
    print("Input results:", results_path)
    print("Output prompt:", output_path)
    print("Total findings:", result["total_findings"])
    print("Total recommendations:", result["total_recommendations"])

    print("\nRecommendations:")
    for number, recommendation in enumerate(
        result["recommendations"], start=1
    ):
        print(f"{number}. {recommendation}")

    print("\nImproved system prompt saved successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate improved chatbot guardrails."
    )

    parser.add_argument(
        "--results",
        default="experiments/member4_original_results.json"
    )

    parser.add_argument(
        "--output",
        default="experiments/member4_pipeline_improved_prompt.txt"
    )

    parser.add_argument(
        "--system-prompt",
        default=DEFAULT_SYSTEM_PROMPT,
        help="Original system prompt to improve."
    )

    args = parser.parse_args()

    run_pipeline(
        args.results,
        args.output,
        args.system_prompt
    )
