import pandas as pd

def score_profit_margin(x):
    if x < 0:
        return 10
    elif x < 0.05:
        return 30
    elif x < 0.10:
        return 50
    elif x < 0.15:
        return 70
    elif x < 0.20:
        return 85
    else:
        return 100


def score_roe(x):
    if x < 0:
        return 10
    elif x < 0.05:
        return 30
    elif x < 0.10:
        return 50
    elif x < 0.15:
        return 70
    elif x < 0.20:
        return 85
    else:
        return 100


def score_growth(x):
    if pd.isna(x):
        return 50
    elif x < 0:
        return 20
    elif x < 0.05:
        return 50
    elif x < 0.10:
        return 70
    elif x < 0.15:
        return 85
    else:
        return 100


def score_debt(x):
    if x < 1:
        return 100
    elif x < 1.5:
        return 85
    elif x < 2:
        return 70
    elif x < 3:
        return 40
    else:
        return 20


def calculate_health(df):
    df["Profit_Score"] = df["Net_Profit_Margin"].apply(score_profit_margin)
    df["ROE_Score"] = df["ROE"].apply(score_roe)
    df["Growth_Score"] = df["Revenue_Growth"].apply(score_growth)
    df["Debt_Score"] = df["Debt_to_Equity"].apply(score_debt)

    df["Health_Score"] = (
        df["Profit_Score"] * 0.30 +
        df["ROE_Score"] * 0.25 +
        df["Growth_Score"] * 0.25 +
        df["Debt_Score"] * 0.20
    )

    def health_category(score):
        if score >= 80:
            return "Healthy"
        elif score >= 60:
            return "Moderate"
        elif score >= 40:
            return "At Risk"
        else:
            return "High Risk"

    df["Health_Status"] = df["Health_Score"].apply(health_category)

    return df