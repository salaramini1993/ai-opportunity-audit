# Answers file format

This guide explains the JSON file that you give to `--answers`.
Use it with the audit interview in `docs/interview.md`.

## Top-level fields

The file is one JSON object with these fields:

- `business_name`: the name of the business. Optional. The default is "Unnamed business".
- `industry`: one industry name. Optional. The names are `manufacturing`, `restaurant`, `retail`, `services`. Run `aiaudit --list-industries` to see the same names.
- `answers`: an object with one value for each question key. Required.
- `area_weights`: an object that sets how important each area is. Optional.

## Answers

Each key in `answers` is a question key. Each value is one of these:

- `true` or `false` for a yes or no answer.
- A whole number from 0 to 3 for a scale answer.

A key that is not in the question list is an error. Run `aiaudit --list-questions` to see the valid keys.

## Question keys

The keys below are the same as the output of `aiaudit --list-questions`.

| Key | Question |
| --- | --- |
| `sells_products` | Do you sell physical or digital products? |
| `many_products` | Do you have more than 50 products or services? |
| `multi_language` | Do you work in more than one language? |
| `support_volume` | Do you get more than 20 customer questions each week? |
| `repeat_questions` | Do customers often ask the same questions? |
| `email_heavy` | Do you spend more than 1 hour each day on email? |
| `posts_social` | Do you post on social media for your business? |
| `small_team` | Do you have fewer than 10 people in the team? |
| `has_leads` | Do you get new sales leads each month? |
| `uses_crm` | Do you use a CRM or a customer list? |
| `writes_quotes` | Do you write quotes or offers for customers? |
| `paper_invoices` | Do you get invoices or receipts as PDF or paper? |
| `manual_bookkeeping` | Do you type financial data by hand? |
| `monthly_reports` | Do you make monthly reports? |
| `holds_stock` | Do you keep stock in a warehouse or at home? |
| `foreign_suppliers` | Do you buy from suppliers in other countries? |
| `many_meetings` | Do you have more than 5 meetings each week? |
| `many_documents` | Do you have many internal documents or procedures? |
| `staff_ask_same` | Do staff often ask the same internal questions? |
| `hires_often` | Do you hire new staff 2 or more times each year? |
| `writes_job_ads` | Do you write your own job ads? |
| `many_applicants` | Do you get more than 20 applications for each job? |
| `sells_online` | Do you sell through a web shop or a marketplace? |
| `gets_reviews` | Do customers write reviews of your products online? |
| `many_returns` | Do you get more than 10 returns each month? |
| `ships_parcels` | Do you send parcels or goods to customers? |
| `where_is_my_order` | Do customers often ask where their order is? |
| `ships_abroad` | Do you send goods to countries outside the EU? |
| `customs_documents` | Do you make customs documents yourself? |

## Area weights

Each key in `area_weights` is an area name. Each value is a number from 0.1 to 5.0.
The default weight for every area is 1.0. A weight of 2 makes an area twice as important.

These are the area names:

- `admin`
- `customer_support`
- `ecommerce`
- `finance`
- `hr`
- `logistics`
- `marketing`
- `operations`
- `sales`

You can also set a weight on the command line with `--weight AREA=NUMBER`.
The command line value replaces the value in the file.

## Small example

```json
{
  "business_name": "Corner Bakery",
  "industry": "retail",
  "answers": {
    "sells_online": true,
    "gets_reviews": false,
    "support_volume": 2
  },
  "area_weights": {
    "customer_support": 2
  }
}
```

Run the file with:

```bash
aiaudit --answers corner_bakery.json
```
