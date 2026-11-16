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

## Report options

- `--name NAME`: the business name in the report. It replaces the name in
  the answers file.
- `--out FILE`: write the report to this file. Without this option, the
  report is printed.
- `--format {markdown,html,csv}`: the report format. The default is
  markdown. The csv format gives only the priority list.
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

## Other options

- `--version`: print the version of the toolkit.
- `-h` or `--help`: print the help text.
