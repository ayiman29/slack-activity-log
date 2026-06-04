from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def parse_timestamp(value: str) -> datetime:
    timestamp_text = value.strip()
    timestamp_formats = (
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
    )

    for timestamp_format in timestamp_formats:
        try:
            return datetime.strptime(timestamp_text, timestamp_format)
        except ValueError:
            continue

    return datetime.fromisoformat(timestamp_text.replace("Z", "+00:00"))


def load_existing_timestamps(path: Path) -> set[str]:
    if not path.exists():
        return set()

    timestamps: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if not row:
                continue
            if row[0] == "timestamp":
                continue
            timestamps.add(row[0])

    return timestamps


def read_source_rows(source_path: Path) -> list[tuple[datetime, str, str]]:
    rows: list[tuple[datetime, str, str]] = []

    with source_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if not row or row[0] == "timestamp":
                continue
            if len(row) < 2:
                continue

            timestamp_text = row[0].strip()
            active_text = row[1].strip()
            timestamp = parse_timestamp(timestamp_text)
            rows.append((timestamp, timestamp_text, active_text))

    return rows


def split_log(source_path: Path, output_dir: Path) -> None:
    rows = read_source_rows(source_path)
    grouped_rows: dict[str, list[tuple[str, str]]] = defaultdict(list)

    for timestamp, timestamp_text, active_text in rows:
        date_key = timestamp.date().isoformat()
        grouped_rows[date_key].append((timestamp_text, active_text))

    output_dir.mkdir(parents=True, exist_ok=True)

    for date_key, date_rows in grouped_rows.items():
        output_path = output_dir / f"{date_key}.txt"
        existing_timestamps = load_existing_timestamps(output_path)
        is_new_file = not output_path.exists()

        new_rows = [
            (timestamp_text, active_text)
            for timestamp_text, active_text in date_rows
            if timestamp_text not in existing_timestamps
        ]

        if not new_rows and not is_new_file:
            continue

        with output_path.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            if is_new_file:
                writer.writerow(["timestamp", "active"])
            for timestamp_text, active_text in new_rows:
                writer.writerow([timestamp_text, active_text])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split slack_activity_log.txt into one file per date and append only new rows."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default="slack_activity_log.txt",
        help="Path to the combined Slack activity log.",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="logs",
        help="Directory where per-day log files will be written.",
    )
    args = parser.parse_args()

    split_log(Path(args.source), Path(args.output_dir))


if __name__ == "__main__":
    main()