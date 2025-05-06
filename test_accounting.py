from python_accounting import Accounting

# Initialize the accounting system
accounting = Accounting()

# Add accounts
accounting.add_account("Cash", "Asset")
accounting.add_account("Revenue", "Income")
accounting.add_account("Operating Expenses", "Expense")
accounting.add_account("Contributed Capital", "Equity")
accounting.add_account("Retained Earnings", "Equity")

# Record transactions
# Example: Revenue transaction
accounting.record_transaction([
    {"account": "Cash", "debit": 1000},
    {"account": "Revenue", "credit": 1000}
])

# Example: Expense transaction
accounting.record_transaction([
    {"account": "Cash", "credit": 500},
    {"account": "Operating Expenses", "debit": 500}
])

# Example: Equity contribution
accounting.record_transaction([
    {"account": "Cash", "debit": 1000},
    {"account": "Contributed Capital", "credit": 1000}
])

# Print balances
print("Balances:", accounting.get_balances())
