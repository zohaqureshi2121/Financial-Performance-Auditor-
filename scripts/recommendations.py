import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("data/financial_dataset_with_health.csv")
print("Dataset loaded:", df.shape)

# Replace inf values
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Calculate dataset medians 
median_npm = df["Net_Profit_Margin"].median()
median_roe = df["ROE"].median()
median_growth = df["Revenue_Growth"].median()
median_de = df["Debt_to_Equity"].median()

print("Dataset medians calculated.")

# Helper Classification Functions

def classify_npm(npm):
    if npm < 0.05:
        return "weak"
    elif npm < 0.15:
        return "moderate"
    else:
        return "strong"

def classify_roe(roe):
    if roe < 0.10:
        return "weak"
    elif roe < 0.20:
        return "moderate"
    else:
        return "strong"

def classify_growth(growth):
    if pd.isna(growth):
        return "not available"
    elif growth < 0:
        return "declining"
    elif growth < 0.10:
        return "stable"
    else:
        return "high growth"

def classify_de(de):
    if de > 2:
        return "aggressive leverage"
    elif de >= 1:
        return "balanced leverage"
    else:
        return "conservative leverage"

# Generate Recommendation

def generate_recommendation(row):
    npm = row["Net_Profit_Margin"]
    roe = row["ROE"]
    growth = row["Revenue_Growth"]
    de = row["Debt_to_Equity"]
    health_status = row["Health_Status"]

    npm_class = classify_npm(npm)
    roe_class = classify_roe(roe)
    growth_class = classify_growth(growth)
    de_class = classify_de(de)

    text = ""

    # Profitability
    text += f"Net Profit Margin ({npm*100:.2f}%) is {npm_class}."
    if npm < median_npm:
        text += "It is below industry median, indicating scope for cost optimization and pricing strategy improvement. "
    else:
        text += "It exceeds industry median, reflecting efficient cost control. "

    # ROE
    text += f"ROE ({roe*100:.2f}%) is {roe_class}."
    if roe < median_roe:
        text += "Capital efficiency can be improved through better asset utilization. "
    else:
        text += "Shareholder return performance is competitive. "

    # Growth
    if pd.isna(growth):
        text += "Revenue Growth is not available for base year analysis. "
    else:
        text += f"Revenue Growth ({growth*100:.2f}%) is {growth_class}."
        if growth < median_growth:
            text += "Growth strategy should be strengthened through market expansion or product diversification. "
        else:
            text += "Revenue expansion is aligned with industry performance. "

    # Debt
    text += f"Debt-to-Equity ratio ({de:.2f}) indicates {de_class}."
    if de > median_de:
        text += "Debt levels should be monitored to maintain financial stability. "
    else:
        text += "Capital structure remains financially controlled. "

    # Final Strategic Direction
    if health_status == "High Risk":
        text += "Overall financial health indicates significant risk, requiring immediate restructuring and cost rationalization."
    elif health_status == "At Risk":
        text += "Overall performance requires operational improvements to strengthen financial stability."
    elif health_status == "Moderate":
        text += "Financial position is stable with opportunities for strategic performance enhancement."
    else:
        text += "Company demonstrates strong financial health and is positioned for sustainable expansion."

    return text

# Apply recommendations
df["Final_Recommendations"] = df.apply(generate_recommendation, axis=1)

# Save file
df.to_csv("data/financial_dataset_with_recommendations.csv", index=False)
print("Recommendations generated successfully.")
print("Final shape:", df.shape)