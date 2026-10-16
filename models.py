
from datetime import datetime


class Transaction:
    def __init__(
        self,
        transaction_id,
        title,
        amount,
        category,
        transaction_type,
        date
    ):
        self.transaction_id = str(transaction_id)
        self.title = title
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = date

        self.validation()

    def validation(self):
        if not self.transaction_id.strip():
            raise ValueError("Transaction ID cannot be empty.")

        if not self.title.strip():
            raise ValueError("Title cannot be empty.")

        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if not self.category.strip():
            raise ValueError("Category cannot be empty.")

        if self.transaction_type not in ("income", "expense"):
            raise ValueError("Transaction type must be income or expense.")

        try:
            parsed_date = datetime.strptime(self.date, "%Y-%m-%d")

            if parsed_date.strftime("%Y-%m-%d") != self.date:
                raise ValueError

        except (ValueError, TypeError):
            raise ValueError("Date must be in YYYY-MM-DD format.")

    def to_dict(self):
        return {
            "Transaction id": self.transaction_id,
            "Title": self.title,
            "Amount": self.amount,
            "Category": self.category,
            "Transaction type": self.transaction_type,
            "Date": self.date
        }

    def __str__(self):
        return (
            f'{self.transaction_id} | {self.title} | {self.amount} | '
            f'{self.category} | {self.transaction_type} | {self.date}'
        )


class Budget:
    def __init__(self, category, monthly_limit, month):
        self.category = category
        self.monthly_limit = monthly_limit
        self.month = month

        self.validation()

    def validation(self):
        if not self.category.strip():
            raise ValueError("Category cannot be empty.")

        if self.monthly_limit <= 0:
            raise ValueError("Monthly limit must be greater than zero.")

        try:
            parsed_month = datetime.strptime(self.month, "%Y-%m")

            if parsed_month.strftime("%Y-%m") != self.month:
                raise ValueError

        except (ValueError, TypeError):
            raise ValueError("Month must be in YYYY-MM format.")

    def to_dict(self):
        return {
            "Category": self.category,
            "Monthly Limit": self.monthly_limit,
            "Month": self.month
        }

    def __str__(self):
        return (
            f'{self.category} | {self.monthly_limit} | {self.month}'
        )
