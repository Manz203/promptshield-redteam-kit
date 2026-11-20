
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = ROOT / "experiments"

REQUIRED_FIELDS = {
    "attack_id",
    "category",
    "attack_prompt",
    "expected_safe_behavior"
}

CATEGORIES = {
    "Instruction Override",
    "Role Spoofing",
    "System Prompt Extraction",
    "Fake Authority",
    "Context Manipulation"
}


def evaluate(version):
    file_path = EXPERIMENTS / f"attack_results_{version}.json"

    if not file_path.exists():
        print(f"{version}: File not found")
        return None

    with file_path.open(encoding="utf-8") as file:
        attacks = json.load(file)

    if not isinstance(attacks, list):
        raise ValueError(f"{version}: Expected a JSON array")

    total = len(attacks)

    valid = sum(
        isinstance(attack, dict)
        and REQUIRED_FIELDS.issubset(attack.keys())
        and all(
            isinstance(attack[field], str)
            and attack[field].strip()
            for field in REQUIRED_FIELDS
            if field in attack
        )
        for attack in attacks
    )

    categories = {
        attack.get("category")
        for attack in attacks
        if isinstance(attack, dict)
        and isinstance(attack.get("category"), str)
    }

    prompts = [
        attack["attack_prompt"].strip().lower()
        for attack in attacks
        if isinstance(attack, dict)
        and isinstance(attack.get("attack_prompt"), str)
    ]

    unique_prompts = len(set(prompts))

    return {
        "version": version,
        "total_attacks": total,
        "valid_attacks": valid,
        "category_coverage": len(categories & CATEGORIES),
        "unique_prompts": unique_prompts
    }


results = []

for version in ["v1", "v2", "v3"]:
    result = evaluate(version)

    if result is not None:
        results.append(result)

print("\nPROMPTSHIELD EVALUATION RESULTS")
print("-" * 65)

for result in results:
    print(
        f"{result['version'].upper()} | "
        f"Attacks: {result['total_attacks']} | "
        f"Valid: {result['valid_attacks']} | "
        f"Categories: {result['category_coverage']}/5 | "
        f"Unique: {result['unique_prompts']}"
    )

output_path = EXPERIMENTS / "evaluation_summary.json"

output_path.write_text(
    json.dumps(results, indent=2),
    encoding="utf-8"
)

print(f"\nEvaluation saved to: {output_path}")
