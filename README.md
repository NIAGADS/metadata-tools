# NIAGADS Ontology

This repository contains a lightweight, OBO-formatted ontology and data dictionary for NIAGADS resources. The canonical source is the ontology file in [obo/niagads.obo](obo/niagads.obo), with term maintenance handled by [obo/obo_term_updater.py](obo/obo_term_updater.py).

## Project purpose

The ontology provides controlled vocabulary for NIAGADS metadata, genomic annotations, and domain-specific concepts such as variant annotation, GWAS summary statistics, and disease-related staging terms. It is designed to support consistent labeling across genomic and data dictionary workflows without requiring a full external ontology dependency.

## Repository contents

- [obo/niagads.obo](obo/niagads.obo): the OBO ontology data file
- [obo/obo_term_updater.py](obo/obo_term_updater.py): command-line script for adding or updating ontology terms from JSON input
- [LICENSE](LICENSE): project license

## Updating the ontology

The updater script accepts either a single term object or a list of term objects in JSON format and appends valid new entries to the ontology.

Example usage:

```bash
python obo/obo_term_updater.py \
  --terms /path/to/terms.json \
  --obo obo/niagads.obo
```

The script:

- validates the input term schema
- checks for duplicate `id` or `name` values already present in the OBO file
- creates a backup before writing changes
- appends new `[Term]` blocks with generated `NIAGADS:` IDs when needed

## JSON term format

```json
{
  "name": "sequencing center",
  "def": "The laboratory or facility responsible for generating sequencing data.",
  "synonyms": ["seq center"],
  "is_a": [
    {"term": "covariate specification", "curie": "OBCS:0000040"}
  ]
}
```

A list of term objects is also accepted.

## Notes

This repository is intentionally minimal and focused on maintaining the ontology dictionary itself. It is best used as a source of controlled terms for NIAGADS data resources and downstream ETL or schema tooling.
