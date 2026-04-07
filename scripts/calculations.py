import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/cleaned_financial_dataset.csv")
print("Cleaned dataset loaded.")

# Aggregate to annual level
annual_df = df.groupby(["Company_ID", "Year"]).agg({
    "Revenue": "sum",
    "Expenses": "sum",
    "Net_Income": "sum",
    "Assets": "mean",
    "Liabilities": "mean",
    "Equity": "mean",
    "Cash_Flow": "sum"
}).reset_index()

print("Annual aggregation complete.")
print("Annual shape:", annual_df.shape)

# Calculate financial ratios:
# Net Profit Margin (measures profitability efficiency)
annual_df["Net_Profit_Margin"] = annual_df["Net_Income"] / annual_df["Revenue"]

# Debt to Equity (measures financial leverage)
annual_df["Debt_to_Equity"] = annual_df["Liabilities"] / annual_df["Equity"]

# Return on Equity (measures shareholder return)
annual_df["ROE"] = annual_df["Net_Income"] / annual_df["Equity"]

# Revenue Growth
annual_df = annual_df.sort_values(["Company_ID", "Year"])
annual_df["Revenue_Growth"] = annual_df.groupby("Company_ID")["Revenue"].pct_change()

print("Financial ratios calculated.")

# Save annual datset 
annual_df.to_csv("data/calculated_financial_dataset.csv", index=False)

print("Annual calculated dataset saved successfully.")
print("Final shape:", annual_df.shape)