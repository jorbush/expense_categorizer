import pandas as pd

file_path = 'expenses.xls'
df = pd.read_excel(file_path, skiprows=8)

print(f"Original Data:\n{df}")
print(f"Columns:\n{df.columns}")

def categorize_transactions(df):
    custom_categories = {
        'Supermarket': ['mercadona', 'carrefour'],
        'Entertainment': ['netflix', 'spotify'],
        'Restaurants': ['mcdonalds', 'starbucks'],
    }

    def assign_category(description):
        description_lower = description.lower()
        print(description_lower)
        for category, keywords in custom_categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        return 'Others'

    df['Category'] = df['Concepto'].apply(assign_category)
    return df

df = categorize_transactions(df)

expenses = df[df['Importe'] < 0]
income = df[df['Importe'] > 0]

print("Categorized Expenses:")
print(expenses.groupby('Category').sum())

print("\nCategorized Income:")
print(income.groupby('Category').sum())


total_income = income['Importe'].sum()
total_expenses = expenses['Importe'].sum()
print(f"\nTotal Income: {total_income:.2f} EUR")
print(f"Total Expenses: {total_expenses:.2f} EUR")
total_savings = total_income + total_expenses
print(f"\nTotal Savings: {total_savings:.2f} EUR")


# Optional: Save the result to a new Excel file
output_path = 'categorized_file.xlsx'
df.to_excel(output_path, index=False)
print(f"\nThe categorized file has been saved to: {output_path}")
