"""Student record checker and report generator.

This script reads a CSV file containing student names, marks, and email
addresses, then:

1. Finds students with marks below 12.
2. Validates email addresses using a regular expression.
3. Prints the result in the terminal.
4. Writes a human-readable report.txt file.

It uses both the built-in csv module and pandas so the task demonstrates
the file-handling and reporting workflow requested in Lab-10.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    pd = None


EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def parse_arguments() -> argparse.Namespace:
    """Return command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Check student marks and email addresses from a CSV file."
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        default="students.csv",
        help="Path to the CSV file with name, marks, and email columns.",
    )
    parser.add_argument(
        "--report",
        default="report.txt",
        help="Output path for the generated report file.",
    )
    return parser.parse_args()


def load_students(csv_path: Path) -> list[dict[str, object]]:
    """Load student records from a CSV file using csv.DictReader."""

    records: list[dict[str, object]] = []

    with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            raise ValueError("The CSV file is empty.")

        header_map = {header.strip().lower(): header for header in reader.fieldnames}
        required_headers = {"name", "marks", "email"}
        if not required_headers.issubset(header_map):
            raise ValueError(
                "CSV file must contain the columns: name, marks, email."
            )

        name_header = header_map["name"]
        marks_header = header_map["marks"]
        email_header = header_map["email"]

        for row in reader:
            name = row.get(name_header, "").strip()
            marks_text = row.get(marks_header, "").strip()
            email = row.get(email_header, "").strip()

            try:
                marks = float(marks_text)
            except ValueError:
                marks = float("nan")

            records.append({"name": name, "marks": marks, "email": email})

    return records


def is_valid_email(email: str) -> bool:
    """Check whether an email address matches the expected pattern."""

    return bool(EMAIL_PATTERN.fullmatch(email))


def build_report(records: list[dict[str, object]]) -> str:
    """Create the report text using pandas for tabular summaries."""

    if not records:
        return "No student records found."

    if pd is not None:
        dataframe = pd.DataFrame(records)
        dataframe["valid_email"] = dataframe["email"].astype(str).apply(is_valid_email)
        dataframe["low_mark"] = dataframe["marks"].astype(float) < 12

        total_students = len(dataframe)
        low_mark_count = int(dataframe["low_mark"].sum())
        invalid_email_count = int((~dataframe["valid_email"]).sum())

        row_source = dataframe.to_dict(orient="records")
    else:
        analyzed_rows = []
        for record in records:
            analyzed_rows.append(
                {
                    "name": record["name"],
                    "marks": record["marks"],
                    "email": record["email"],
                    "valid_email": is_valid_email(str(record["email"])),
                    "low_mark": float(record["marks"]) < 12,
                }
            )

        low_mark_rows = [row for row in analyzed_rows if row["low_mark"]]
        invalid_email_rows = [row for row in analyzed_rows if not row["valid_email"]]

        total_students = len(analyzed_rows)
        low_mark_count = len(low_mark_rows)
        invalid_email_count = len(invalid_email_rows)

        row_source = analyzed_rows

    low_mark_rows = [row for row in row_source if row["low_mark"]]
    invalid_email_rows = [row for row in row_source if not row["valid_email"]]
    low_mark_table = format_rows(low_mark_rows)
    invalid_email_table = format_rows(invalid_email_rows)

    summary_rows = [
        ["Total students", total_students],
        ["Marks below 12", low_mark_count],
        ["Invalid emails", invalid_email_count],
    ]

    validation_rows = []
    for row in row_source:
        status_mark = "LOW MARK" if row["low_mark"] else "OK"
        status_email = "VALID EMAIL" if row["valid_email"] else "INVALID EMAIL"
        validation_rows.append(
            [row["name"], f"{row['marks']}", row["email"], status_mark, status_email]
        )

    report_lines = [
        *format_banner("STUDENT RECORD CHECK REPORT"),
        "",
        *format_section("Summary", format_key_value_table(summary_rows)),
        "",
        *format_section(
            "Students scoring below 12",
            low_mark_table if low_mark_table != "None" else "None",
        ),
        "",
        *format_section(
            "Students with invalid email addresses",
            invalid_email_table if invalid_email_table != "None" else "None",
        ),
        "",
        *format_section(
            "Validation details",
            format_table(
                validation_rows,
                ["Name", "Marks", "Email", "Mark Status", "Email Status"],
            ),
        ),
    ]

    return "\n".join(report_lines)


def format_rows(rows: list[dict[str, object]]) -> str:
    """Format rows into a compact fixed-width table without pandas."""

    return format_table(
        [[str(row["name"]), str(row["marks"]), str(row["email"])] for row in rows],
        ["Name", "Marks", "Email"],
    )


def format_banner(title: str) -> list[str]:
    """Return a boxed banner for the report title."""

    width = max(len(title) + 4, 62)
    border = "+" + "-" * (width - 2) + "+"
    centered_title = f"| {title.center(width - 4)} |"
    return [border, centered_title, border]


def format_section(title: str, body: str) -> list[str]:
    """Format a named section with an ASCII divider."""

    return [
        title,
        "-" * len(title),
        body,
    ]


def format_key_value_table(rows: list[list[object]]) -> str:
    """Format summary key-value rows."""

    header = ["Metric", "Value"]
    return format_table(rows, header)


def format_table(rows: list[list[object]], headers: list[str]) -> str:
    """Format rows into a compact fixed-width table."""

    if not rows:
        return "None"

    string_rows = [[str(value) for value in row] for row in rows]
    widths = [len(header) for header in headers]

    for row in string_rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
    header_line = "|" + "|".join(
        f" {header.ljust(widths[index])} " for index, header in enumerate(headers)
    ) + "|"
    data_lines = [
        "|"
        + "|".join(f" {value.ljust(widths[index])} " for index, value in enumerate(row))
        + "|"
        for row in string_rows
    ]
    return "\n".join([border, header_line, border, *data_lines, border])


def save_report(report_text: str, report_path: Path) -> None:
    """Write the report to disk."""

    with report_path.open("w", encoding="utf-8") as report_file:
        report_file.write(report_text)
        report_file.write("\n")


def main() -> None:
    """Run the student checker workflow."""

    args = parse_arguments()
    csv_path = Path(args.csv_file)
    report_path = Path(args.report)

    records = load_students(csv_path)
    report_text = build_report(records)
    save_report(report_text, report_path)

    print("Generating student record report...")
    print(f"Source CSV : {csv_path.resolve()}")
    print(f"Report file: {report_path.resolve()}")
    print()
    print(report_text)
    print()
    print("Done: report generated successfully.")


if __name__ == "__main__":
    main()