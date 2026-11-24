# Troubleshooting

This file lists the error and warning messages of `aiaudit`.
For each message, it says what the message means and how to fix it.
Errors go to the terminal (stderr). The command then stops with exit code 2.

## Errors

- `Error: Unknown question key: KEY`
  The answers file has a question key that the tool does not know.
  Run `python -m aiaudit --list-questions` to see the valid keys.
  Fix the key spelling in the answers file.

- `Error: Answer for KEY must be true, false or a number from 0 to 3`
  An answer has a wrong value. Use `true`, `false`, or a whole number
  from 0 to 3. Do not use text such as `"yes"`.

- `Error: Unknown area: AREA. Known areas: ...`
  An area name in `area_weights` is not valid.
  Run `python -m aiaudit --list-areas` to see the valid names.

- `Error: Weight for AREA must be a number`
  A weight is a text value or a true/false value. Use a number, such as `1.2`.

- `Error: Weight for AREA must be from 0.1 to 5.0`
  A weight is outside the allowed range. Change it to a value in the range.

- `Error: Unknown industry: NAME. Known industries: ...`
  The industry name is not valid.
  Run `python -m aiaudit --list-industries` to see the valid names.

- `Error: 'area_weights' must be an object`
  The `area_weights` value in the answers file is a list or a number.
  Write it as an object, for example `{"marketing": 1.3}`.

- `Error: unknown language 'CODE'. Use one of: ...`
  The `--lang` code is not supported.
  Run `python -m aiaudit --list-languages` to see the valid codes.

## Warnings

- `Warning: no answer for N question(s), counted as no: ...`
  The answers file does not have some questions. The tool still makes
  the report. It counts each missing answer as `false`.
  Add the missing keys to the answers file if the answer is not `false`.
  Run `python -m aiaudit --template` to get a file with every key.
