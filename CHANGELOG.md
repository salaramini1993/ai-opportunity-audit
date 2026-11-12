# Changelog

All notable changes to this project are listed here.
The newest changes are at the top.

## Unreleased

### Added

- `--list-questions` option that prints each question key and text.
- `--list-industries` option that prints the industry names.
- `--version` option that prints the toolkit version.
- Accounting firm example business (`examples/accounting_firm.json`).
- Guide for running an audit interview with a business owner
  (`docs/interview.md`).
- Restaurant example business (`examples/restaurant.json`).
- Tests for the CLI with JSON input, bad input and output files.
- GitHub Actions workflow that runs the tests on each push.
- Report in Persian: headings, labels and plan text (`--lang fa`),
  opportunity text, risks and GDPR notes. The HTML report and chart
  use right-to-left layout.
- Report in Swedish: headings, labels, plan text, opportunity text,
  risks and GDPR notes. Use `--lang sv`.
- CSV export of the priority list (`--format csv`).
- HTML report (`--format html`) with an impact/effort chart and a
  30/60/90-day action plan.
- 30/60/90-day action plan section in the Markdown report.
- Estimates of hours saved per week and cost per month for each
  opportunity.
- Answers with a scale from 0 to 3, in addition to yes and no.
- Area weights, so one area can count more in the priority list.
- Industry filter: retail, services, manufacturing and restaurant.
- Human-review and data-privacy checks for each opportunity.
- GDPR notes for opportunities that use personal data.
- HR, e-commerce and logistics opportunities.
- `pyproject.toml`, so the tool installs with `pip install .`, and an
  `aiaudit` command.
- Catalog loaded from a JSON data file (`aiaudit/data/catalog.json`).

### Changed

- Opportunity catalog and question bank moved out of Python code into
  JSON data files.
