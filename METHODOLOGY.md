# Methodology

> How we collect, validate, and maintain the awesome-ai-index datasets.

---

## 1. Model Selection Criteria

A model is included if it meets **all** of the following:

| Criterion | Threshold |
|-----------|----------|
| Public availability | API or weights downloadable |
| Parameter count disclosed | Yes |
| At least one benchmark score | Independently verified |
| Release date | After January 2023 |

Models are **excluded** if they are:
- Unreleased or rumored
- Fine-tunes of existing entries without novel architecture
- Duplicates under marketing aliases

## 2. Benchmark Sources

All scores come from **primary or independently verified sources**:

| Benchmark | Primary Source |
|-----------|---------------|
| MMLU / MMLU-Pro | Original papers; Hugging Face Open LLM Leaderboard |
| GPQA Diamond | Official leaderboard |
| HumanEval | OpenAI evals repo; vendor technical reports |
| SWE-bench Verified | SWE-bench official site |
| MATH-500 | Hendrycks et al. original dataset |
| Chatbot Arena | LMSYS Chatbot Arena Elo rankings |
| ARC-AGI-2 | ARC Prize Foundation |
| IFEval | Google Research |
| LiveCodeBench | LiveCodeBench leaderboard |
| AIME 2025 | AMC/AIME competition results |

When a vendor self-reports a score without independent replication, we tag it `"source": "vendor-reported"` in the JSON.

## 3. Vendor Data

Vendor entries are sourced from:
- Official company websites and press releases
- Crunchbase for founding year and HQ
- GitHub organization pages for open-source activity

Each vendor record includes: `id`, `name`, `hq_country`, `hq_city`, `founded`, `focus`, and `website`.

## 4. Compliance Framework Mapping

We map each framework from its **official legislative or standards body text**:

| Framework | Authority |
|-----------|-----------|
| EU AI Act | European Parliament |
| NIST AI RMF 1.0 | U.S. NIST |
| ISO/IEC 42001 | ISO/IEC JTC 1/SC 42 |
| NTIA AI SBOM | U.S. NTIA |
| Canada AIDA | Parliament of Canada |
| UK AI Regulation | UK DSIT |
| China AI Regulations | CAC |

Risk tiers (e.g., `high-risk`, `limited-risk`) follow the EU AI Act Annex III classification.

## 5. Update Cadence

| Dataset | Frequency | Method |
|---------|-----------|--------|
| Models | Weekly (Friday) | GitHub Actions + manual review |
| Vendors | Weekly | Automated check + PR review |
| Benchmarks | Monthly | Manual survey of new benchmarks |
| Compliance | Quarterly | Legislative tracking |

## 6. Data Validation

Every PR and push triggers `scripts/validate.py`, which checks:

1. **Schema conformance** - All required fields present and correctly typed
2. **ID uniqueness** - No duplicate `id` values within a dataset
3. **Referential integrity** - Every `model.vendor` matches a `vendor.id`
4. **Date format** - ISO 8601 (`YYYY-MM-DD`)
5. **URL reachability** - Optional check for broken links
6. **Benchmark range** - Scores within plausible bounds (0-100 for percentages, 800-1600 for Elo)

## 7. Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR** - Breaking schema changes
- **MINOR** - New datasets or fields added
- **PATCH** - Data corrections, new model/vendor entries

Each release is tagged and published as a GitHub Release with a changelog.

## 8. Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to submit additions or corrections.

---

*Last updated: 2026-03-20*