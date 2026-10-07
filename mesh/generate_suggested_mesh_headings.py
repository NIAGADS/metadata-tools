#!/usr/bin/env python3
"""Generate the suggested MeSH headings support page from retained terms."""

from __future__ import annotations

import argparse
import csv
import html
import re
from pathlib import Path


DEFAULT_DIRECTORY = Path(__file__).parent
DEFAULT_INPUT = DEFAULT_DIRECTORY / "MeSH-retained-terms.txt"
DEFAULT_OUTPUT = DEFAULT_DIRECTORY / "suggested-MeSH-headings.html"


def read_terms(input_path: Path) -> list[dict[str, str]]:
    """Read retained MeSH headings from a tab-delimited file."""
    with input_path.open(newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file, delimiter="\t")
        if reader.fieldnames != ["mesh_term", "curie"]:
            raise ValueError(
                f"Expected mesh_term and curie columns in {input_path}."
            )

        terms = list(reader)

    if any(not row["mesh_term"] or not row["curie"] for row in terms):
        raise ValueError(f"Empty MeSH term or CURIE found in {input_path}.")

    return terms


def render_rows(terms: list[dict[str, str]]) -> str:
    """Render retained MeSH headings as an HTML table body."""
    rows = []
    for row in terms:
        term = html.escape(row["mesh_term"])
        curie = html.escape(row["curie"])
        mesh_id = html.escape(row["curie"].split(":", 1)[-1], quote=True)
        rows.append(
            "<tr>"
            f"<td>{term}</td>"
            '<td class="curie">'
            f'<a href="https://www.ncbi.nlm.nih.gov/mesh/{mesh_id}" '
            'target="_blank" rel="noopener noreferrer">'
            f"{curie}</a></td></tr>"
        )

    return "".join(rows)


def generate_page(input_path: Path, output_path: Path) -> None:
    """Generate the support page using the existing HTML as a template."""
    terms = read_terms(input_path)
    page = re.sub(r"\s+", " ", output_path.read_text(encoding="utf-8")).strip()
    table_start = page.index("<tbody>") + len("<tbody>")
    table_end = page.index("</tbody>", table_start)
    page = page[:table_start] + render_rows(terms) + page[table_end:]
    page = page.replace(
        "257 of 257 headings",
        f"{len(terms)} of {len(terms)} headings",
    )
    output_path.write_text(page, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the suggested MeSH headings HTML page."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Retained MeSH terms TSV file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Suggested headings HTML file.",
    )
    args = parser.parse_args()
    generate_page(args.input, args.output)


if __name__ == "__main__":
    main()
