import pandas as pd

# Load raw dataset
df_original = pd.read_csv("data/financial_dataset.csv")  
print("Original column names:")
print(df_original.columns.tolist())

# Creating a working copy so raw dataset remains unchanged
df = df_original.copy()
# preview 
print(df.head())

#Selecting only the columns required for KPI calculations
columns_to_keep = [
    'Year', 'Quarter', 'Company_ID', 'Revenue', 'Expenses', 
    'Net_Income', 'Assets', 'Liabilities', 'Equity', 'Cash_Flow'
]
df = df[columns_to_keep]
# Verifying that only selected columns remain
print(df.columns)


# Converting financial columns to numeric format.
numeric_cols = ['Revenue', 'Expenses', 'Net_Income', 'Assets', 'Liabilities', 'Equity', 'Cash_Flow']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')  #any invalid values are turned into NaN

# Removing incomplete financial records
df = df.dropna(subset=numeric_cols)
# Removing duplicate entries
df = df.drop_duplicates()

#Removing unrealistic or invalid financial values that could distort KPIs
df = df[
    (df['Revenue'] > 0) &
    (df['Expenses'] >= 0) &
    (df['Assets'] > 0) &
    (df['Equity'] != 0)
]
# Sort dataset by Company, Year, and Quarter
df = df.sort_values(by=['Company_ID', 'Year', 'Quarter']).reset_index(drop=True)

# Save cleaned working dataset 
df.to_csv("data/cleaned_financial_dataset.csv", index=False)

# verification 
print("Data cleaning complete. Cleaned dataset saved as 'cleaned_financial_dataset.csv'.")
print("Cleaned dataset shape:", df.shape)
print("Original dataset shape:", df_original.shape)
print("Columns available in working dataset:", df.columns.tolist())
