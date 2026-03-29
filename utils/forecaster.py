import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from utils.db_manager import execute_query

def forecast_monthly_expense():
    """
    Predicts the month-end total expense based on current month's spending trend.
    """
    today = datetime.now()
    first_day = today.replace(day=1)

    # Query current month expenses
    query = "SELECT date, amount FROM expenses WHERE date >= %s"
    data = execute_query(query, (first_day.strftime('%Y-%m-%d'),), fetch=True)

    if not data or len(data) < 2:
        return None, 0, 0

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.day

    # Group by day to get daily totals
    daily_spend = df.groupby('day')['amount'].sum().reset_index()
    daily_spend['cumulative'] = daily_spend['amount'].cumsum()

    # Prepare data for Linear Regression
    X = daily_spend[['day']].values
    y = daily_spend['cumulative'].values

    model = LinearRegression()
    model.fit(X, y)

    # Predict for the last day of the month
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    prediction_day = np.array([[last_day.day]])
    predicted_total = model.predict(prediction_day)[0]

    current_total = daily_spend['cumulative'].iloc[-1]

    return predicted_total, current_total, last_day.day

def get_budget_status():
    """Compares forecasted total with total budget limit."""
    query = "SELECT SUM(budget_limit) as total_budget FROM categories"
    res = execute_query(query, fetch=True)
    total_budget = res[0]['total_budget'] if res and res[0]['total_budget'] else 0

    predicted_total, current_total, _ = forecast_monthly_expense()

    # FIX: check for None before calling float() to avoid a TypeError crash
    if predicted_total is None:
        predicted_total_safe = float(current_total)
        is_over_budget = False
    else:
        predicted_total_safe = float(predicted_total)
        is_over_budget = predicted_total_safe > float(total_budget)

    return {
        'total_budget': float(total_budget),
        'current_total': float(current_total),
        'predicted_total': predicted_total_safe,
        'is_over_budget': is_over_budget
    }