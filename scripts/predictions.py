import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from health_scoring import calculate_health   

# Load & Sort Data
df = pd.read_csv("data/financial_dataset_with_recommendations.csv")
df = df.sort_values(by=["Company_ID", "Year"])

latest_year = df["Year"].max()
print("Latest Year in Dataset:", latest_year)

# Create Next Year Targets
df["Revenue_next"] = df.groupby("Company_ID")["Revenue"].shift(-1)
df["Net_Income_next"] = df.groupby("Company_ID")["Net_Income"].shift(-1)
df["Liabilities_next"] = df.groupby("Company_ID")["Liabilities"].shift(-1)
df["Equity_next"] = df.groupby("Company_ID")["Equity"].shift(-1)  # New target for Equity prediction

df_model = df.dropna(subset=["Revenue_next", "Net_Income_next", "Liabilities_next", "Equity_next"])

# Train/Test Split
train_data = df_model[df_model["Year"] < latest_year]
test_data = df_model[df_model["Year"] == latest_year - 1]

features = [
    "Revenue",
    "Net_Income",
    "Liabilities",
    "Assets",
    "Equity",
    "Cash_Flow"
]

# Input features
X_train = train_data[features]
X_test = test_data[features]

# Targets for train/test
y_train_rev = train_data["Revenue_next"]
y_train_inc = train_data["Net_Income_next"]
y_train_liab = train_data["Liabilities_next"]
y_train_eq = train_data["Equity_next"]  

y_test_rev = test_data["Revenue_next"]
y_test_inc = test_data["Net_Income_next"]
y_test_liab = test_data["Liabilities_next"]
y_test_eq = test_data["Equity_next"] 

# Train Models
model_rev = LinearRegression()
model_inc = LinearRegression()
model_liab = LinearRegression()
model_eq = LinearRegression()  

# Fit models
model_rev.fit(X_train, y_train_rev)
model_inc.fit(X_train, y_train_inc)
model_liab.fit(X_train, y_train_liab)
model_eq.fit(X_train, y_train_eq)

# Validate on Latest Year
print("\nValidation Results:")

pred_rev_val = model_rev.predict(X_test)
pred_inc_val = model_inc.predict(X_test)
pred_liab_val = model_liab.predict(X_test)
pred_eq_val = model_eq.predict(X_test)

print("Revenue MAE:", mean_absolute_error(y_test_rev, pred_rev_val))
print("Net Income MAE:", mean_absolute_error(y_test_inc, pred_inc_val))
print("Liabilities MAE:", mean_absolute_error(y_test_liab, pred_liab_val))
print("Equity MAE:", mean_absolute_error(y_test_eq, pred_eq_val))

# Retrain on Full Data
X_full = df_model[features]

model_rev.fit(X_full, df_model["Revenue_next"])
model_inc.fit(X_full, df_model["Net_Income_next"])
model_liab.fit(X_full, df_model["Liabilities_next"])
model_eq.fit(X_full, df_model["Equity_next"])

# Predict Next Year
df_latest = df[df["Year"] == latest_year]
X_latest = df_latest[features]

pred_rev = model_rev.predict(X_latest)
pred_inc = model_inc.predict(X_latest)
pred_liab = model_liab.predict(X_latest)
pred_eq = model_eq.predict(X_latest)

# Build Prediction DataFrame
pred_df = df_latest[["Company_ID"]].copy()  
pred_df["Year"] = latest_year + 1
pred_df["Revenue"] = pred_rev
pred_df["Net_Income"] = pred_inc
pred_df["Liabilities"] = pred_liab
pred_df["Equity"] = pred_eq  

# Recalculate Financial Ratios
pred_df["Net_Profit_Margin"] = pred_df["Net_Income"] / pred_df["Revenue"]
pred_df["Debt_to_Equity"] = pred_df["Liabilities"] / pred_df["Equity"]
pred_df["ROE"] = pred_df["Net_Income"] / pred_df["Equity"]
pred_df["Revenue_Growth"] = (
    (pred_df["Revenue"] - df_latest["Revenue"].values)
    / df_latest["Revenue"].values
)

# Apply Health Scoring
pred_df = calculate_health(pred_df)

# Save Predictions
pred_df.to_csv("data/financial_predictions_2025.csv", index=False)

print("\nPredictions saved to: data/financial_predictions_2025.csv")
print(pred_df.head())