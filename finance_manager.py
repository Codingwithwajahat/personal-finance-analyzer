from datetime import datetime
import json
from pathlib import Path
from itertools import count

from models import Transaction, Budget

DATA_FOLDER = Path("data")
TRANSACTION_FILE = DATA_FOLDER / "transactions.json"
BUDGET_FILE = DATA_FOLDER / "budgets.json"

DATA_FOLDER.mkdir(exist_ok=True)

transactions = []
budgets = []
transactions_file_valid = True
budgets_file_valid = True
transaction_counter = count(0)


def add_transaction():
    if not transactions_file_valid:
        print("Fix transactions.json before adding transactions.")
        return

    transaction_id = str(next(transaction_counter))
    title = input("Enter the title: ")

    try:
        amount = float(input("Enter the amount: "))
    except ValueError:
        print("Amount must be a number.")
        return

    category = input("Enter the category: ")
    transaction_type = input("Enter transaction type (income/expense): ")
    date = input("Enter date (YYYY-MM-DD): ")

    try:
        transaction = Transaction(
            transaction_id, title, amount, category, transaction_type, date
        )
        transactions.append(transaction.to_dict())

        if save_transactions():
            print(f"Transaction added successfully. ID: {transaction_id}")
        else:
            transactions.pop()

    except ValueError as error:
        print(f"Invalid data: {error}")


def view_transactions():
    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:
        print(transaction)


def search_transaction():
    user_id = input("Enter the transaction ID: ")

    for transaction in transactions:
        if transaction["Transaction id"] == user_id:
            print(transaction)
            return transaction

    print("Transaction ID not found.")
    return None


def update_transaction():
    if not transactions_file_valid:
        print("Fix transactions.json before updating transactions.")
        return

    user_id = input("Enter the transaction ID: ")

    for index, item in enumerate(transactions):
        if item["Transaction id"] == user_id:
            print("1. Title")
            print("2. Amount")
            print("3. Category")
            print("4. Transaction type")
            print("5. Date")

            option = input("Choose what to update: ")

            try:
                updated = Transaction(
                    item["Transaction id"],
                    item["Title"],
                    item["Amount"],
                    item["Category"],
                    item["Transaction type"],
                    item["Date"]
                )

                if option == "1":
                    updated.title = input("Enter the new title: ")
                elif option == "2":
                    updated.amount = float(input("Enter the new amount: "))
                elif option == "3":
                    updated.category = input("Enter the new category: ")
                elif option == "4":
                    updated.transaction_type = input(
                        "Enter transaction type (income/expense): "
                    )
                elif option == "5":
                    updated.date = input("Enter the new date (YYYY-MM-DD): ")
                else:
                    print("Invalid option.")
                    return

                updated.validation()

                old_transaction = transactions[index]
                transactions[index] = updated.to_dict()

                if save_transactions():
                    print("Transaction updated successfully.")
                else:
                    transactions[index] = old_transaction

                return

            except ValueError as error:
                print(f"Invalid data: {error}")
                return

    print("Transaction ID not found.")


def delete_transaction():
    if not transactions_file_valid:
        print("Fix transactions.json before deleting transactions.")
        return

    user_id = input("Enter the transaction ID: ")

    for index, item in enumerate(transactions):
        if item["Transaction id"] == user_id:
            transactions.pop(index)

            if save_transactions():
                print("Transaction deleted successfully.")
            else:
                transactions.insert(index, item)

            return

    print("Transaction ID not found.")


def add_budget():
    if not budgets_file_valid:
        print("Fix budgets.json before adding budgets.")
        return

    category = input("Enter the category: ")

    try:
        monthly_limit = float(input("Enter the monthly limit: "))
    except ValueError:
        print("Monthly limit must be a number.")
        return

    month = input("Enter the month (YYYY-MM): ")

    for item in budgets:
        if (
            item["Category"].lower() == category.lower()
            and item["Month"] == month
        ):
            print("A budget already exists for this category and month.")
            return

    try:
        budget = Budget(category, monthly_limit, month)
        budgets.append(budget.to_dict())

        if save_budgets():
            print("Budget added successfully.")
        else:
            budgets.pop()

    except ValueError as error:
        print(f"Invalid budget: {error}")


def view_budgets():
    if not budgets:
        print("No budgets found.")
        return

    for budget in budgets:
        print(budget)


def update_budget():
    if not budgets_file_valid:
        print("Fix budgets.json before updating budgets.")
        return

    category = input("Enter the category: ")
    month = input("Enter the month (YYYY-MM): ")

    for index, item in enumerate(budgets):
        if (
            item["Category"].lower() == category.lower()
            and item["Month"] == month
        ):
            try:
                monthly_limit = float(
                    input("Enter the new monthly limit: ")
                )

                updated = Budget(
                    item["Category"],
                    monthly_limit,
                    item["Month"]
                )

                budgets[index] = updated.to_dict()

                if save_budgets():
                    print("Budget updated successfully.")
                else:
                    budgets[index] = item

            except ValueError as error:
                print(f"Invalid budget: {error}")

            return

    print("Budget not found.")


