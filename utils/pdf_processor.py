import pdfplumber
import re
import pandas as pd
from datetime import datetime


# ── CATEGORIZATION ───────────────────────────────────────────────────────────

def categorize_description(description):
    description = description.lower()
    mapping = {
        'Food':          ['market', 'grocery', 'restaurant', 'food', 'swiggy', 'zomato',
                          'blinkit', 'bigbasket', 'dunzo', 'cafe', 'kitchen', 'bakery',
                          'hotel', 'dhaba', 'mess', 'canteen'],
        'Utilities':     ['power', 'electricity', 'water', 'bill', 'recharge', 'airtel',
                          'jio', 'vodafone', 'bsnl', 'broadband', 'internet',
                          'dth', 'tatasky', 'gas', 'cylinder', 'lpg'],
        'Rent':          ['rent', 'lease', 'house', 'flat', 'pg', 'hostel', 'lodging'],
        'Entertainment': ['netflix', 'amazonprime', 'hotstar', 'disney', 'spotify',
                          'youtube', 'movie', 'cinema', 'pvr', 'inox', 'bookmyshow'],
        'Transport':     ['petrol', 'fuel', 'uber', 'ola', 'rapido', 'metro', 'train',
                          'irctc', 'bus', 'toll', 'parking', 'fastag', 'redbus'],
    }
    for category, keywords in mapping.items():
        if any(kw in description for kw in keywords):
            return category
    return 'Other'


# ── DATE NORMALISATION ────────────────────────────────────────────────────────

