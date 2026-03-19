# Fintech Retention Funnel Analysis

## Overview
This project analyses user retention in a simulated fintech app using Python and SQL-style product analytics.

The goal was to identify which early user behaviours are most strongly associated with 7-day retention, and to propose a product change that could improve early engagement and long-term retention.

## Business Problem
Many fintech users sign up but do not become retained users.

This project investigates which early actions in the onboarding journey are most predictive of 7-day retention, with a focus on understanding whether users need to simply fund their account or whether they need to go further and experience the core value of the product.

## Dataset
This project uses a synthetic but behaviour-driven dataset designed to simulate a realistic fintech onboarding funnel.

It includes:
- `users.csv` — user signup dates and acquisition channels
- `events.csv` — user actions such as:
  - `app_open_initial`
  - `add_money`
  - `make_payment`
  - `set_up_direct_debit`
  - `app_open_return`

The dataset was designed so that stronger progression through the funnel increases the probability of retention.

## Key Question
Which early user behaviour is the strongest driver of 7-day retention?

## Method
The analysis followed these steps:
1. Define 7-day retention as a return app open between day 2 and day 7 after signup
2. Measure overall retention
3. Compare users who added money early vs those who did not
4. Compare three user groups:
   - Group A: added money and made a payment within 3 days
   - Group B: added money within 3 days but did not make a payment
   - Group C: did not add money within 3 days

## Key Results
- Overall 7-day retention: **35.7%**
- Early add money retention: **42.9%**
- No early add money retention: **8.2%**

Retention by behavioural group:
- **Group A (add money + payment): 61.1%**
- **Group B (add money only): 33.8%**
- **Group C (no add money): 8.2%**

## Main Insight
The strongest behavioural driver of retention is **making a first payment within the first few days of signup**.

Users who add money and complete a payment early have materially higher retention than users who only add money, suggesting that experiencing the core value of the product early is the key mechanism driving retention.

## Product Recommendation
Introduce a **guided onboarding checklist** immediately after signup.

The checklist should prompt users to:
1. Add money
2. Make their first payment

This is designed to reduce friction and help users reach the product’s “aha moment” faster.

## Experiment Design
To validate this recommendation:

- **Control group:** existing onboarding flow
- **Treatment group:** guided onboarding checklist

### Primary metric
- 7-day retention rate

### Secondary metrics
- % of users adding money within 3 days
- % of users making a payment within 3 days

### Test duration
- 2–4 weeks, depending on sample size

## Tools Used
- Python
- Pandas
- VS Code
- GitHub
- SQL

## Files
- `generate_data.py` — generates the synthetic behaviour-driven dataset
- `analysis.py` — runs the retention and funnel analysis
- `retention_analysis.sql` — SQL version of key retention logic
- `users.csv` — user table
- `events.csv` — event table

## Next Steps
- add a fuller SQL version of the funnel analysis
- create a Streamlit dashboard
- test additional behaviours such as direct debit setup and recurring usage