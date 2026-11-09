# Contributing

Thank you for your help. This guide explains how to change the project.

## Set up

```bash
git clone https://github.com/salaramini1993/ai-opportunity-audit.git
cd ai-opportunity-audit
pip install -e ".[test]"
pytest
```

All tests must pass before you open a pull request.

## Check test coverage

Coverage shows which lines the tests do not run. Run these commands:

```bash
pip install pytest-cov
pytest --cov=aiaudit --cov-report=term-missing
```

The column `Missing` lists the line numbers that no test runs.
The project goal is more than 90% coverage. Add a test when you change
a line that has no coverage.

## Where things are

- `aiaudit/data/catalog.json`: the opportunities, with translations.
- `aiaudit/questions.py`: the yes/no questions.
- `aiaudit/scoring.py`: how fit, impact, effort and priority are calculated.
- `aiaudit/*_report.py`: the Markdown, HTML and CSV output.
- `tests/`: one file for each feature.
- `ROADMAP.md`: the list of open tasks.

## Add an opportunity

1. Add a new question in `aiaudit/questions.py` if you need one.
2. Add the opportunity to `aiaudit/data/catalog.json`. Use a unique `key`.
3. Add a Swedish and a Persian translation. The `risks` and `gdpr_notes`
   lists must have the same number of sentences as the English lists.
4. Add a test in `tests/` that shows the opportunity appears for the right answers.

## Make a change

- Keep one change in one pull request.
- Write the commit message in the imperative mood, for example "Add invoice check".
- Mark the matching task in `ROADMAP.md` with `[x]` in the same commit.
- Write new text for users in plain English. Use short sentences.

## Code style

- Python 3.10 or later.
- Use type hints for public functions.
- Keep functions short. Do not add a dependency unless it is needed.
