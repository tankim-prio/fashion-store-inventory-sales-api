# Testing Guide

This project uses Pytest and FastAPI TestClient for automated backend testing.

---

## Test Coverage

The test suite covers:

- Authentication
- Protected routes
- Categories
- Products
- Customers
- Product variants
- Stock management
- AI Assistant
- Predictive Analytics

---

## Run Demo Seed Data

Before running tests, seed the database with demo data:

```bash
python seed_demo_data.py
```

---

## Run All Tests

```bash
python -m pytest -v
```

Expected result:

```text
29 passed
```

---

## Test Files

```text
tests/
├── conftest.py
├── test_auth.py
├── test_categories_products.py
├── test_customers.py
├── test_variants_stock.py
├── test_predictive_analytics.py
└── test_ai_assistant_analytics.py
```

---

## Notes

The tests are written to work with an existing database and demo seed data.

The test suite uses:

- Real JWT login
- Real admin token
- Unique test data
- Stable repeated test execution

Warnings from third-party packages are not project failures.
