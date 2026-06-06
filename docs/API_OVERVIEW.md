# API Overview

## Authentication

- POST `/auth/register`
- POST `/auth/login`
- GET `/auth/me`
- PUT `/auth/profile`

## Users

- GET `/users/`
- GET `/users/{user_id}`
- PUT `/users/{user_id}`
- DELETE `/users/{user_id}`

## Categories

- POST `/categories/`
- GET `/categories/`
- GET `/categories/{category_id}`
- PUT `/categories/{category_id}`
- DELETE `/categories/{category_id}`

## Products

- POST `/products/`
- GET `/products/`
- GET `/products/{product_id}`
- PUT `/products/{product_id}`
- DELETE `/products/{product_id}`

## Variants

- POST `/variants/`
- GET `/variants/`
- GET `/variants/{variant_id}`
- PUT `/variants/{variant_id}`
- DELETE `/variants/{variant_id}`

## Stock

- POST `/stock/add`
- POST `/stock/remove`
- GET `/stock/history`
- GET `/stock/low`

## Customers

- POST `/customers/`
- GET `/customers/`
- GET `/customers/{customer_id}`
- PUT `/customers/{customer_id}`
- DELETE `/customers/{customer_id}`

## Orders

- POST `/orders/`
- GET `/orders/`
- GET `/orders/{order_id}`

## Payments

- POST `/payments/`
- GET `/payments/`
- GET `/payments/{payment_id}`

## Invoices

- GET `/invoices/order/{order_id}`
- GET `/invoices/print/{order_id}`

## Reports

- GET `/reports/daily-sales`
- GET `/reports/monthly-sales`
- GET `/reports/profit`
- GET `/reports/top-products`
- GET `/reports/low-stock`

## AI Assistant

- POST `/ai/chat`

## Predictive Analytics

- GET `/ml/summary`
- GET `/ml/sales-forecast`
- GET `/ml/low-stock-prediction`
- GET `/ml/reorder-recommendations`
- GET `/ml/customer-segments`
- GET `/ml/product-recommendations`
- GET `/ml/product-recommendations/{customer_id}`
