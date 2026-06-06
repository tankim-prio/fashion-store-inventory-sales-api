# AI Assistant and Predictive Analytics

This project includes a local AI Assistant and Predictive Analytics engine for fashion store business intelligence.

---

## AI Assistant

The AI Assistant helps users ask business questions in natural language.

Example questions:

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

## AI Assistant Design

The AI system uses:

- Fast rule-based intent detection
- Local Ollama model
- Safe SQLAlchemy database queries
- Structured table and metric responses
- Predictive Analytics integration

---

## Ollama Model

Recommended local model:

```text
qwen2.5:3b
```

The AI Assistant works locally and does not require a paid API.

---

## Predictive Analytics Modules

### Analytics Overview

Shows the overall business intelligence summary.

### Sales Forecast

Predicts upcoming sales using recent sales trends.

### Stock Risk Prediction

Finds products that may run out soon.

### Restock Plan

Suggests which products should be bought again, how many pieces are needed, and estimated buying budget.

### Customer Insights

Analyzes customers using:

- Purchase count
- Total spending
- Last purchase date

### Product Recommendations

Suggests products using:

- Sales popularity
- Stock availability
- Customer purchase history
