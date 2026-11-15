# Example businesses

The `examples/` folder has sample answers for several kinds of business.
Use them to test the tool, or to see what a report looks like.
Run one with `--answers`:

```bash
aiaudit --answers examples/dental_clinic.json
```

Each file has these parts:

- `business_name`: the name that the report shows.
- `answers`: the yes/no and scale answers for each question.
- `industry` (optional): the industry filter, for example `restaurant`.
- `area_weights` (optional): the weight for each area.

## The examples

- `examples/accounting_firm.json`: a tax and bookkeeping firm with 6 staff.
  Industry: services. Weight: finance.
- `examples/dental_clinic.json`: a dental clinic with 2 dentists and 9 staff.
  Industry: services. Weights: admin and customer support.
- `examples/law_firm.json`: a law firm with 3 lawyers and 4 staff.
  Industry: services. Weights: admin and sales.
- `examples/manufacturer.json`: a metal parts maker with 40 staff.
  Industry: manufacturing. Weight: operations.
- `examples/online_shop.json`: an online shop that imports from China and
  sells in the EU. It has no industry and no area weights.
- `examples/restaurant.json`: a restaurant with lunch and dinner service
  at 2 locations. Industry: restaurant. Weights: customer support and HR.

## Make your own example

Copy one of the files and change the answers. Keep the same question keys.
Run `aiaudit --list-questions` to see the keys. Run `aiaudit --list-industries`
to see the industry names. Run `aiaudit --list-areas` to see the area names.
