import pandas as pd
import numpy as np
from datetime import timedelta

np.random.seed(42)

n_users = 1000

# -----------------------------
# Create users
# -----------------------------
users = pd.DataFrame({
    "user_id": range(1, n_users + 1),
    "signup_date": pd.to_datetime("2024-01-01") + pd.to_timedelta(
        np.random.randint(0, 90, n_users), unit="D"
    ),
    "acquisition_channel": np.random.choice(
        ["organic", "paid", "referral"], n_users
    )
})

events = []

for _, user in users.iterrows():
    user_id = user["user_id"]
    signup_date = user["signup_date"]

    # -----------------------------
    # Optional initial app open
    # This is onboarding / first use
    # It should NOT be used as retention
    # -----------------------------
    if np.random.rand() < 0.85:
        initial_open_time = signup_date + timedelta(days=np.random.randint(0, 2))
        events.append([user_id, "app_open_initial", initial_open_time, None])

    # -----------------------------
    # Behaviour funnel
    # -----------------------------
    did_add_money = False
    did_make_payment = False
    did_set_up_dd = False

    # 80% add money
    if np.random.rand() < 0.80:
        did_add_money = True
        add_money_time = signup_date + timedelta(days=np.random.randint(0, 4))
        add_money_amount = np.random.randint(50, 1000)
        events.append([user_id, "add_money", add_money_time, add_money_amount])

        # 50% of add_money users make a payment
        if np.random.rand() < 0.50:
            did_make_payment = True
            payment_time = add_money_time + timedelta(days=np.random.randint(0, 4))
            payment_amount = np.random.randint(5, 200)
            events.append([user_id, "make_payment", payment_time, payment_amount])

            # 35% of payment users set up direct debit
            if np.random.rand() < 0.35:
                did_set_up_dd = True
                dd_time = payment_time + timedelta(days=np.random.randint(0, 4))
                events.append([user_id, "set_up_direct_debit", dd_time, None])

    # -----------------------------
    # Retention probability
    # Based on strongest behaviour reached
    # -----------------------------
    if did_set_up_dd:
        retention_prob = 0.75
    elif did_add_money and did_make_payment:
        retention_prob = 0.50
    elif did_add_money:
        retention_prob = 0.25
    else:
        retention_prob = 0.10

    # -----------------------------
    # Return event for retention
    # Counts only if day 2-7
    # -----------------------------
    retained = np.random.rand() < retention_prob
    if retained:
        return_time = signup_date + timedelta(days=np.random.randint(2, 8))
        events.append([user_id, "app_open_return", return_time, None])

# -----------------------------
# Save data
# -----------------------------
events_df = pd.DataFrame(
    events,
    columns=["user_id", "event_name", "event_time", "amount"]
)

users.to_csv("users.csv", index=False)
events_df.to_csv("events.csv", index=False)

print("Clean behaviour-driven dataset generated successfully.")