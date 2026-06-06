# Demo Guide

This guide explains how to run and demonstrate the Fashion Store Inventory & Sales Management API.

---

## 1. Start PostgreSQL

Make sure PostgreSQL is running and the database exists:

```text
fashion_store_db
```

---

## 2. Activate Virtual Environment

```bash
venv\Scripts\activate
```

---

## 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 4. Seed Demo Data

```bash
python seed_demo_data.py
```

This creates demo users, products, customers, orders, payments and analytics data.

---

## 5. Start Ollama for AI Assistant

Make sure Ollama is running.

Recommended model:

```bash
ollama run qwen2.5:3b
```

---

## 6. Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

## 7. Open Swagger API Docs

```text
http://127.0.0.1:8000/docs
```

Use Swagger to show:

- Auth login
- Categories
- Products
- Customers
- Orders
- Payments
- Reports
- AI Assistant
- Predictive Analytics

---

## 8. Open Frontend Login Page

```text
http://127.0.0.1:8000/site/login.html
```

Demo login:

```text
Email: admin.demo@gmail.com
Password: 123456
```

---

## 9. Open Dashboard

```text
http://127.0.0.1:8000/site/dashboard_v2.html
```

Dashboard demo flow:

1. Login as admin
2. Show dashboard overview
3. Show products
4. Show customers
5. Show orders
6. Show payments
7. Show reports
8. Show AI Assistant
9. Show Analytics

---

## 10. AI Assistant Demo Questions

Try these questions:

```text
Who bought products and paid?
Who still needs to pay?
Show today sales
How much profit did we make?
Which products should I restock?
Forecast next 7 days sales
Show customer insights
Recommend products for customer 1
```

---

## 11. Predictive Analytics Demo

Show these modules:

- Analytics Overview
- Sales Forecast
- Stock Risk Prediction
- Restock Plan
- Customer Insights
- Product Recommendations

---

## 12. Run Automated Tests

```bash
python -m pytest -v
```

Expected result:

```text
29 passed
```

---

## Best Demo Order for Interview

1. Explain project purpose
2. Show Swagger API docs
3. Login from frontend
4. Show dashboard modules
5. Create customer/product/order
6. Show payment and invoice
7. Show reports
8. Show AI Assistant
9. Show Predictive Analytics
10. Show automated test result

---

## Project Strength

This project demonstrates:

- FastAPI backend development
- PostgreSQL database design
- JWT authentication
- Role-based access control
- Real business workflow
- AI Assistant integration
- Predictive Analytics
- Frontend dashboard
- Automated testing
- Professional documentation
