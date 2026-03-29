from fpdf import FPDF
from utils.db_manager import execute_query
from datetime import datetime
import os
import platform


def _setup_font(pdf):
    """
    Add a Unicode-capable font that works on both Windows and Linux.

    Strategy:
    1. Windows → use Arial from C:\\Windows\\Fonts
    2. Linux (Streamlit Cloud) → use DejaVuSans from the fonts/ folder in the project
    3. Fallback → use helvetica (no ₹ but won't crash)

    For Linux/Streamlit Cloud, add a fonts/ folder to your project root
    containing DejaVuSans.ttf, DejaVuSans-Bold.ttf, DejaVuSans-Oblique.ttf
    Download from: https://dejavu-fonts.github.io/
    """
    system = platform.system()

    # ── Windows ──────────────────────────────────────────────────
    if system == "Windows":
        win_fonts = r"C:\Windows\Fonts"
        try:
            pdf.add_font('mainfont', '',  os.path.join(win_fonts, 'arial.ttf'),   uni=True)
            pdf.add_font('mainfont', 'B', os.path.join(win_fonts, 'arialbd.ttf'), uni=True)
            pdf.add_font('mainfont', 'I', os.path.join(win_fonts, 'ariali.ttf'),  uni=True)
            return 'mainfont'
        except Exception:
            pass

    # ── Linux / Mac (Streamlit Cloud) ────────────────────────────
    # Look for DejaVuSans in a fonts/ folder next to this file or in project root
    possible_dirs = [
        os.path.join(os.path.dirname(__file__), '..', 'fonts'),  # utils/../fonts/
        os.path.join(os.path.dirname(__file__), 'fonts'),        # utils/fonts/
        os.path.join(os.getcwd(), 'fonts'),                      # project root/fonts/
    ]
    for font_dir in possible_dirs:
        regular = os.path.join(font_dir, 'DejaVuSans.ttf')
        bold    = os.path.join(font_dir, 'DejaVuSans-Bold.ttf')
        if os.path.exists(regular):
            try:
                pdf.add_font('mainfont', '',  regular, uni=True)
                pdf.add_font('mainfont', 'B', bold if os.path.exists(bold) else regular, uni=True)
                return 'mainfont'
            except Exception:
                pass

    # ── Fallback: helvetica (no ₹ support, but won't crash) ──────
    return 'helvetica'


class ExpenseReport(FPDF):
    font_name = 'helvetica'  # overwritten after font setup

    def header(self):
        self.set_font(self.font_name, 'B', 15)
        self.cell(0, 10, 'Monthly Expense Report', border=0, new_x='LMARGIN', new_y='NEXT', align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.font_name, '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', border=0, align='C')


def generate_pdf_report(month, year):
    # ── Fetch data ──────────────────────────────────────────────
    expenses = execute_query(
        "SELECT date, category, amount, description FROM expenses "
        "WHERE MONTH(date) = %s AND YEAR(date) = %s ORDER BY date ASC",
        (month, year), fetch=True
    )
    budget_res   = execute_query("SELECT SUM(budget_limit) as total_budget FROM categories", fetch=True)
    total_budget = float(budget_res[0]['total_budget']) if budget_res and budget_res[0]['total_budget'] else 0.0
    total_spent  = sum(float(e['amount']) for e in expenses) if expenses else 0.0
    month_name   = datetime(year, month, 1).strftime('%B')

    # ── Create PDF ───────────────────────────────────────────────
    pdf = ExpenseReport()
    font = _setup_font(pdf)
    pdf.font_name = font  # share with header/footer

    pdf.add_page()

    # ── Summary ──────────────────────────────────────────────────
    pdf.set_font(font, 'B', 12)
    pdf.cell(0, 10, f'Period: {month_name} {year}', border=0, new_x='LMARGIN', new_y='NEXT')
    pdf.ln(2)

    pdf.set_font(font, '', 11)
    pdf.set_fill_color(240, 242, 246)

    pdf.cell(90, 10, 'Total Budget:', border=1, new_x='RIGHT', new_y='TOP', align='L', fill=True)
    pdf.cell(90, 10, f'Rs. {total_budget:,.2f}', border=1, new_x='LMARGIN', new_y='NEXT', align='R')

    pdf.cell(90, 10, 'Total Spent:', border=1, new_x='RIGHT', new_y='TOP', align='L', fill=True)
    pdf.cell(90, 10, f'Rs. {total_spent:,.2f}', border=1, new_x='LMARGIN', new_y='NEXT', align='R')

    status = 'UNDER BUDGET' if total_spent <= total_budget else 'OVER BUDGET'
    pdf.set_font(font, 'B', 11)
    pdf.set_text_color(*(200, 0, 0) if status == 'OVER BUDGET' else (0, 128, 0))
    pdf.cell(90, 10, 'Status:', border=1, new_x='RIGHT', new_y='TOP', align='L', fill=True)
    pdf.cell(90, 10, status, border=1, new_x='LMARGIN', new_y='NEXT', align='R')
    pdf.set_text_color(0, 0, 0)

    pdf.ln(10)

    # ── Table header ─────────────────────────────────────────────
    pdf.set_font(font, 'B', 11)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(30, 10, 'Date',        border=1, new_x='RIGHT', new_y='TOP', align='C', fill=True)
    pdf.cell(50, 10, 'Category',    border=1, new_x='RIGHT', new_y='TOP', align='C', fill=True)
    pdf.cell(40, 10, 'Amount (Rs)', border=1, new_x='RIGHT', new_y='TOP', align='C', fill=True)
    pdf.cell(60, 10, 'Description', border=1, new_x='LMARGIN', new_y='NEXT', align='C', fill=True)

    # ── Table body ───────────────────────────────────────────────
    pdf.set_font(font, '', 10)
    if expenses:
        for exp in expenses:
            date_str = exp['date'].strftime('%Y-%m-%d') if hasattr(exp['date'], 'strftime') else str(exp['date'])
            desc     = str(exp['description'] or '')[:30].replace('₹', 'Rs.')
            pdf.cell(30, 10, date_str,                       border=1, new_x='RIGHT', new_y='TOP')
            pdf.cell(50, 10, exp['category'],                border=1, new_x='RIGHT', new_y='TOP')
            pdf.cell(40, 10, f"{float(exp['amount']):,.2f}", border=1, new_x='RIGHT', new_y='TOP', align='R')
            pdf.cell(60, 10, desc,                           border=1, new_x='LMARGIN', new_y='NEXT')
    else:
        pdf.cell(0, 10, 'No transactions found for this period.',
                 border=1, new_x='LMARGIN', new_y='NEXT', align='C')

    return bytes(pdf.output())