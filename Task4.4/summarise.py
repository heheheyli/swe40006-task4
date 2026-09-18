#!/usr/bin/env python3
"""Summarise a CSV file: row/column counts and stats for numeric columns.

Usage:
    python summarise.py <input.csv> [output.txt]

Reads the CSV, prints a summary to the console, and writes the same summary
to a text file (default: summary.txt) next to the input.
"""

import csv
import statistics
import sys
from pathlib import Path


def summarise(rows: list[dict], headers: list[str]) -> list[str]:
    lines = []
    lines.append(f"Rows: {len(rows)}")
    lines.append(f"Columns: {len(headers)} ({', '.join(headers)})")
    lines.append("")

    for col in headers:
        values = [r[col] for r in rows if r[col] not in ("", None)]
        # Try to treat the column as numeric.
        nums = []
        for v in values:
            try:
                nums.append(float(v))
            except ValueError:
                nums = []
                break

        if nums:
            lines.append(f"[{col}] numeric")
            lines.append(f"    count : {len(nums)}")
            lines.append(f"    min   : {min(nums):g}")
            lines.append(f"    max   : {max(nums):g}")
            lines.append(f"    mean  : {statistics.mean(nums):.2f}")
        else:
            uniques = len(set(values))
            lines.append(f"[{col}] text - {len(values)} values, {uniques} unique")
        lines.append("")

    return lines


def main() -> int:
    if len(sys.argv) < 2:
        print("Error: no input file given.")
        print("Usage: python summarise.py <input.csv> [output.txt]")
        return 1

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else in_path.with_name("summary.txt")

    if not in_path.exists():
        print(f"Error: file not found: {in_path}")
        return 1

    print(f"Reading: {in_path}")
    with in_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    if not headers:
        print("Error: the CSV has no header row.")
        return 1

    report = summarise(rows, headers)

    print("-" * 40)
    for line in report:
        print(line)
    print("-" * 40)

    out_path.write_text("\n".join(report), encoding="utf-8")
    print(f"Summary written to: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
