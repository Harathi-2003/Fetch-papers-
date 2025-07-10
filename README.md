# 🔍 PubMed Paper Fetcher

A Python command-line tool to fetch PubMed research papers based on user queries, and identify papers with **at least one author affiliated with a pharmaceutical or biotech company**.

The program uses the **PubMed API**, supports full PubMed query syntax, and outputs results as a CSV file with detailed metadata.

---

## 🚀 Features

- ✅ Full PubMed query support
- ✅ Filters for **non-academic** authors (e.g., company affiliations)
- ✅ Outputs data with:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic Author(s)
  - Company Affiliation(s)
  - Corresponding Author Email
- ✅ Command-line interface with:
  - `-h`, `--help` – Show usage instructions
  - `-d`, `--debug` – Show debug info
  - `-f`, `--file` – Save results to a CSV file
- ✅ Modular architecture: module + CLI
- ✅ Fully typed Python code
- ✅ Robust error handling
- ✅ Packaged with Poetry
- ✅ Bonus: Published module to [Visithere](https://rainbow-figolla-d190c9.netlify.app)

---

## 🧠 How it Works

The tool identifies **non-academic authors** using a heuristic:
- Affiliation strings are scanned for company-related keywords (e.g., *Inc.*, *Ltd.*, *Pharma*, *Biotech*)
- Emails not ending in `.edu`, `.ac`, or similar academic domains are also flagged

---

## 🗂️ Code Structure

```text
pubmed_paper_fetcher/
├── __init__.py
├── fetcher.py         # Core logic for fetching and filtering PubMed data
├── parser.py          # Heuristics for identifying company affiliations
├── writer.py          # CSV output writer
└── cli.py             # CLI logic using argparse
tests/
├── test_fetcher.py
└── test_parser.py
pyproject.toml         # Poetry config with dependencies and entrypoints
README.md
