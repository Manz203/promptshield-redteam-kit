
import csv
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
input_path = ROOT / "experiments" / "quality_review.csv"
output_path = ROOT / "experiments" / "quality_summary.json"

score_columns = [
    "relevance_1_to_5",
    "realism_1_to_5",
    "creativity_1_to_5",
    "expected_behavior_1_to_5",
]

with input_path.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f, delimiter="\t")
    rows = list(reader)

summary = {}

for version in ["v1", "v2", "v3"]:
    version_rows = [r for r in rows if r["version"].strip() == version]

    if len(version_rows) != 5:
        raise ValueError(f"{version}: Expected 5 attacks")

    for row in version_rows:
        for column in score_columns:
            value = row[column].strip()
            if not value or not value.isdigit() or not 1 <= int(value) <= 5:
                raise ValueError(
                    f"Invalid or missing score: {version}, "
                    f"{row['attack_id']}, {column}"
                )

    averages = {
        column: round(mean(int(r[column]) for r in version_rows), 2)
        for column in score_columns
    }

    totals = [
        sum(int(row[column]) for column in score_columns)
        for row in version_rows
    ]

    summary[version] = {
        "attack_count": len(version_rows),
        "average_total_out_of_20": round(mean(totals), 2),
        "dimension_averages": averages,
    }

output_path.write_text(
    json.dumps(summary, indent=2),
    encoding="utf-8"
)

for version, result in summary.items():
    print(
        f"{version.upper()} | "
        f"Attacks: {result['attack_count']} | "
        f"Average: {result['average_total_out_of_20']}/20"
    )

print(f"\nSummary saved to: {output_path}")
