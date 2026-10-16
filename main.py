
import finance_manager


while True:
    print("""
===== Personal Finance Analyzer =====

1. Add Transaction
2. View Transactions
3. Search Transaction
4. Update Transaction
5. Delete Transaction
6. Add Budget
7. View Budgets
8. Update Budget
9. Delete Budget
10. Monthly Financial Report
11. Category-wise Expense Report
12. Budget Tracking
13. Filter Transactions by Month
14. Exit
""")

    choice = input("Enter your choice: ")

    if choice == "1":
        finance_manager.add_transaction()

    elif choice == "2":
        finance_manager.view_transactions()

    elif choice == "3":
        finance_manager.search_transaction()

    elif choice == "4":
        finance_manager.update_transaction()

    elif choice == "5":
        finance_manager.delete_transaction()

    elif choice == "6":
        finance_manager.add_budget()

    elif choice == "7":
        finance_manager.view_budgets()

    elif choice == "8":
        finance_manager.update_budget()

    elif choice == "9":
        finance_manager.delete_budget()

    elif choice == "10":
        finance_manager.monthly_report()

    elif choice == "11":
        finance_manager.category_expense_report()

    elif choice == "12":
        finance_manager.budget_tracking()

    elif choice == "13":
        finance_manager.filter_transactions_by_month()

    elif choice == "14":
        print("You chose Exit.")
        break

    else:
        print("Enter a valid choice.")
