import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
records = json.loads((root / "students.json").read_text(encoding="utf-8"))
assert isinstance(records, list), "students.json must contain a list"
seen = set()
for number, record in enumerate(records, 1):
    assert isinstance(record, dict), f"Record {number} must be an object"
    civil_id = record.get("civil_id")
    assert isinstance(civil_id, str) and re.fullmatch(r"[0-9]+", civil_id), f"Invalid civil ID in record {number}"
    assert civil_id not in seen, f"Duplicate civil ID in record {number}"
    seen.add(civil_id)
    for field in ("student_name", "grade", "class"):
        assert isinstance(record.get(field), str) and record[field].strip(), f"Missing {field} in record {number}"
    pdf = record.get("pdf", "")
    if pdf and pdf != "#":
        assert isinstance(pdf, str) and re.fullmatch(r"pdfs/[a-zA-Z0-9/_-]+\.pdf", pdf), f"Invalid PDF path in record {number}"
        assert (root / pdf).is_file(), f"Missing PDF in record {number}"
        assert (root / pdf).read_bytes().startswith(b"%PDF-"), f"Invalid PDF file in record {number}"
print(f"Validated {len(records)} student records.")
