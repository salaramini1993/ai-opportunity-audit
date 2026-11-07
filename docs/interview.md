# How to run an audit interview

This guide shows how to ask a business owner the audit questions.
Use it before you run `aiaudit`. The answers go into a JSON file.

## Before the meeting

1. Book 30 minutes with the owner. Ask for a quiet room.
2. Ask the owner to bring a list of their main tools. For example: the
   web shop, the email account, the accounting software.
3. Print the question list. Run `aiaudit --interactive` to read the
   questions in order.

## During the meeting

1. Explain the goal in one sentence. Say: "We will find where AI can
   help your business first."
2. Ask each question as written. Do not add words to the question.
3. Accept a clear answer. For a yes/no question, use `true` or `false`.
4. Some answers are a scale. Use a whole number from 0 to 3. Use the
   level the owner gives: 0 is the lowest level and 3 is the highest.
5. If the owner is not sure, write a note. Check the answer again later.
   Do not guess.

## Ask about the industry

Ask which group the business belongs to. The groups are `retail`,
`services`, `manufacturing` and `restaurant`. If none fits, leave the
`industry` field out. The audit then shows all opportunities.

## Ask about areas that matter most

Ask: "Which work area is most important for you?" Common areas are
`customer_support`, `hr`, `finance`, `sales` and `operations`.
Give that area a higher weight, such as 1.5. Leave the others at 1.

## Write the answers file

Save the answers in a JSON file. Use the same keys as the examples in
the `examples/` folder. For example:

```json
{
  "business_name": "Example Bakery",
  "industry": "retail",
  "answers": {
    "sells_products": true,
    "support_volume": false
  },
  "area_weights": {"customer_support": 1.5}
}
```

Then run the audit:

```bash
aiaudit --answers bakery.json --format html --out bakery.html
```

## After the meeting

1. Read the report with the owner. Start with the top three items.
2. Check each GDPR note. If the opportunity uses personal data, plan a
   human check before you start.
3. Agree on one first step for the next 30 days.
4. Send the report and the answers file to the owner within one day.

## Do not do this

- Do not promise results. The report gives estimates only.
- Do not record personal data about staff or customers in the answers
  file. The file needs only yes/no and scale answers.
- Do not sell a tool in the meeting. Show the report first.
