# Lab-10 Student Record Checker

## What it does

This program reads a CSV file with `name`, `marks`, and `email` columns, then:

1. Finds students with marks below 12.
2. Validates email addresses using a regular expression.
3. Prints the result in the terminal.
4. Writes a `report.txt` file with the full results.

## Concepts used

- File handling with `open()`
- CSV processing with `csv.DictReader`
- Data analysis and table formatting with `pandas`
- Email validation with `re`

If `pandas` is not installed, the script still works using a built-in
formatting fallback.

## How to run

```powershell
& "f:/BSE-6A/ML Learning/.venv/Scripts/python.exe" "f:/BSE-6A/ML Learning/Lab-10/Task-01.py" "f:/BSE-6A/ML Learning/Lab-10/students.csv" --report "f:/BSE-6A/ML Learning/Lab-10/report.txt"
```

## Output files

- `report.txt` contains the generated report.