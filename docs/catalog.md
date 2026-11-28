# Catalog file

The catalog is the file `aiaudit/data/catalog.json`. It has three lists:
`areas`, `industries` and `opportunities`. You can change this file.
You do not need to change Python code.

The tool checks the file when it starts. If a field is wrong, the tool
stops and shows the opportunity and the field. See
[troubleshooting](troubleshooting.md) for the error messages.

## Areas and industries

- `areas`: a list of area names. Each opportunity uses one area. The
  area names are used for `--weight` and `--list-areas`.
- `industries`: a list of industry names, for example `retail`. The names
  are used for `--industry` and `--list-industries`.

## Opportunity fields

Each item in `opportunities` is an object. These fields are required:

- `key`: a name, for example `support_faq_assistant`. No two opportunities
  can have the same key.
- `area`: one of the names in `areas`.
- `title`: a short name for the report. The text must not be empty.
- `description`: text for the report. The text must not be empty. Keep it
  short.
- `signals`: a list of question keys. A question key is a name from
  `--list-questions`. These answers show that the task exists in the
  business. The list must not be empty.
- `base_effort`: a whole number from 1 (easy) to 5 (difficult).

These fields are optional:

- `example_tools`: a list of text with example tools.
- `hours_saved_per_week`: a list of two numbers, `[low, high]`. The
  numbers are from 0 to 40. They give the time saved each week when the
  task fits the business fully. The low value must not be more than the
  high value.
- `cost_per_month`: one of `low` (under 50 EUR), `medium` (50-300 EUR)
  or `high` (more than 300 EUR).
- `risks`: a list of short sentences about risks and checks, for example
  data privacy or human review.
- `gdpr_notes`: a list of short sentences for tasks that use personal
  data. Say what personal data is used and what the business must do.
- `industries`: a list of names from `industries`. If the list is empty
  or not there, the opportunity applies to all industries. The list must
  not have the same name twice.
- `translations`: text in other languages. See below.

Any other field name is an error. This stops typing mistakes, for
example `hours_saved` instead of `hours_saved_per_week`.

## Translations

The `translations` field is an object. Each key is a language code. The
codes that the tool uses are `sv` (Swedish) and `fa` (Persian). Do not use
`en` here. The English text is in the opportunity itself. Each language can
have these fields:

- `title` and `description`: text that is not empty.
- `risks` and `gdpr_notes`: lists of text. Each list must have the same
  number of sentences as the English list. Sentence 1 in the translation
  is the translation of sentence 1 in English.

If a language has no text for a field, the tool uses the English text.

## Example

```json
{
  "key": "support_faq_assistant",
  "area": "customer_support",
  "title": "FAQ assistant for customer questions",
  "description": "Use an AI assistant to answer common customer questions.",
  "signals": ["support_volume", "repeat_questions"],
  "base_effort": 2,
  "hours_saved_per_week": [3, 8],
  "cost_per_month": "medium",
  "risks": ["The assistant can give wrong answers. Check the answers each week."],
  "translations": {
    "sv": {
      "title": "FAQ-assistent för kundfrågor",
      "risks": ["Assistenten kan ge fel svar. Kontrollera svaren varje vecka."]
    }
  }
}
```

## Adding an opportunity

1. Pick a unique `key`.
2. Pick an `area` from `areas`.
3. Add the `signals`. Use question keys from `--list-questions`.
4. Set `base_effort` from 1 to 5.
5. Add the optional fields that you know.
6. Run the tests with `python -m pytest`. The tests check the catalog.
