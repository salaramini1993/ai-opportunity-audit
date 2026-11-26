# Report formats

The `aiaudit` command makes one report for each audit.
Use `--format` to choose the type of report:
`markdown`, `html`, `csv` or `json`. The default is `markdown`.

## Markdown

The Markdown report is plain text. It works in any editor and on most
websites. It has:

- a summary,
- the priority list of opportunities,
- the details of each opportunity, with its risks and GDPR notes,
- the 30/60/90-day action plan.

Use `--lang sv` or `--lang fa` for a report in Swedish or Persian.

## HTML

The HTML report opens in a web browser. It has the same content as the
Markdown report. It also has an impact/effort chart. The Persian report
uses a right-to-left layout.

## CSV

The CSV report is a table for spreadsheets. Each row is one opportunity.
The first row is the header. The columns are:

- `rank`: the place in the priority list. The first row is 1.
- `key`: the opportunity key, as shown by `--list-opportunities`.
- `title`: the opportunity title.
- `area`: the area of the opportunity, as shown by `--list-areas`.
- `quadrant`: the place on the impact/effort chart.
- `impact`: the impact score.
- `effort`: the effort score.
- `weight`: the area weight that was used. The default is 1.0.
- `priority`: the priority score. A higher number means a higher priority.
- `fit`: how well the business matches the opportunity.
- `hours_saved_low`: the low estimate of hours saved each week.
- `hours_saved_high`: the high estimate of hours saved each week.
- `cost_per_month`: the cost level: `low`, `medium` or `high`.

If the catalog has no hours or cost estimate for an opportunity, the
cell is empty. If no opportunity matches, the CSV report has only the
header row. The column names and the titles are always in English.

## JSON

The JSON report is a file for other programs. It has the same priority
list as the CSV report. The file is one JSON object with three keys:
`business` (the business name), `industry` (the industry, or `null`) and
`opportunities` (the list). Each item in `opportunities` has the same
fields as a CSV column, in the same order. An empty CSV cell is `null`
in the JSON report. Use `--format json --out FILE` to save the file.

## Example

```bash
aiaudit --answers examples/restaurant.json --format csv --out restaurant.csv
```

Open `restaurant.csv` in a spreadsheet program to sort the list or
filter it by area.
