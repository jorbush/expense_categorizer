import pandas as pd
import json

file_path = 'expenses.xls'
df = pd.read_excel(file_path, skiprows=8)

with open('categories.json', 'r') as file:
    custom_categories = json.load(file)

def assign_category(description):
    description_lower = description.lower()
    print(f"    {description_lower}")
    for category, keywords in custom_categories.items():
        if any(keyword in description_lower for keyword in keywords):
            return category
    return 'Others'

def categorize_transactions(df):
    print("\nConcepts:")
    df['Category'] = df['Concepto'].apply(assign_category)
    return df

df = categorize_transactions(df)

expenses = df[df['Importe'] < 0]
income = df[df['Importe'] > 0]

print("\nCategorized Expenses:")
for category, group in expenses.groupby('Category'):
    total = group['Importe'].sum()
    print(f"    {category}: {total:.2f} EUR")
total_expenses = expenses['Importe'].sum()
print(f"Total Expenses: {total_expenses:.2f} EUR")

print("\nCategorized Income:")
for category, group in income.groupby('Category'):
    total = group['Importe'].sum()
    print(f"    {category}: {total:.2f} EUR")

total_income = income['Importe'].sum()
print(f"Total Income: {total_income:.2f} EUR")

total_savings = total_income + total_expenses
print(f"\nTotal Savings: {total_savings:.2f} EUR")

output_path = 'categorized_file.xlsx'
df.to_excel(output_path, index=False)
print(f"\nThe categorized file has been saved to: {output_path}")
