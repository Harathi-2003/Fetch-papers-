### FILE: pubmed_paper_fetcher/fetcher.py

from typing import List, Dict
from Bio import Entrez
from .utils import is_non_academic_affiliation
import logging
import re

Entrez.email = "your-email@example.com"  # REQUIRED by NCBI


def fetch_pubmed_ids(query: str, retmax: int = 20) -> List[str]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]


def fetch_paper_details(pmid: str) -> Dict:
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml")
    record = Entrez.read(handle)
    handle.close()

    article = record["PubmedArticle"][0]
    medline = article["MedlineCitation"]
    article_data = medline["Article"]

    title = article_data.get("ArticleTitle", "")
    pub_date = article_data.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
    date_str = f"{pub_date.get('Year', '')}-{pub_date.get('Month', '')}-{pub_date.get('Day', '')}"

    authors = article_data.get("AuthorList", [])
    non_academic_authors = []
    company_affiliations = []
    corresponding_email = ""

    for author in authors:
        if "AffiliationInfo" in author:
            affiliations = author["AffiliationInfo"]
            for aff in affiliations:
                aff_text = aff.get("Affiliation", "")
                if is_non_academic_affiliation(aff_text):
                    fullname = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()
                    non_academic_authors.append(fullname)
                    company_affiliations.append(aff_text)
                    match = re.search(r"[\w\.-]+@[\w\.-]+", aff_text)
                    if match:
                        corresponding_email = match.group(0)

    return {
        "PubmedID": pmid,
        "Title": title,
        "Publication Date": date_str,
        "Non-academic Author(s)": ", ".join(set(non_academic_authors)),
        "Company Affiliation(s)": ", ".join(set(company_affiliations)),
        "Corresponding Author Email": corresponding_email
    }


def fetch_papers(query: str, debug: bool = False) -> List[Dict]:
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info(f"Fetching PubMed IDs for query: {query}")
    pmids = fetch_pubmed_ids(query)
    logging.debug(f"Found PubMed IDs: {pmids}")

    papers = []
    for pmid in pmids:
        try:
            paper = fetch_paper_details(pmid)
            if paper["Non-academic Author(s)"]:
                papers.append(paper)
        except Exception as e:
            logging.error(f"Error fetching details for PMID {pmid}: {e}")
    return papers


### FILE: pubmed_paper_fetcher/utils.py

import re

def is_non_academic_affiliation(affiliation: str) -> bool:
    non_academic_keywords = [
        "pharma", "biotech", "inc", "ltd", "llc", "gmbh", "corp", "co", "industries",
        "solutions", "company", "laboratories", "lab", "research institute"
    ]
    academic_keywords = [
        "university", "college", "school", "institute of technology", "faculty",
        "dept", "department", "hospital", "center", "centre", "academy"
    ]
    aff = affiliation.lower()
    return any(k in aff for k in non_academic_keywords) and not any(k in aff for k in academic_keywords)


### FILE: cli.py

import argparse
import csv
from pubmed_paper_fetcher.fetcher import fetch_papers

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", type=str, help="PubMed query string")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results as CSV")
    args = parser.parse_args()

    papers = fetch_papers(args.query, debug=args.debug)

    if args.file:
        with open(args.file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "PubmedID", "Title", "Publication Date",
                "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
            writer.writeheader()
            for paper in papers:
                writer.writerow(paper)
        print(f"Saved results to {args.file}")
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()


### FILE: pyproject.toml

[tool.poetry]
name = "pubmed-paper-fetcher"
version = "0.1.0"
description = "Fetch PubMed papers with at least one non-academic author."
authors = ["Your Name <your-email@example.com>"]

[tool.poetry.dependencies]
python = ">=3.9"
biopython = "^1.83"

[tool.poetry.scripts]
get-papers-list = "cli:main"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"


### FILE: README.md

# PubMed Paper Fetcher

A command-line tool to fetch PubMed papers with at least one non-academic author (e.g., from pharmaceutical or biotech companies).

## 🔧 Features

- Fetches PubMed results using full query syntax.
- Filters papers with at least one non-academic author.
- Outputs results to CSV or console.
- Extracts:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic Author(s)
  - Company Affiliation(s)
  - Corresponding Author Email

## 🚀 Usage

```bash
poetry run get-papers-list "cancer immunotherapy" --file results.csv
```

### Options

- `-h`, `--help`: Show help message
- `-d`, `--debug`: Print debug logs
- `-f`, `--file`: Specify CSV output file name

## 📦 Setup

Install [Poetry](https://python-poetry.org/docs/#installation) and then run:

```bash
poetry install
poetry shell
```

## ▶️ Run Locally

```bash
poetry run get-papers-list "malaria vaccine"
```

## 📁 Project Structure

- `fetcher.py`: Core logic to fetch and parse PubMed results
- `utils.py`: Helper functions for filtering
- `cli.py`: Command-line interface entry point

## 🛠 Tools Used

- [Biopython](https://biopython.org/) - PubMed API integration
- [Poetry](https://python-poetry.org/) - Dependency management and packaging

## ✅ License

MIT License
