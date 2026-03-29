from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_sample_statement():
    filename = "sample_bank_statement.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "GLOBAL BANK - ACCOUNT STATEMENT")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, "Account Number: 1234567890")
    c.drawString(50, height - 85, "Period: February 2026")
    
    # Column Headers
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, height - 120, "Date")
    c.drawString(150, height - 120, "Description")
    c.drawString(450, height - 120, "Amount (₹)")
    
    c.line(50, height - 125, 550, height - 125)
    
    # Sample Data
    expenses = [
        ("2026-02-01", "Whole Foods Market", "-85.50"),
        ("2026-02-03", "Netflix Subscription", "-15.99"),
        ("2026-02-05", "Shell Gas Station", "-45.00"),
        ("2026-02-10", "Starbucks Coffee", "-6.50"),
        ("2026-02-12", "Utility Bill - City Power", "-120.00"),
        ("2026-02-14", "Amazon.com Order", "-32.40"),
        ("2026-02-15", "Rent Payment", "-1500.00"),
    ]
    
    y = height - 145
    c.setFont("Helvetica", 11)
    
    for date, desc, amount in expenses:
        c.drawString(50, y, date)
        c.drawString(150, y, desc)
        c.drawRightString(510, y, amount)
        y -= 20
        
    c.save()
    print(f"Sample PDF created: {os.path.abspath(filename)}")

if __name__ == "__main__":
    create_sample_statement()
