
# Personal Finance Analyzer

A Python-based personal finance management project that helps users manage their income, expenses, and monthly budgets through a command-line interface.

## Features

- Add, view, search, update, and delete transactions
- Manage monthly budgets
- Generate monthly financial reports
- Generate category-wise expense reports
- Track expenses against budgets
- Filter transactions by month
- Validate transaction and budget data
- Store data in JSON files
- Unit tests using pytest

## Technologies Used

- Python
- JSON
- Object-Oriented Programming (OOP)
- pytest
- Git and GitHub

## Project Structure

```text
personal-finance-analyzer/
├── main.py
├── finance_manager.py
├── models.py
├── data/
│   ├── transactions.json
│   └── budgets.json
├── imports/
├── exports/
├── tests/
│   ├── test_models.py
│   └── test_finance_manager.py
├── .gitignore
└── README.md
```

## Requirements

- Python 3.12 or compatible version
- pytest for running tests

## How to Run

1. Clone or download this repository.
2. Open the project folder in the terminal.
3. Run the application:

```bash
python main.py
```

## Run Tests

Install pytest if it is not installed:

```bash
python -m pip install pytest
```

Run the tests:

```bash
python -m pytest -v
```

## Learning Outcomes

This project helped me practice Python functions, classes, input validation, JSON file handling, exception handling, CRUD operations, and automated testing.

## Author

Codingwithwajahat
