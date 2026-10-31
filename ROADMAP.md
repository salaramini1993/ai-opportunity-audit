# Roadmap

This file is the work list. Do one task at a time. Mark a task as done
with `[x]` in the same commit as the change. Add new tasks when you find them.

## Core

- [x] Opportunity catalog (12 opportunities, 6 areas)
- [x] Yes/no question bank
- [x] Scoring: fit, impact, effort, priority, quadrant
- [x] Markdown report
- [x] CLI with JSON input and interactive mode
- [x] Add `pyproject.toml` so users can install with `pip install .`
- [x] Add an `aiaudit` console script entry point
- [x] Load the catalog from a JSON data file, not from Python code
- [x] Add weights per area (for example, a user can say "support is most important")
- [x] Estimate hours saved per week for each opportunity
- [x] Estimate cost per month for each opportunity (low / medium / high)
- [x] Add a "risks and checks" field to each opportunity (data privacy, human review)
- [x] Add answers with a scale (0-3) in addition to yes/no

## Catalog

- [x] Add HR opportunities (job ads, CV screening with human review)
- [x] Add e-commerce opportunities (review replies, return reasons analysis)
- [x] Add logistics opportunities (shipment status replies, customs document check)
- [x] Add an industry filter (retail, services, manufacturing, restaurant)
- [x] Add GDPR notes for opportunities that use personal data

## Reports

- [ ] HTML report with a simple impact/effort chart
- [ ] CSV export of the priority list
- [ ] 30/60/90-day action plan section
- [ ] Report in Swedish
- [ ] Report in Persian

## Quality

- [ ] GitHub Actions workflow: run tests on each push
- [ ] Add ruff lint config and fix warnings
- [ ] Add type checks with mypy
- [ ] Tests for the CLI (JSON input, bad input, output file)
- [ ] Test coverage above 90%

## Docs

- [ ] Guide: how to run an audit interview with a business owner
- [ ] Two more example businesses (restaurant, accounting firm)
- [ ] CHANGELOG.md
- [ ] CONTRIBUTING.md
