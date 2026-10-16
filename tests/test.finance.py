
import json
import pytest
import finance_manager


@pytest.fixture
def setup_data(tmp_path, monkeypatch):
    transaction_file = tmp_path / "transactions.json"
    budget_file = tmp_path / "budgets.json"

    monkeypatch.setattr(
        finance_manager, "TRANSACTION_FILE", transaction_file
    )
    monkeypatch.setattr(
        finance_manager, "BUDGET_FILE", budget_file
    )

    finance_manager.transactions = []
    finance_manager.budgets = []
    finance_manager.transactions_file_valid = True
    finance_manager.budgets_file_valid = True

    yield

    finance_manager.transactions = []
    finance_manager.budgets = []
    finance_manager.transactions_file_valid = True
    finance_manager.budgets_file_valid = True


def test_add_transaction(setup_data, monkeypatch):
    inputs = iter([
        "Salary",
        "50000",
        "Job",
        "income",
        "2026-10-16"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    finance_manager.add_transaction()

    assert len(finance_manager.transactions) == 1
    assert finance_manager.transactions[0]["Title"] == "Salary"
    assert finance_manager.transactions[0]["Amount"] == 50000

    with open(finance_manager.TRANSACTION_FILE, encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 1


def test_search_transaction(setup_data, monkeypatch):
    finance_manager.transactions = [
        {
            "Transaction id": "1",
            "Title": "Salary",
            "Amount": 50000,
            "Category": "Job",
            "Transaction type": "income",
            "Date": "2026-10-16"
        }
    ]

    monkeypatch.setattr("builtins.input", lambda _: "1")

    result = finance_manager.search_transaction()

    assert result is not None
    assert result["Title"] == "Salary"


def test_search_transaction_not_found(setup_data, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "99")

    result = finance_manager.search_transaction()

    assert result is None


def test_delete_transaction(setup_data, monkeypatch):
    finance_manager.transactions = [
        {
            "Transaction id": "1",
            "Title": "Salary",
            "Amount": 50000,
            "Category": "Job",
            "Transaction type": "income",
            "Date": "2026-10-16"
        }
    ]

    monkeypatch.setattr("builtins.input", lambda _: "1")

    finance_manager.delete_transaction()

    assert len(finance_manager.transactions) == 0


def test_add_budget(setup_data, monkeypatch):
    inputs = iter(["Food", "15000", "2026-10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    finance_manager.add_budget()

    assert len(finance_manager.budgets) == 1
    assert finance_manager.budgets[0]["Category"] == "Food"
    assert finance_manager.budgets[0]["Monthly Limit"] == 15000

    with open(finance_manager.BUDGET_FILE, encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 1


def test_add_duplicate_budget(setup_data, monkeypatch):
    finance_manager.budgets = [
        {
            "Category": "Food",
            "Monthly Limit": 15000,
            "Month": "2026-10"
        }
    ]

    inputs = iter(["food", "20000", "2026-10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    finance_manager.add_budget()

    assert len(finance_manager.budgets) == 1
    assert finance_manager.budgets[0]["Monthly Limit"] == 15000


def test_delete_budget(setup_data, monkeypatch):
    finance_manager.budgets = [
        {
            "Category": "Food",
            "Monthly Limit": 15000,
            "Month": "2026-10"
        }
    ]

    inputs = iter(["Food", "2026-10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    finance_manager.delete_budget()

    assert len(finance_manager.budgets) == 0


def test_monthly_report(setup_data, monkeypatch, capsys):
    finance_manager.transactions = [
        {
            "Transaction id": "1",
            "Title": "Salary",
            "Amount": 50000,
            "Category": "Job",
            "Transaction type": "income",
            "Date": "2026-10-01"
        },
        {
            "Transaction id": "2",
            "Title": "Groceries",
            "Amount": 5000,
            "Category": "Food",
            "Transaction type": "expense",
            "Date": "2026-10-05"
        }
    ]

    monkeypatch.setattr("builtins.input", lambda _: "2026-10")

    finance_manager.monthly_report()

    output = capsys.readouterr().out

    assert "Total Income: 50000" in output
    assert "Total Expenses: 5000" in output
    assert "Remaining Balance: 45000" in output


def test_invalid_month(setup_data, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "2026-15")

    finance_manager.monthly_report()

    output = capsys.readouterr().out

    assert "valid month" in output
