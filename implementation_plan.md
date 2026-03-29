# Implementation Plan: Smart Household Expense Manager

## 1. Project Overview
A Streamlit-based application to manage household finances, featuring automated PDF expense extraction and AI-driven spending forecasts.

## 2. Technical Stack
- **Frontend:** Streamlit (v1.x)
- **Database:** MySQL (hosted on localhost via XAMPP/Workbench)
- **Data Processing:** Pandas, PDFPlumber
- **AI/Forecasting:** Scikit-learn (Linear Regression)
- **Security:** `st.secrets` for credentials, parameterized queries for SQL.

## 3. Database Schema
### Table: `categories`
- `id`: INT (Primary Key, Auto-increment)
- `name`: VARCHAR(255) (Unique)
- `budget_limit`: DECIMAL(10, 2)

### Table: `expenses`
- `id`: INT (Primary Key, Auto-increment)
- `date`: DATE
- `category`: VARCHAR(255)
- `amount`: DECIMAL(10, 2)
- `description`: TEXT
- `raw_text_source`: TEXT (Stores raw text from PDF for auditing)

## 4. Application Architecture
- `app.py`: Main entry point handling the UI state and page routing.
- `db_init.py`: One-time setup script for database and table creation.
- `utils/`:
    - `db_manager.py`: Centralized module for database connectivity and query execution.
    - `pdf_processor.py`: Logic to parse bank statements and map them to the schema.
    - `forecaster.py`: Trains a simple regression model on historical data to predict current month's total.

## 5. Feature Breakdown

### A. Smart Forecast (AI)
- **Logic:** Aggregate daily/weekly expenses.
- **Model:** Use `scikit-learn.linear_model.LinearRegression` to project the trend line to the last day of the current month.
- **Alert:** Compare `predicted_total` vs `budget_limit`. Display a `st.error` or "Red Warning" if predicted > budget.

### B. PDF Statement Parser
- **Tool:** `pdfplumber`.
- **Workflow:** Upload PDF -> Extract text -> Regex matching for Dates, Descriptions, and Amounts -> Preview extracted rows -> Save to MySQL.

### C. Dashboard
- **Visuals:** Use `st.metric` for total spend vs total budget.
- **Charts:** Use `st.bar_chart` or `st.plotly_chart` for category-wise distribution.

## 6. Security & Best Practices
- **Credentials:** Stored in `.streamlit/secrets.toml`.
- **SQL Safety:** Use `%s` placeholders in `mysql-connector-python` to prevent SQL injection.
- **Modularity:** Separate UI components from business logic.
