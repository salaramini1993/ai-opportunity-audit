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

- [x] HTML report (`--format html`)
- [x] Impact/effort chart in the HTML report
- [x] CSV export of the priority list
- [x] 30/60/90-day action plan section (Markdown report)
- [x] 30/60/90-day action plan section in the HTML report
- [x] Report in Swedish
  - [x] Swedish headings and labels in the Markdown report (`--lang sv`)
  - [x] Swedish text for the 30/60/90-day action plan
  - [x] Swedish title and description for the opportunities in the catalog
  - [x] Swedish risks and GDPR notes for the opportunities in the catalog
  - [x] Swedish HTML report
    - [x] Swedish headings, labels and text in the HTML report
    - [x] Swedish labels inside the impact/effort chart
- [x] Report in Persian
  - [x] Persian headings, labels and plan text in the Markdown report (`--lang fa`)
  - [x] Persian title and description for the opportunities in the catalog
  - [x] Persian risks and GDPR notes for the opportunities in the catalog
  - [x] Right-to-left layout (`dir="rtl"`) in the Persian HTML report and chart

## Quality

- [x] GitHub Actions workflow: run tests on each push
- [x] Add ruff lint config and fix warnings
- [x] Add type checks with mypy
- [x] Tests for the CLI (JSON input, bad input, output file)
- [ ] Test coverage above 90%

## Docs

- [x] Guide: how to run an audit interview with a business owner
- [x] Example business: restaurant
- [x] Example business: accounting firm
- [x] Example business: manufacturer
- [x] CHANGELOG.md
- [x] CONTRIBUTING.md