def normalise_date(date_str):
    date_str = date_str.replace(',', ' ')          # remove commas first
    date_str = re.sub(r'(\d{1,2})([A-Za-z])', r'\1 \2', date_str)
    date_str = re.sub(r'([A-Za-z])(\d)', r'\1 \2', date_str)
    date_str = re.sub(r'\s+', ' ', date_str.strip())
    formats = ["%d %b %Y", "%b %d %Y", "%B %d %Y", "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str


# ── AMOUNT CLEANING ───────────────────────────────────────────────────────────

def clean_amount(raw):
    cleaned = re.sub(r'[₹,\s]', '', str(raw))
    try:
        return float(cleaned)
    except ValueError:
        return None


# ── GPAY PARSER ───────────────────────────────────────────────────────────────

def parse_gpay(pdf_file):
    """
    GPay merges column text together with no spaces:
    '15Feb,2026 Paidtosanjeevanhostel ₹5,000'

    Strategy: read line by line, match lines that contain
    'Paidto' (no space) but NOT 'PaidtoBankofBaroda' (those are credits).
    """
    records = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.split('\n'):
                line = line.strip()

                # Must contain 'Paidto' (merged) but not a bank credit line
                if 'Paidto' not in line:
                    continue
                if 'BankofBaroda' in line or 'Baroda' in line:
                    continue
                # Also skip "Paid to Bank" variants
                if re.search(r'Paidto\w*[Bb]ank', line):
                    continue

                # ── Date ─────────────────────────────────────────────
                # Format: "15Feb,2026" — digits then letters merged
                date_match = re.search(
                    r"(\d{1,2}(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec),?\s*\d{4})",
                    line, re.IGNORECASE
                )
                if not date_match:
                    continue
                date_str = normalise_date(date_match.group(1))

                # ── Amount ───────────────────────────────────────────
                amt_match = re.search(r'₹([\d,]+\.?\d*)', line)
                if not amt_match:
                    continue
                amount = clean_amount(amt_match.group(1))
                if not amount or amount <= 0:
                    continue

                # ── Merchant ─────────────────────────────────────────
                # Extract text between "Paidto" and "₹"
                merchant_match = re.search(
                    r'Paidto(.+?)(?:₹|UPI|$)', line, re.IGNORECASE
                )
                if not merchant_match:
                    continue
                merchant = merchant_match.group(1).strip()
                if not merchant:
                    continue

                records.append({
                    "date":            date_str,
                    "description":     merchant,
                    "amount":          amount,
                    "category":        categorize_description(merchant),
                    "raw_text_source": line[:120]
                })

    return records


# ── PHONEPE PARSER ────────────────────────────────────────────────────────────

def parse_phonepe(text):
    """
    PhonePe text has spaces: 'Paid to RONAK ENTERPRISES DEBIT ₹75'
    Split into blocks by date and parse each block.
    """
    records = []
    date_pattern = re.compile(
        r"(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec),?\s+\d{4}"
        r"|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4})",
        re.IGNORECASE
    )
    splits = list(date_pattern.finditer(text))

    for i, match in enumerate(splits):
        start = match.start()
        end   = splits[i + 1].start() if i + 1 < len(splits) else len(text)
        block = text[start:end].strip()
        block_lower = block.lower()

        if any(w in block_lower for w in ["received from", "type credit", "credited", "refund"]):
            continue

        amount_match = (
            re.search(r"Amount\s*₹\s*([\d,]+\.?\d*)", block, re.IGNORECASE) or
            re.search(r"DEBIT\s*₹\s*([\d,]+\.?\d*)", block, re.IGNORECASE) or
            re.search(r"₹\s*([\d,]+\.?\d*)", block)
        )
        if not amount_match:
            continue
        amount = clean_amount(amount_match.group(1))
        if not amount or amount <= 0:
            continue

        paid_to = re.search(
            r"(?:Paid to|To)\s+(.+?)(?:\s+UPI|\s+DEBIT|\s+CREDIT|\s+Transaction|\s+Amount|\s+Paidby|\s*\n|$)",
            block, re.IGNORECASE
        )
        merchant = paid_to.group(1).strip() if paid_to else None
        if not merchant:
            fallback = re.search(r"\d{2}:\d{2}\s+(?:am|pm)\s+(.+?)(?:\s+UPI|\s+DEBIT|\s+₹)", block, re.IGNORECASE)
            merchant = fallback.group(1).strip() if fallback else block[:50].replace("\n", " ").strip()

        merchant = re.sub(r'\s+(UPI|DEBIT|Transaction).*$', '', merchant, flags=re.IGNORECASE).strip()

        records.append({
            "date":            normalise_date(match.group(1)),
            "description":     merchant,
            "amount":          amount,
            "category":        categorize_description(merchant),
            "raw_text_source": block[:120]
        })

    return records


# ── GENERIC BANK PARSER ───────────────────────────────────────────────────────

def parse_generic(text):
    records = []
    date_pat = (r"(\d{1,2}[-\s](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-\s]\d{2,4}"
                r"|\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4})")
    pattern = re.compile(date_pat + r"\s+(.+?)\s+([\d,]+\.\d{2})", re.IGNORECASE)
    for m in pattern.finditer(text):
        desc = m.group(2).strip()
        amt  = clean_amount(m.group(3))
        if amt and amt > 0 and len(desc) > 2:
            records.append({
                "date":            normalise_date(m.group(1)),
                "description":     desc,
                "amount":          amt,
                "category":        categorize_description(desc),
                "raw_text_source": m.group(0)
            })
    return records


# ── DETECT SOURCE ─────────────────────────────────────────────────────────────

def detect_source(text):
    t = text.lower()
    if "google pay" in t or "gpay" in t or "google llc" in t:
        return "gpay"
    if "phonepe" in t or "phone pe" in t:
        return "phonepe"
    return "generic"


# ── MAIN ENTRY POINT ──────────────────────────────────────────────────────────

def parse_bank_statement(pdf_file):
    all_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n"

    if not all_text.strip():
        return pd.DataFrame()

    source = detect_source(all_text)

    if source == "gpay":
        records = parse_gpay(pdf_file)
    elif source == "phonepe":
        records = parse_phonepe(all_text)
    else:
        records = parse_generic(all_text)

    # Fallback: try other parsers if nothing found
    if not records:
        for fn, arg in [(parse_gpay, pdf_file), (parse_phonepe, all_text), (parse_generic, all_text)]:
            try:
                records = fn(arg)
                if records:
                    break
            except Exception:
                continue

    # Deduplicate
    seen, unique = set(), []
    for r in records:
        key = (r["date"], r["description"][:30], r["amount"])
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return pd.DataFrame(unique) if unique else pd.DataFrame()