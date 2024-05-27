import pandas as pd
import json
from utils import print_section_header, print_section_footer, initialize_colorama, format_currency

def load_data(file_path, skiprows=8):
    """Load the Excel file, skipping the specified number of rows."""
    return pd.read_excel(file_path, skiprows=skiprows)

def load_categories(json_path):
    """Load categories from a JSON file."""
    with open(json_path, 'r') as file:
        return json.load(file)

def assign_category(description, custom_categories):
    """Assign a category to a transaction based on its description."""
    description_lower = description.lower()
    print(f"    {description_lower}")
    for category, keywords in custom_categories.items():
        if any(keyword in description_lower for keyword in keywords):
            return category
    return 'Others'

def categorize_transactions(df, custom_categories):
    """Categorize transactions in the DataFrame."""
    print_section_header("Concepts")
    df['Category'] = df['Concepto'].apply(assign_category, args=(custom_categories,))
    print_section_footer()
    return df

def summarize_transactions(df):
    """Summarize categorized transactions, printing totals for each category."""
    expenses = df[df['Importe'] < 0]
    income = df[df['Importe'] > 0]

    print("\nCategorized Income:")
    for category, group in income.groupby('Category'):
        total = group['Importe'].sum()
        print(f"    {category}: {total:.2f} EUR")
    total_income = income['Importe'].sum()
    print(f"Total Income: {format_currency(total_income)}")

    print("\nCategorized Expenses:")
    for category, group in expenses.groupby('Category'):
        total = group['Importe'].sum()
        print(f"    {category}: {total:.2f} EUR")
    total_expenses = expenses['Importe'].sum()
    print(f"Total Expenses: {format_currency(total_expenses)}")

    total_savings = total_income + total_expenses
    print(f"\nTotal Savings: {format_currency(total_savings)}")

def save_categorized_data(df, output_path):
    """Save the categorized DataFrame to an Excel file."""
    df.to_excel(output_path, index=False)
    print(f"\nThe categorized file has been saved to: {output_path}")

def main():
    initialize_colorama()
    file_path = 'expenses.xls'
    json_path = 'categories.json'
    output_path = 'categorized_file.xlsx'

    df = load_data(file_path)
    custom_categories = load_categories(json_path)
    df = categorize_transactions(df, custom_categories)

    summarize_transactions(df)
    save_categorized_data(df, output_path)

if __name__ == "__main__":
    main()
