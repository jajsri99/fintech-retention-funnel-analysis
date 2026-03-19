import pandas as pd

# -----------------------------
# Load data
# -----------------------------
users = pd.read_csv("users.csv")
events = pd.read_csv("events.csv")

# Convert dates
users["signup_date"] = pd.to_datetime(users["signup_date"])
events["event_time"] = pd.to_datetime(events["event_time"])

# -----------------------------
# 1. 7-day retention
# Definition:
# A user is retained if they have at least one app_open_return
# between day 2 and day 7 after signup
# -----------------------------
returns = events[events["event_name"] == "app_open_return"].copy()

returns = returns.merge(
    users[["user_id", "signup_date"]],
    on="user_id",
    how="left"
)

returns["days_since_signup"] = (
    returns["event_time"] - returns["signup_date"]
).dt.days

retained_users = returns[
    (returns["days_since_signup"] >= 2) &
    (returns["days_since_signup"] <= 7)
]["user_id"].unique()

users["retained_7d"] = users["user_id"].isin(retained_users)

total_users = users["user_id"].nunique()
retained_7d_count = users["retained_7d"].sum()
retention_rate_7d = retained_7d_count / total_users

print("=== Overall 7-Day Retention ===")
print("Total users:", total_users)
print("Returned within 7 days:", retained_7d_count)
print("7-day retention rate:", round(retention_rate_7d, 3))

# -----------------------------
# 2. Early add_money analysis
# Definition:
# A user is an early add_money user if they add money
# within 3 days of signup
# -----------------------------
add_money = events[events["event_name"] == "add_money"].copy()

add_money = add_money.merge(
    users[["user_id", "signup_date"]],
    on="user_id",
    how="left"
)

add_money["days_to_add_money"] = (
    add_money["event_time"] - add_money["signup_date"]
).dt.days

early_add_users = add_money[
    (add_money["days_to_add_money"] >= 0) &
    (add_money["days_to_add_money"] <= 3)
]["user_id"].unique()

users["early_add_money"] = users["user_id"].isin(early_add_users)

early_group = users[users["early_add_money"] == True]
non_early_group = users[users["early_add_money"] == False]

retention_early = early_group["retained_7d"].mean()
retention_non_early = non_early_group["retained_7d"].mean()

print("\n=== Early Add Money Analysis ===")
print("Users with early add_money:", early_group["user_id"].nunique())
print("Users without early add_money:", non_early_group["user_id"].nunique())
print("Early add_money retention:", round(retention_early, 3))
print("No early add_money retention:", round(retention_non_early, 3))
print("Difference:", round(retention_early - retention_non_early, 3))

# -----------------------------
# 3. Retention by acquisition channel
# -----------------------------
channel_retention = (
    users.groupby("acquisition_channel")
    .agg(
        total_users=("user_id", "count"),
        retained_users=("retained_7d", "sum")
    )
    .reset_index()
)

channel_retention["retention_rate"] = (
    channel_retention["retained_users"] / channel_retention["total_users"]
)

print("\n=== Retention by Acquisition Channel ===")
print(channel_retention)

# -----------------------------
# 4. Retention by signup cohort (month)
# -----------------------------
users["signup_month"] = users["signup_date"].dt.to_period("M").astype(str)

cohort_retention = (
    users.groupby("signup_month")
    .agg(
        total_users=("user_id", "count"),
        retained_users=("retained_7d", "sum")
    )
    .reset_index()
)

cohort_retention["retention_rate"] = (
    cohort_retention["retained_users"] / cohort_retention["total_users"]
)

print("\n=== Retention by Signup Cohort ===")
print(cohort_retention.sort_values("signup_month"))

# --- Funnel Analysis: Add Money + Payment ---

# ADD MONEY
add_money = events[events["event_name"] == "add_money"].copy()
add_money = add_money.merge(users[["user_id", "signup_date"]], on="user_id")
add_money["days_to_add"] = (add_money["event_time"] - add_money["signup_date"]).dt.days

early_add = add_money[add_money["days_to_add"] <= 3]["user_id"].unique()

# MAKE PAYMENT
payments = events[events["event_name"] == "make_payment"].copy()
payments = payments.merge(users[["user_id", "signup_date"]], on="user_id")
payments["days_to_pay"] = (payments["event_time"] - payments["signup_date"]).dt.days

early_pay = payments[payments["days_to_pay"] <= 3]["user_id"].unique()

# GROUPS
group_A = users["user_id"].isin(early_add) & users["user_id"].isin(early_pay)
group_B = users["user_id"].isin(early_add) & ~users["user_id"].isin(early_pay)
group_C = ~users["user_id"].isin(early_add)

users["group"] = "C"
users.loc[group_B, "group"] = "B"
users.loc[group_A, "group"] = "A"

# RETENTION BY GROUP
group_retention = users.groupby("group")["retained_7d"].mean()

print("\n=== Funnel Analysis (Add Money + Payment) ===")
print(group_retention)