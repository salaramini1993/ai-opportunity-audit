# Scoring rules

This page explains how the audit scores each opportunity.
The code is in `aiaudit/scoring.py`.

## Answers

Each answer is yes, no, or a number from 0 to 3.

- 0 means no.
- 1 means a little.
- 2 means some.
- 3 means a lot.
- true has the same value as 3.
- false has the same value as 0.

The signal strength is the answer divided by 3. So the strength is
0.0 to 1.0.

## Fit

The fit is the mean signal strength of the signals for an opportunity.
The fit is a number from 0.0 to 1.0.

An opportunity is shown only when its fit is at least 0.5.

## Impact

The impact is a whole number from 1 to 5.

The impact is 2 plus the sum of the signal strengths, rounded to a
whole number. The impact can never be more than 5.

## Effort

The effort is the base effort from the catalog. It is a number from 1 to 5.
Lower effort means the change is easier.

## Area weights

Each area has a weight. The default weight is 1.0.

A weight can be from 0.1 to 5.0. A weight of 2.0 doubles the priority
of every opportunity in that area. The weight changes only the sort
order. It does not change the quadrant.

## Priority

Priority = impact x area weight / effort, rounded to two decimal places.

The list is sorted by priority, highest first. Ties are sorted by impact,
then by key.

## Quadrant

| Impact | Effort | Quadrant |
|---|---|---|
| 3 to 5 | 1 or 2 | quick win |
| 3 to 5 | 3 to 5 | strategic project |
| 1 or 2 | 1 or 2 | small improvement |
| 1 or 2 | 3 to 5 | not now |

## Hours saved

The catalog gives a range of hours saved per week, for example 2 to 4.
The estimate is the range multiplied by the fit.

For example, an opportunity with a range of 2 to 4 hours and a fit
of 0.5 gives an estimate of 1.0 to 2.0 hours per week.

This is a rough estimate. Use it to compare opportunities. Do not use
it as a promise.

## Industries

If you give an industry, only the opportunities for that industry are
scored. An opportunity with no industry list applies to every industry.
