import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import streamlit as st
from utils.db_manager import execute_query


@st.cache_data(ttl=300)
def forecast_monthly_expense():
    """
    Predicts the month-end total expense using Linear Regression on this month's data.
    Cached for 5 minutes to avoid rerunning sklearn on every page rerun.
    """
    today     = datetime.now()
    first_day = today.replace(day=1)

    data = execute_query(
        "SELECT date, amount FROM expenses WHERE date >= %s",
        (first_day.strftime('%Y-%m-%d'),), fetch=True
    )

    if not data or len(data) < 2:
        return None, 0, 0

    df = pd.DataFrame(data)
    df['date']   = pd.to_datetime(df['date'])
    df['amount'] = df['amount'].astype(float)
    df['day']    = df['date'].dt.day

    daily_spend             = df.groupby('day')['amount'].sum().reset_index()
    daily_spend['cumulative'] = daily_spend['amount'].cumsum()

    X = daily_spend[['day']].values
    y = daily_spend['cumulative'].values

    model = LinearRegression()
    model.fit(X, y)

    last_day        = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    predicted_total = model.predict(np.array([[last_day.day]]))[0]
    current_total   = float(daily_spend['cumulative'].iloc[-1])

    return float(predicted_total), current_total, last_day.day


@st.cache_data(ttl=300)
def get_budget_status():
    """
    Returns budget, current spending, forecast and over-budget flag.
    Cached for 5 minutes — avoids re-querying DB + re-running sklearn on every rerun.
    """
    res          = execute_query("SELECT SUM(budget_limit) as total_budget FROM categories", fetch=True)
    total_budget = float(res[0]['total_budget']) if res and res[0]['total_budget'] else 0.0

    predicted_total, current_total, _ = forecast_monthly_expense()

    if predicted_total is None:
        predicted_safe = current_total
        is_over        = False
    else:
        predicted_safe = predicted_total
        is_over        = predicted_safe > total_budget

    return {
        'total_budget':    total_budget,
        'current_total':   current_total,
        'predicted_total': predicted_safe,
        'is_over_budget':  is_over,
    }


def clear_forecast_cache():
    """Call this after adding expenses so the forecast refreshes on next load."""
    forecast_monthly_expense.clear()
    get_budget_status.clear()