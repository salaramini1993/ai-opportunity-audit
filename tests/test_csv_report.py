import csv
import io
import json

from aiaudit.cli import main
from aiaudit.csv_report import COLUMNS, render_csv
from aiaudit.scoring import score

SHOP = {"sells_products": True, "many_products": True, "multi_language": True}


def _rows(text):
    return list(csv.DictReader(io.StringIO(text)))


def test_empty_csv_has_only_header():
    text = render_csv([])
    assert text == ",".join(COLUMNS) + "\r\n"


def test_csv_rows_follow_priority_order():
    results = score(SHOP)
    rows = _rows(render_csv(results))
    assert len(rows) == len(results)
    assert [row["key"] for row in rows] == [r.opportunity.key for r in results]
    assert [row["rank"] for row in rows] == [str(i) for i in range(1, len(rows) + 1)]
    first, top = rows[0], results[0]
    assert first["title"] == top.opportunity.title
    assert first["quadrant"] == top.quadrant
    assert float(first["priority"]) == top.priority


def test_csv_hours_and_cost_columns():
    results = score(SHOP)
    for row, r in zip(_rows(render_csv(results)), results):
        if r.hours_saved is None:
            assert row["hours_saved_low"] == row["hours_saved_high"] == ""
        else:
            assert float(row["hours_saved_low"]) == r.hours_saved[0]
            assert float(row["hours_saved_high"]) == r.hours_saved[1]
        assert row["cost_per_month"] == (r.opportunity.cost_per_month or "")


def test_cli_writes_csv_file(tmp_path):
    answers = tmp_path / "answers.json"
    answers.write_text(json.dumps({"business_name": "Shop", "answers": SHOP}))
    out = tmp_path / "priorities.csv"
    assert main(["--answers", str(answers), "--format", "csv", "--out", str(out)]) == 0
    data = out.read_bytes().decode("utf-8")
    assert data.startswith("rank,key,title,")
    assert "\r\n" in data and "\r\r\n" not in data
    assert len(_rows(data)) == len(score(SHOP))
