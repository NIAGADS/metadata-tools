#!/usr/bin/env python3
"""Print accession/MeSH-term pairs from NIAGADS study or dataset records.

Usage:
    python dss_fetch_pubmed_mesh.py study --email you@example.org > out.txt
    python dss_fetch_pubmed_mesh.py dataset --email you@example.org > out.txt

Output is tab-delimited on stdout, with columns: accession, mesh_term, and
curie.

Code generated with assistance from ChatGPT (OpenAI); reviewed and validated by NIAGADS.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from itertools import islice
from typing import Iterator
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

WP_API_URL = "https://dss.niagads.org/wp-json/wp/v2/"
EUTILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
WP_PAGE_SIZE = 100
PUBMED_BATCH_SIZE = 200
PUBMED_REQUEST_DELAY_SECONDS = 0.34


def batched(values: list[str], batch_size: int) -> Iterator[list[str]]:
    iterator = iter(values)
    while batch := list(islice(iterator, batch_size)):
        yield batch


def fetch_json(url: str) -> object:
    try:
        with urlopen(url, timeout=60) as response:
            return json.load(response)
    except HTTPError as error:
        body = error.read().decode("utf-8")
        try:
            return json.loads(body)
        except json.JSONDecodeError as parse_error:
            raise RuntimeError(f"Request failed ({error.code}): {url}") from parse_error


def get_accession_pmids(content_type: str) -> dict[str, list[str]]:
    accession_pmids: dict[str, list[str]] = {}
    page = 1

    while True:
        url = (
            f"{WP_API_URL}{content_type}?"
            f"{urlencode({'per_page': WP_PAGE_SIZE, 'page': page})}"
        )
        response = fetch_json(url)

        if isinstance(response, dict):
            if response.get("code") == "rest_post_invalid_page_number":
                break
            raise RuntimeError(
                f"WordPress API request failed on page {page}: "
                f"{response.get('message', response)}"
            )

        if not isinstance(response, list):
            raise RuntimeError(f"Unexpected WordPress API response on page {page}.")

        for record in response:
            accession = record.get("slug")
            pubmed_id_text = record.get("acf", {}).get(
                "related_publications_pubmed_ids", ""
            )
            pmids = list(dict.fromkeys(re.findall(r"\d+", pubmed_id_text)))

            if accession and pmids:
                accession_pmids[accession] = pmids

        page += 1

    return accession_pmids


def get_mesh_terms(
    pmids: list[str], email: str | None, api_key: str | None
) -> dict[str, list[tuple[str, str]]]:
    params = {
        "db": "pubmed",
        "retmode": "xml",
        "id": ",".join(pmids),
        "tool": "niagads_publication_mesh_export",
    }
    if email:
        params["email"] = email
    if api_key:
        params["api_key"] = api_key

    with urlopen(f"{EUTILS_URL}?{urlencode(params)}", timeout=60) as response:
        root = ET.parse(response).getroot()

    mesh_by_pmid: dict[str, list[tuple[str, str]]] = {}
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext("./MedlineCitation/PMID")
        if pmid:
            mesh_by_pmid[pmid] = [
                (descriptor.text.strip(), f"MeSH:{descriptor.attrib['UI']}")
                for descriptor in article.findall(
                    "./MedlineCitation/MeshHeadingList/MeshHeading/DescriptorName"
                )
                if descriptor.text
                and descriptor.text.strip()
                and descriptor.attrib.get("UI")
            ]

    return mesh_by_pmid


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print NIAGADS accession/MeSH-term pairs as TSV."
    )
    parser.add_argument(
        "content_type",
        choices=("study", "dataset"),
        help="NIAGADS WordPress endpoint to query",
    )
    parser.add_argument("--email", help="Email address supplied to NCBI (recommended)")
    parser.add_argument("--api-key", help="NCBI API key; increases request limits")
    args = parser.parse_args()

    accession_pmids = get_accession_pmids(args.content_type)
    all_pmids = list(
        dict.fromkeys(pmid for pmids in accession_pmids.values() for pmid in pmids)
    )

    mesh_by_pmid: dict[str, list[tuple[str, str]]] = {}
    for batch_number, pmid_batch in enumerate(batched(all_pmids, PUBMED_BATCH_SIZE)):
        mesh_by_pmid.update(get_mesh_terms(pmid_batch, args.email, args.api_key))
        if (batch_number + 1) * PUBMED_BATCH_SIZE < len(all_pmids):
            time.sleep(PUBMED_REQUEST_DELAY_SECONDS)

    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(["accession", "mesh_term", "curie"])

    for accession, pmids in accession_pmids.items():
        terms = dict.fromkeys(
            term_and_curie
            for pmid in pmids
            for term_and_curie in mesh_by_pmid.get(pmid, [])
        )
        for term, curie in terms:
            writer.writerow([accession, term, curie])


if __name__ == "__main__":
    main()
