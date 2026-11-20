
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = ROOT / "experiments"

output_path = EXPERIMENTS / "quality_review.csv"

with output_path.open("w", newline="", encoding="utf-8-sig") as output:
    writer = csv.writer(output)

    writer.writerow([
        "version",
        "attack_id",
        "category",
        "attack_prompt",
        "expected_safe_behavior",
        "relevance_1_to_5",
        "realism_1_to_5",
        "creativity_1_to_5",
        "expected_behavior_1_to_5",
        "review_notes"
    ])

    for version in ["v1", "v2", "v3"]:
        file_path = EXPERIMENTS / f"attack_results_{version}.json"

        with file_path.open(encoding="utf-8") as file:
            attacks = json.load(file)

        for attack in attacks:
            writer.writerow([
                version,
                attack["attack_id"],
                attack["category"],
                attack["attack_prompt"],
                attack["expected_safe_behavior"],
                "", "", "", "", ""
            ])

print("Quality review file created successfully!")
print(f"Saved to: {output_path}")
print("Total attacks prepared for review: 15")
