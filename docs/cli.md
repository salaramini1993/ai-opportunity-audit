# Command-line options

This file lists the options of the `aiaudit` command.
Run `python -m aiaudit --help` to see the same list in the terminal.

Use one source of answers: `--answers FILE` or `--interactive`.
These two options cannot be used together.

## Source of answers

- `--answers FILE`: read the answers, the business name, the area
  weights and the industry from a JSON file. See the files in `examples/`.
- `--interactive`: ask the questions in the terminal.

## Listing options

These options print a list and stop. They do not need an answers file.

- `--list-questions`: print each question key and its text.
- `--list-opportunities`: print each opportunity key, area and title.
- `--list-industries`: print the industry names for `--industry`.
- `--list-areas`: print the area names for `--weight`.
- `--list-languages`: print the language codes for `--lang`, with their
  English names.
- `--list-formats`: print the report format names for `--format`.
- `--template`: print a blank answers file with every question key set to
  false. Save it, change the answers and run it with `--answers`.

## Report options

- `--name NAME`: the business name in the report. It replaces the name in
  the answers file.
- `--out FILE`: write the report to this file. The folders of the file
  are made if they do not exist. Without this option, the report is printed.
- `--format {markdown,html,csv,json}`: the report format. The default is
  markdown. The csv and json formats give only the priority list.
- `--lang {en,sv,fa}`: the language of the headings and labels. The default
  is en. The csv format does not use this option.

## Scoring options

- `--weight AREA=NUMBER`: make an area more or less important, for example
  `--weight customer_support=2`. Use this option more than one time for
  more areas. A value here replaces the same value in the answers file.
- `--industry NAME`: show only the opportunities for this industry. It
  replaces the industry in the answers file.
- `--top NUMBER`: show only the NUMBER opportunities with the highest
  priority. The number must be 1 or more. The default is to show all
  opportunities that fit.
- `--min-priority NUMBER`: hide the opportunities with a priority below
  NUMBER. The number must be 0 or more. The default is to hide none.
  It runs before `--top`.
  If the filters hide every opportunity, a warning is printed.
- `--exclude KEY`: hide the opportunity with this key, for example
  `--exclude support_faq_assistant`. Use `--list-opportunities` to see the keys.
  Use this option more than one time for more opportunities. The default is
  to hide none. It runs before `--min-priority` and `--top`.
- `--quadrant NAME`: show only the opportunities in this quadrant. The names
  are `quick win`, `strategic project`, `small improvement` and `not now`.
  Use quotation marks for a name with a space, for example
  `--quadrant "quick win"`. The default is to show all quadrants. It runs
  before `--min-priority` and `--top`. See [scoring](scoring.md#quadrant).

## Other options

- `--quiet`: do not print warnings. For example, the warning about
  questions that the answers file leaves out is not shown. Errors are
  still printed.
- `--version`: print the version of the toolkit.
- `-h` or `--help`: print the help text.