def delete_budget():
    if not budgets_file_valid:
        print("Fix budgets.json before deleting budgets.")
        return

    category = input("Enter the category: ")
    month = input("Enter the month (YYYY-MM): ")

    for index, item in enumerate(budgets):
        if (
            item["Category"].lower() == category.lower()
            and item["Month"] == month
        ):
            budgets.pop(index)

            if save_budgets():
                print("Budget deleted successfully.")
            else:
                budgets.insert(index, item)

            return

    print("Budget not found.")


def monthly_report():
    month = input("Enter the month (YYYY-MM): ")

    if not valid_month(month):
        print("Enter a valid month in YYYY-MM format.")
        return

    total_income = 0
    total_expense = 0
    found = False

    for item in transactions:
        if item["Date"][:7] == month:
            found = True

            if item["Transaction type"] == "income":
                total_income += item["Amount"]
            else:
                total_expense += item["Amount"]

    if not found:
        print("Month transactions not found.")
        return

    balance = total_income - total_expense

    print(f"""
Month: {month}
Total Income: {total_income}
Total Expenses: {total_expense}
Remaining Balance: {balance}
""")


def category_expense_report():
    month = input("Enter the month (YYYY-MM): ")

    if not valid_month(month):
        print("Enter a valid month in YYYY-MM format.")
        return

    expenses = {}

    for item in transactions:
        if (
            item["Transaction type"] == "expense"
            and item["Date"][:7] == month
        ):
            category = item["Category"]

            if category not in expenses:
                expenses[category] = item["Amount"]
            else:
                expenses[category] += item["Amount"]

    if not expenses:
        print("No expense category found for this month.")
        return

    total_expenses = 0

    for category, amount in expenses.items():
        print(f"{category}: {amount}")
        total_expenses += amount

    print(f"Total Expenses: {total_expenses}")


def budget_tracking():
    month = input("Enter the month (YYYY-MM): ")

    if not valid_month(month):
        print("Enter a valid month in YYYY-MM format.")
        return

    found = False

    for budget in budgets:
        if budget["Month"] == month:
            found = True
            spent = 0

            for item in transactions:
                if (
                    item["Category"].lower() == budget["Category"].lower()
                    and item["Date"][:7] == month
                    and item["Transaction type"] == "expense"
                ):
                    spent += item["Amount"]

            monthly_budget = budget["Monthly Limit"]
            remaining = monthly_budget - spent

            if spent > monthly_budget:
                status = "Budget Exceeded"
                over_budget = spent - monthly_budget
            else:
                status = "Within Budget"
                over_budget = 0

            print(f"""
Category: {budget["Category"]}
Monthly Budget: {monthly_budget}
Total Spent: {spent}
Remaining Amount: {remaining}
Status: {status}
Over Budget By: {over_budget}
""")

    if not found:
        print("No budgets found for this month.")


def filter_transactions_by_month():
    month = input("Enter the month (YYYY-MM): ")

    if not valid_month(month):
        print("Enter a valid month in YYYY-MM format.")
        return

    found = False

    for item in transactions:
        if item["Date"][:7] == month:
            print(item)
            found = True

    if not found:
        print("Month transactions not found.")


def valid_month(month):
    try:
        return datetime.strptime(month, "%Y-%m").strftime("%Y-%m") == month
    except (ValueError, TypeError):
        return False


def load_transactions():
    global transactions, transactions_file_valid

    if not TRANSACTION_FILE.exists():
        transactions = []
        transactions_file_valid = True
        return

    try:
        with open(TRANSACTION_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("transactions.json must contain a list.")

        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Invalid transaction record.")

            transaction = Transaction(
                item["Transaction id"],
                item["Title"],
                item["Amount"],
                item["Category"],
                item["Transaction type"],
                item["Date"]
            )

        transactions = data
        transactions_file_valid = True

    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError):
        transactions = []
        transactions_file_valid = False
        print("Error: transactions.json is invalid. Fix the file before making changes.")


def load_budgets():
    global budgets, budgets_file_valid

    if not BUDGET_FILE.exists():
        budgets = []
        budgets_file_valid = True
        return

    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("budgets.json must contain a list.")

        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Invalid budget record.")

            budget = Budget(
                item["Category"],
                item["Monthly Limit"],
                item["Month"]
            )

        budgets = data
        budgets_file_valid = True

    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError):
        budgets = []
        budgets_file_valid = False
        print("Error: budgets.json is invalid. Fix the file before making changes.")


def save_transactions():
    if not transactions_file_valid:
        print("Transactions file is invalid. Changes were not saved.")
        return False

    try:
        with open(TRANSACTION_FILE, "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)

        return True

    except OSError as error:
        print(f"Could not save transactions: {error}")
        return False


def save_budgets():
    if not budgets_file_valid:
        print("Budgets file is invalid. Changes were not saved.")
        return False

    try:
        with open(BUDGET_FILE, "w", encoding="utf-8") as file:
            json.dump(budgets, file, indent=4)

        return True

    except OSError as error:
        print(f"Could not save budgets: {error}")
        return False


load_transactions()
load_budgets()

transaction_counter = count(
    max(
        (int(item["Transaction id"]) for item in transactions),
        default=-1
    ) + 1
)
