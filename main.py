import pandas as pd
import json
from utils import print_section_header, print_section_footer, initialize_colorama, format_currency
import sys

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
    income_summary = income.groupby('Category')['Importe'].sum().sort_values(ascending=False)
    total_income = income_summary.sum()
    for category, total in income_summary.items():
        percentage = (total / total_income) * 100
        print(f"    {category:.<40} {total:.2f} EUR ({percentage:.2f}%)")
    print(f"{'Total Income':.<44} {format_currency(total_income)}")

    print("\nCategorized Expenses:")
    expenses_summary = expenses.groupby('Category')['Importe'].sum().sort_values()
    total_expenses = expenses_summary.sum()
    for category, total in expenses_summary.items():
        percentage = (total / total_expenses) * 100
        print(f"    {category:.<40} {total:.2f} EUR ({percentage:.2f}%)")
    print(f"{'Total Expenses':.<44} {format_currency(total_expenses)}")

    total_savings = total_income + total_expenses
    print(f"\n{'Total Savings':.<44} {format_currency(total_savings)}")

def save_categorized_data(df, output_path):
    """Save the categorized DataFrame to an Excel file."""
    df.to_excel(output_path, index=False)
    print(f"\nThe categorized file has been saved to: {output_path}")

def main():
    initialize_colorama()
    file_path = sys.argv[1]
    json_path = 'categories.json'
    output_path = 'categorized_file.xlsx'

    df = load_data(file_path)
    custom_categories = load_categories(json_path)
    df = categorize_transactions(df, custom_categories)

    summarize_transactions(df)
    save_categorized_data(df, output_path)

if __name__ == "__main__":
    main()
