
import pytest

from models import Transaction, Budget


def test_create_transaction():
    transaction = Transaction(
        "1",
        "Salary",
        50000,
        "Job",
        "income",
        "2026-10-16"
    )

    assert transaction.title == "Salary"
    assert transaction.amount == 50000
    assert transaction.category == "Job"
    assert transaction.transaction_type == "income"


def test_transaction_to_dict():
    transaction = Transaction(
        "1",
        "Salary",
        50000,
        "Job",
        "income",
        "2026-10-16"
    )

    data = transaction.to_dict()

    assert data["Transaction id"] == "1"
    assert data["Title"] == "Salary"
    assert data["Amount"] == 50000


def test_transaction_string():
    transaction = Transaction(
        "1",
        "Salary",
        50000,
        "Job",
        "income",
        "2026-10-16"
    )

    assert "Salary" in str(transaction)


def test_empty_transaction_title():
    with pytest.raises(ValueError):
        Transaction(
            "1",
            "",
            50000,
            "Job",
            "income",
            "2026-10-16"
        )


def test_negative_transaction_amount():
    with pytest.raises(ValueError):
        Transaction(
            "1",
            "Salary",
            -500,
            "Job",
            "income",
            "2026-10-16"
        )


def test_invalid_transaction_type():
    with pytest.raises(ValueError):
        Transaction(
            "1",
            "Salary",
            50000,
            "Job",
            "other",
            "2026-10-16"
        )


def test_invalid_transaction_date():
    with pytest.raises(ValueError):
        Transaction(
            "1",
            "Salary",
            50000,
            "Job",
            "income",
            "16-10-2026"
        )


def test_create_budget():
    budget = Budget(
        "Food",
        15000,
        "2026-10"
    )

    assert budget.category == "Food"
    assert budget.monthly_limit == 15000
    assert budget.month == "2026-10"


def test_budget_to_dict():
    budget = Budget(
        "Food",
        15000,
        "2026-10"
    )

    data = budget.to_dict()

    assert data["Category"] == "Food"
    assert data["Monthly Limit"] == 15000
    assert data["Month"] == "2026-10"


def test_empty_budget_category():
    with pytest.raises(ValueError):
        Budget(
            "",
            15000,
            "2026-10"
        )


def test_negative_budget_limit():
    with pytest.raises(ValueError):
        Budget(
            "Food",
            -100,
            "2026-10"
        )


def test_invalid_budget_month():
    with pytest.raises(ValueError):
        Budget(
            "Food",
            15000,
            "2026-15"
        )
