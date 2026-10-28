# AI Opportunity Audit

**Find where AI can help a small business, and what to do first.**

This tool helps an AI consultant do an audit of a small business.
The tool asks yes/no questions about the business. Then it finds the AI
opportunities that fit, gives each one a score, and makes a report.

## What the tool does

1. It asks questions about sales, marketing, support, operations, finance and admin.
2. It compares the answers with a catalog of AI opportunities.
3. It gives each opportunity an impact score (1-5) and an effort score (1-5).
4. It sorts the opportunities by priority (impact divided by effort).
5. It writes a Markdown report with a priority list and next steps.

## Install

You must have Python 3.10 or later.

```bash
git clone https://github.com/salaramini1993/ai-opportunity-audit.git
cd ai-opportunity-audit
pip install .
```

To install the test tools too, use `pip install ".[test]"`.

## Use

Run the audit from a JSON file:

```bash
python -m aiaudit --answers examples/online_shop.json
```

Run the audit in the terminal:

```bash
python -m aiaudit --interactive --name "My Business" --out report.md
```

## Opportunity types

| Type | Impact | Effort | What to do |
|---|---|---|---|
| Quick win | High | Low | Do these first |
| Strategic project | High | High | Plan these |
| Small improvement | Low | Low | Do these when you have time |
| Not now | Low | High | Do not do these now |

## Run the tests

```bash
pip install pytest
pytest
```

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## License

MIT
