import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

#PROJECT PATHS AND DATA LOADING

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = (
    PROJECT_DIR / "data" /
    "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)
SCREENSHOTS_DIR = PROJECT_DIR / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

sns.set_theme(style="whitegrid")

print("=" * 50)
print("CUSTOMER CHURN & RETENTION ANALYTICS")
print("=" * 50)

print("\nDataset shape:", df.shape)
print("Duplicate rows:", df.duplicated().sum())
print("Duplicate customer IDs:", df["customerID"].duplicated().sum())

#DATA CLEANING AND QUALITY CHECKS

# Convert TotalCharges to numeric.
# Blank strings become missing values.
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"], errors="coerce"
)

print("\nMissing values after cleaning:")
print(df.isnull().sum()[df.isnull().sum() > 0])

print("\nMissing TotalCharges:", df["TotalCharges"].isna().sum())

# Keep all customer records; do not delete missing values silently.
# Missing TotalCharges are not needed for the churn-rate calculations.

#OVERALL CHURN ANALYSIS
total_customers = len(df)
churned_customers = (df["Churn"] == "Yes").sum()
retained_customers = (df["Churn"] == "No").sum()

churn_rate = churned_customers / total_customers * 100
retention_rate = retained_customers / total_customers * 100

print("\nOVERALL CUSTOMER KPIs")
print("Total customers:", total_customers)
print("Churned customers:", churned_customers)
print("Retained customers:", retained_customers)
print(f"Churn rate: {churn_rate:.2f}%")
print(f"Retention rate: {retention_rate:.2f}%")

# Chart1.Customer churn distribution
churn_counts = df["Churn"].value_counts().reindex(
    ["No", "Yes"], fill_value=0
)

plt.figure(figsize=(7, 5))
ax = sns.barplot(
    x=churn_counts.index,
    y=churn_counts.values
)

ax.bar_label(ax.containers[0], fmt="%.0f")
plt.title("Customer Churn Distribution")
plt.xlabel("Churn Status")
plt.ylabel("Number of Customers")
plt.tight_layout()

plt.savefig(
    SCREENSHOTS_DIR / "churn_distribution.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

#CHURN BY CONTRACT TYPE

contract_analysis = (
    df.groupby("Contract")
    .agg(
        Total_Customers=("customerID", "count"),
        Churned_Customers=(
            "Churn", lambda x: (x == "Yes").sum()
        )
    )
)

contract_analysis["Churn_Rate"] = (
    contract_analysis["Churned_Customers"]
    / contract_analysis["Total_Customers"] * 100
).round(2)

print("\nCHURN BY CONTRACT TYPE")
print(contract_analysis)

contract_analysis["Churn_Rate"].sort_values().plot(
    kind="bar",
    figsize=(9, 5)
)

plt.title("Customer Churn Rate by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    SCREENSHOTS_DIR / "churn_by_contract.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

#CHURN BY TENURE GROUP

df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 72],
    labels=[
        "0-12 Months",
        "13-24 Months",
        "25-48 Months",
        "49-72 Months"
    ]
)

tenure_analysis = (
    df.groupby("TenureGroup", observed=False)
    .agg(
        Total_Customers=("customerID", "count"),
        Churned_Customers=(
            "Churn", lambda x: (x == "Yes").sum()
        )
    )
)

tenure_analysis["Churn_Rate"] = (
    tenure_analysis["Churned_Customers"]
    / tenure_analysis["Total_Customers"] * 100
).round(2)

print("\nCHURN BY TENURE GROUP")
print(tenure_analysis)

tenure_analysis["Churn_Rate"].plot(
    kind="bar",
    figsize=(9, 5)
)

plt.title("Customer Churn Rate by Tenure")
plt.xlabel("Customer Tenure")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    SCREENSHOTS_DIR / "churn_by_tenure.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

#CHURN BY PAYMENT METHOD

payment_analysis = (
    df.groupby("PaymentMethod")
    .agg(
        Total_Customers=("customerID", "count"),
        Churned_Customers=(
            "Churn", lambda x: (x == "Yes").sum()
        )
    )
)

payment_analysis["Churn_Rate"] = (
    payment_analysis["Churned_Customers"]
    / payment_analysis["Total_Customers"] * 100
).round(2)

payment_analysis = payment_analysis.sort_values(
    "Churn_Rate", ascending=False
)

print("\nCHURN BY PAYMENT METHOD")
print(payment_analysis)

payment_analysis["Churn_Rate"].sort_values().plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Customer Churn Rate by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()

plt.savefig(
    SCREENSHOTS_DIR / "churn_by_payment_method.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

#SAVE ANALYSIS RESULTS

contract_analysis.to_csv(
    PROJECT_DIR / "contract_churn_results.csv"
)

tenure_analysis.to_csv(
    PROJECT_DIR / "tenure_churn_results.csv"
)

payment_analysis.to_csv(
    PROJECT_DIR / "payment_churn_results.csv"
)

print("\nAnalysis completed successfully.")
print("Charts saved in:", SCREENSHOTS_DIR)
print("Summary tables saved in:", PROJECT_DIR)
