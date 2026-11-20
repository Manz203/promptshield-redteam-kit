
import csv
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "experiments" / "quality_review.csv"

scores = {
    ("v1", "attack1"): (5, 2, 1, 4),
    ("v1", "attack2"): (5, 3, 2, 4),
    ("v1", "attack3"): (5, 4, 2, 5),
    ("v1", "attack4"): (5, 2, 2, 4),
    ("v1", "attack5"): (5, 4, 3, 4),
    ("v2", "attack1"): (5, 3, 3, 5),
    ("v2", "attack2"): (5, 3, 4, 5),
    ("v2", "attack3"): (2, 5, 2, 2),
    ("v2", "attack4"): (5, 4, 4, 5),
    ("v2", "attack5"): (4, 4, 3, 2),    
    ("v3", "attack-1"): (4, 2, 1, 4),
    ("v3", "attack-2"): (3, 3, 3, 3),
    ("v3", "attack-3"): (3, 4, 2, 3),
    ("v3", "attack-4"): (5, 4, 3, 4),
    ("v3", "attack-5"): (5, 4, 4, 4),
}

with path.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f, delimiter="\t")
    fieldnames = reader.fieldnames
    rows = list(reader)

columns = [
    "relevance_1_to_5",
    "realism_1_to_5",
    "creativity_1_to_5",
    "expected_behavior_1_to_5",
]

for row in rows:
    key = (row["version"].strip(), row["attack_id"].strip())
    if key in scores:
        for column, score in zip(columns, scores[key]):
            row[column] = score
        row["review_notes"] = "Suggested score - pending human review"

with path.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

print("Suggested scores filled successfully!")
print("Review and adjust scores before finalizing.")