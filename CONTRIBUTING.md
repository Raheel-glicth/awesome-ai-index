# Contributing to awesome-ai-index

Thank you for helping build the definitive open-source AI ecosystem database.

## Ways to Contribute

| Type | How |
|------|-----|
| Add a model | Open an issue using the **Add Model** template |
| Add a vendor | Open an issue using the **Add Vendor** template |
| Fix incorrect data | Open an issue using the **Data Correction** template |
| Improve docs | Submit a PR directly |
| Add a benchmark | Open an issue for discussion first |

## Before You Start

1. Check [existing issues](https://github.com/alpha-one-index/awesome-ai-index/issues) to avoid duplicates
2. Read [METHODOLOGY.md](METHODOLOGY.md) to understand our inclusion criteria
3. Ensure your data comes from a verifiable source

## Adding a Model

Add an entry to `data/models/models.json` following this schema:

```json
{
  "id": "vendor-model-version",
  "name": "Model Name",
  "vendor": "vendor-id",
  "parameters_b": 70,
  "context_window": 128000,
  "release_date": "2026-01-15",
  "benchmarks": {
    "mmlu": 89.5,
    "gpqa_diamond": 55.0,
    "humaneval": 85.0
  },
  "license_spdx": "Apache-2.0",
  "model_type": "open-weight",
  "modality": ["text"],
  "eu_ai_act_risk": "limited-risk",
  "ntia_compliant": true,
  "known_cves": []
}
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b add/model-name`
3. Make your changes in the appropriate JSON file
4. Run validation locally: `python scripts/validate.py`
5. Commit with a descriptive message: `feat: add ModelName to models.json`
6. Push and open a PR against `main`

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New model, vendor, or benchmark entry
- `fix:` - Data correction
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct. Be respectful and constructive.

## Questions?

Open a [discussion](https://github.com/alpha-one-index/awesome-ai-index/discussions) or reach out at [alphaoneindex.com](https://alphaoneindex.com).