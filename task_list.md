# Task List: Smart Household Expense Manager

## Phase 1: Environment & Database Setup
- [ ] Initialize project directory and virtual environment.
- [ ] Create `requirements.txt` with necessary dependencies (`streamlit`, `mysql-connector-python`, `pandas`, `scikit-learn`, `pdfplumber`).
- [ ] Configure `.streamlit/secrets.toml` for secure database access.
- [ ] Develop `db_init.py` to create `household_db` and required tables (`categories`, `expenses`).

## Phase 2: Core Backend Logic
- [ ] Implement `utils/db_manager.py` for parameterized SQL operations (CRUD).
- [ ] Implement `utils/pdf_processor.py` using `pdfplumber` to extract expense data from bank statements.
- [ ] Implement `utils/forecaster.py` using `scikit-learn` (Linear Regression or Time Series) to predict month-end spending.

## Phase 3: Streamlit UI Development
- [ ] Setup `app.py` with sidebar navigation.
- [ ] **Module: Add Expense**
    - [ ] Create form for manual entry.
    - [ ] Implement category selection (fetched from DB).
- [ ] **Module: Dashboard**
    - [ ] Display expense metrics and category charts.
    - [ ] Integrate forecasting model with visual warnings for budget overruns.
- [ ] **Module: Smart Upload**
    - [ ] File uploader for PDF bank statements.
    - [ ] Data validation and bulk insertion logic.

## Phase 4: Refinement & Testing
- [ ] Add error handling for database connections and PDF parsing.
- [ ] Style the dashboard using Streamlit's layout features.
- [ ] Final end-to-end testing with sample data and PDFs.
