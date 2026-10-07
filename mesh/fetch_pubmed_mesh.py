#!/usr/bin/env python3
"""Fetch MeSH terms for PubMed IDs using NCBI E-utilities.

Usage:
    python fetch_pubmed_mesh.py pubmed_ids.txt pubmed_mesh.tsv

The input may contain one PMID per line, or a comma/whitespace-delimited list.
The output is a TSV with columns: pubmed_id and mesh_terms. MeSH terms are
separated by " // ".
"""

from __future__ import annotations

import argparse
import csv
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


EUTILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH_SIZE = 200
REQUEST_DELAY_SECONDS = 0.34


def read_pmids(path: Path) -> list[str]:
    """Read PMIDs, preserving order and dropping duplicates."""
    values = path.read_text(encoding="utf-8").replace(",", " ").split()
    pmids: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not value.isdigit():
            raise ValueError(f"Invalid PubMed ID: {value!r}")
        if value not in seen:
            pmids.append(value)
            seen.add(value)
    return pmids


def fetch_mesh_terms(
    pmids: list[str], email: str | None, api_key: str | None
) -> dict[str, list[str]]:
    params = {"db": "pubmed", "retmode": "xml", "id": ",".join(pmids)}
    if email:
        params["email"] = email
    if api_key:
        params["api_key"] = api_key

    with urlopen(f"{EUTILS_URL}?{urlencode(params)}", timeout=60) as response:
        root = ET.parse(response).getroot()

    results: dict[str, list[str]] = {}
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext("./MedlineCitation/PMID")
        if not pmid:
            continue
        terms = [
            descriptor.text.strip()
            for descriptor in article.findall(
                "./MedlineCitation/MeshHeadingList/MeshHeading/DescriptorName"
            )
            if descriptor.text and descriptor.text.strip()
        ]
        results[pmid] = terms
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch PubMed MeSH terms into a TSV file."
    )
    parser.add_argument("input_file", type=Path, help="Text file containing PubMed IDs")
    parser.add_argument("output_file", type=Path, help="Output TSV file")
    parser.add_argument("--email", help="Email address supplied to NCBI (recommended)")
    parser.add_argument("--api-key", help="NCBI API key; increases request limits")
    args = parser.parse_args()

    pmids = read_pmids(args.input_file)
    with args.output_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["pubmed_id", "mesh_terms"])
        for index in range(0, len(pmids), BATCH_SIZE):
            batch = pmids[index : index + BATCH_SIZE]
            mesh_by_pmid = fetch_mesh_terms(batch, args.email, args.api_key)
            for pmid in batch:
                writer.writerow([pmid, " // ".join(mesh_by_pmid.get(pmid, []))])
            if index + BATCH_SIZE < len(pmids):
                time.sleep(REQUEST_DELAY_SECONDS)


if __name__ == "__main__":
    main()
