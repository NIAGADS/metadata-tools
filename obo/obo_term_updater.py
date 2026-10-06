#!/usr/bin/env python3
"""Append or update terms in an OBO file.

Bare-bones standalone utility for managing an OBO dictionary.

Expected JSON input can be either a single term object or a list of term objects.
Each object accepts optional id, name, def, optional synonyms, and optional is_a
term/curie pairs.

If the incoming term matches an existing id or name in the OBO file, the script
prints a warning and exits.


Examples:
    ./obo_term_updater.py --terms /path/to/terms.json --obo /path/to/niagads.obo

    /path/to/terms.json contents:
        {
            "name": "sequencing center",
            "def": "The laboratory or facility responsible for generating sequencing data.",
            "is_a": [{"term": "covariate specification", "curie": "OBCS:0000040"}]
        }

    /path/to/term_list.json contents:
        [
          {
                "id": "OTHER:0000068",
                "name": "sequencing center",
                "def": "The laboratory or facility responsible for generating sequencing data.",
                "synonyms": ["seq center"],
                "is_a": [{"term": "covariate specification", "curie": "OBCS:0000040"}]
            },
            {
                "name": "technical variables",
                "def": "Variables describing technical aspects of data generation, processing, or quality control.",
                "is_a": [{"term": "covariate specification", "curie": "OBCS:0000040"}]
                }
        ]
"""

import argparse
import json
from logging import warning
import re
from pathlib import Path
import shutil
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class IsAItem(BaseModel):
    term: str
    curie: str


class Term(BaseModel):
    id: Optional[str] = None
    name: str
    def_: str = Field(..., alias="def")
    synonyms: list[str] = Field(default_factory=list)
    is_a: list[IsAItem] = Field(default_factory=list)

    # because of the def_ (def is a reserve word)
    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    def from_block(cls, block: str):
        data = {"id": None, "name": None, "def": None, "synonyms": [], "is_a": []}
        for line in block.splitlines():
            if not line.strip():
                continue
            if line.startswith("id:"):
                data["id"] = line.split(":", 1)[1].strip()
            elif line.startswith("name:"):
                data["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("def:"):
                value = line.split(":", 1)[1].strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                data["def"] = value
            elif line.startswith("synonym:"):
                match = re.search(r'"(.*?)"', line)
                if match:
                    data["synonyms"].append(match.group(1))
            elif line.startswith("is_a:"):
                match = re.match(r"is_a:\s*(\S+)\s*!\s*(.*)$", line)
                if match:
                    data["is_a"].append(
                        {"curie": match.group(1), "term": match.group(2).strip()}
                    )
        return cls(**data)


class OBOUpdater:
    def __init__(self, term_file: str, obo_file: str):
        self._term_file_path = Path(term_file)
        self._obo_file_path = Path(obo_file)
        if not self._term_file_path.exists():
            raise FileNotFoundError(f"Term file not found: {term_file}")
        if not self._obo_file_path.exists():
            raise FileNotFoundError(f"OBO file not found: {obo_file}")

        self._next_id = 0
        self._indexed_terms = {}
        self._terms = []

    def _parse_obo(self):
        text = self._obo_file_path.read_text(encoding="utf-8")
        self._obo_file_metadata = (
            text[: text.index("[Term]")] if "[Term]" in text else ""
        )

        blocks = re.findall(r"\[Term\].*?(?=\n\[Term\]|\Z)", text, flags=re.S)
        self._indexed_terms = {}
        for block in blocks:
            term = Term.from_block(block)
            if term.id and term.id.startswith("NIAGADS"):
                id_num = int(term.id.split(":")[-1])
                if self._next_id < id_num:
                    self._next_id = id_num

            self._terms.append(term)
            if term.id:
                self._indexed_terms[f"id|{term.id}"] = term.id
            if term.name:
                self._indexed_terms[f"name|{term.name}"] = term.name

            self._next_id += 1

    def _exists(self, term: Term):
        if f"name|{term.name}" in self._indexed_terms:
            return True
        if term.id and f"id|{term.id}" in self._indexed_terms:
            return True

        return False

    def _next_term_id(self) -> str:
        term_id = f"NIAGADS:{self._next_id:07d}"
        self._next_id += 1
        return term_id

    def _render_term(self, term: Term) -> str:
        def_text = term.def_ or ""
        lines = ["[Term]", f"id: {term.id}", f"name: {term.name}"]
        if def_text:
            lines.append(f'def: "{def_text}"')
        for synonym in term.synonyms:
            lines.append(f'synonym: "{synonym}" EXACT []')
        for rel in term.is_a:
            lines.append(f"is_a: {rel.curie} ! {rel.term}")
        return "\n".join(lines) + "\n\n"

    def _load_candidate_terms(self):
        payload = json.loads(self._term_file_path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return [Term(**item) for item in payload]
        else:
            return [Term(**payload)]

    def _update(self):
        candidate_terms = self._load_candidate_terms()
        for term in candidate_terms:
            if self._exists(term):
                existing_term_key = f"{term.name}|{term.id or ''}"
                warning(
                    f"{existing_term_key} already exists in "
                    f"{self._obo_file_path}. SKIPPING. Please revise directly.",
                )
                continue
            term.id = term.id or self._next_term_id()
            self._terms.append(term)

    def run(self):
        self._parse_obo()
        self._update()
        rendered_terms = [self._render_term(t) for t in self._terms]
        shutil.copy(self._obo_file_path, self._obo_file_path.with_suffix(".obo.bak"))
        self._obo_file_path.write_text(
            self._obo_file_metadata + "".join(rendered_terms), encoding="utf-8"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append or update a term in an OBO file."
    )
    parser.add_argument("--terms", required=True, help="Path to the term JSON file.")
    parser.add_argument("--obo", required=True, help="Path to the OBO file to update.")

    args = parser.parse_args()
    updater = OBOUpdater(args.terms, args.obo)
    updater.run()


if __name__ == "__main__":
    raise SystemExit(main())
