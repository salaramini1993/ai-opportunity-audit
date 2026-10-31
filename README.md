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
aiaudit --answers examples/online_shop.json
```

The `aiaudit` command is available after `pip install .`.
If you did not install the package, use `python -m aiaudit` instead.

Run the audit in the terminal:

```bash
aiaudit --interactive --name "My Business" --out report.md
```

## Answers on a scale

An answer can be `true` or `false`. An answer can also be a whole number
from 0 to 3. Use the scale when "yes" or "no" is not exact.

| Value | Meaning |
|---|---|
| 0 | No (the same as `false`) |
| 1 | A little |
| 2 | Some |
| 3 | A lot (the same as `true`) |

```json
{
  "business_name": "My Shop",
  "answers": {"support_volume": 3, "repeat_questions": 2, "email_heavy": false}
}
```

A lower value gives a lower fit, a lower impact and fewer hours saved.
In interactive mode, type `y`, `n` or a number from 0 to 3.

## Area weights

You can make some areas more important than others. A weight multiplies
the priority of each opportunity in that area. The default weight is 1.
A weight must be from 0.1 to 5. The weight changes only the sort order.
It does not change the opportunity type.

The areas are: `sales`, `marketing`, `customer_support`, `operations`,
`finance`, `admin`, `hr` and `ecommerce`.

Give weights on the command line:

```bash
aiaudit --answers examples/online_shop.json --weight customer_support=2 --weight admin=0.5
```

Or add an `area_weights` object to the answers file:

```json
{
  "business_name": "My Shop",
  "answers": {"support_volume": true},
  "area_weights": {"customer_support": 2}
}
```

If the file and the command line give a weight for the same area,
the tool uses the value from the command line.

## Opportunity types

| Type | Impact | Effort | What to do |
|---|---|---|---|
| Quick win | High | Low | Do these first |
| Strategic project | High | High | Plan these |
| Small improvement | Low | Low | Do these when you have time |
| Not now | Low | High | Do not do these now |

## Hours saved per week

The report shows an estimate of the hours that each opportunity can save
each week. The catalog gives a range for a small business, for example
2-6 hours. The tool multiplies this range by the fit. If the business has
half of the signals, the estimate is half of the range.

The summary shows the total for all opportunities. These numbers are
rough estimates. Use them to compare opportunities. Measure the real time
before and after you start.

## Cost per month

The report shows a rough tool cost per month for each opportunity.
The cost has three levels:

| Level | Cost per month |
|---|---|
| low | under 50 EUR |
| medium | 50-300 EUR |
| high | more than 300 EUR |

The cost is for the tools only. It does not include the time to set up
the tools. Check the real prices before you buy.

## Risks and checks

The report shows a list of risks and checks for each opportunity. For
example, a person must check each draft, or the data is personal data.
Read the list before you start. Do the checks when the tool is in use.

## Edit the catalog

The catalog is in the file `aiaudit/data/catalog.json`. To add or change
an opportunity, edit this file. You do not need to change Python code.

Each opportunity has these fields:

- `key`: a unique name.
- `area`: one of the names in the `areas` list.
- `title` and `description`: text for the report.
- `signals`: the question keys that show this task exists in the business.
- `base_effort`: an integer from 1 (easy) to 5 (difficult).
- `example_tools`: optional. A list of example tools.
- `hours_saved_per_week`: optional. A list of two numbers `[low, high]`
  from 0 to 40. This is the time saved each week when the task fits fully.
- `cost_per_month`: optional. One of `low`, `medium` or `high`.
- `risks`: optional. A list of short sentences about risks and checks,
  for example data privacy or human review.

The tool checks the file when it starts. If a field is not correct,
the tool stops and shows an error.

## Run the tests

```bash
pip install pytest
pytest
```

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## License

MIT
