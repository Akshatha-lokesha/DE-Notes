raw_orders = [
    {"order_id": 3001, "amount": 499.95,  "status": "completed",    "currency": "inr",   "customer_id": 101},
    {"order_id": 3002, "amount": -75.00,  "status": "VALID",        "currency": "USD",   "customer_id": 102},
    {"order_id": 3003, "amount": 820.00,  "status": "  VALID  ",    "currency": " gbp ", "customer_id": 103},
    {"order_id": 3004, "amount": 0.00,    "status": "valid",        "currency": "INR",   "customer_id": 104},
    {"order_id": 3005, "amount": 150.00,  "status": "FAILED",       "currency": "usd",   "customer_id": 105},
    {"order_id": 3001, "amount": 999.00,  "status": "VALID",        "currency": "INR",   "customer_id": 106},
    {"order_id": 3006, "amount": 340.00,  "status": "VALID",        "currency": "eur",   "customer_id": 107},
    {"order_id": 3007, "amount": -200.00, "status": "VALID",        "currency": "INR",   "customer_id": 108},
    {"order_id": 3008, "amount": 1200.00, "status": "COMPLETED",    "currency": "inr",   "customer_id": 109},
    {"order_id": 3009, "amount": 75.50,   "status": "VALID",        "currency": "USD",   "customer_id": 110},
    {"order_id": 3010, "amount": 0.00,    "status": "PENDING",      "currency": "INR",   "customer_id": 111},
    {"order_id": 3011, "amount": 450.00,  "status": "valid",        "currency": " INR ", "customer_id": 112},
    {"order_id": 3003, "amount": 820.00,  "status": "VALID",        "currency": "GBP",   "customer_id": 113},
    {"order_id": 3012, "amount": 95.00,   "status": "FAILED",       "currency": "usd",   "customer_id": 114},
    {"order_id": 3013, "amount": 670.00,  "status": "  completed ", "currency": "INR",   "customer_id": 115},
]

# Task 1 — clean_record(record) → returns a cleaned dict
# Floor negative amount to 0.0
# status: strip whitespace + uppercase
# currency: strip whitespace + uppercase
# Keep order_id and customer_id unchanged

# Task 2 — is_valid(record) → returns True or False
# A record is valid only if both:
# amount > 0
# status is either "VALID" or "COMPLETED"

# Task 3 — get_duplicate_ids(orders) → returns a sorted list of duplicate order IDs
# Use a seen set and a local duplicates list — no global variables
# No shadowing of built-ins

# Task 4 — count_statuses(orders) → returns a dict
# Use the frequency counter .get() pattern
# Count how many times each status appears in the cleaned dataset
# Example: {"COMPLETED": 3, "VALID": 7, "FAILED": 2, ...}

# Task 5 — run_pipeline(orders) — the orchestrator function
# Calls all the above functions and prints this exact report format:

# ============================================================
#        WEEK 1 PROJECT - DATA VALIDATION PIPELINE
# ============================================================
#   Total records received : 15
# --- CLEANING REPORT ---
#   Negative amounts floored : 2
#   Fields normalized        : 15
# --- DUPLICATE ORDER IDs ---
#   Duplicates found : 2
#   Affected IDs     : [3001, 3003]
# --- STATUS FREQUENCY (after cleaning) ---
#   COMPLETED    : 3
#   VALID        : 7
#   FAILED       : 2
#   PENDING      : 1
#   ... (whatever your data produces)
# --- VALIDATION RESULT ---
#   Valid (ready to load)  : X
#   Invalid (quarantined)  : X
# --- VALID ORDERS ---
#   Order 3001 | ₹ 499.95 | Status: COMPLETED | Currency: INR
#   Order 3003 | ₹ 820.00 | Status: VALID     | Currency: GBP
#   ... (all valid orders)
# ============================================================
#   Pipeline run complete. 2026-09-30
# ============================================================

def clean_record(records):
    for record in records:
        record["amount"] = max(record["amount"], 0.0)
        record["status"] = record["status"].strip().upper()
        record["currency"] = record["currency"].strip().upper()
    return records

def is_valid(record):
    return record["amount"] > 0 and (record["status"] == "VALID" or  record["status"] == "COMPLETED")

def get_duplicate_ids(orders):
    seen = set()
    duplicates = []
    for order in orders:
        if order["order_id"] in seen:
            duplicates.append(order["order_id"])
        seen.add(order["order_id"])
        duplicates.sort()
    return duplicates

def count_statuses(orders):
    status_freq = {}
    for order in orders:
        status_freq[order["status"]] = status_freq.get(order["status"], 0)+1
    return status_freq

def run_pipeline(orders):
    print("="*50)
    print(f"     WEEK 1 PROJECT - DATA VALIDATION PIPELINE")
    print("="*50)
    print(f"Total records received : {len(raw_orders)}")
    print("--- CLEANING REPORT ---")
    # print(orders)
    negative_amt = [r for r in orders if r["amount"] < 0]
    print(f"Negative amounts floored : {len(negative_amt)}")
    cleaned_records = clean_record(orders)
    print(f"Fields normalized : {len(cleaned_records)}")
    print("--- DUPLICATE ORDER IDs ---")
    duplicate_orders = get_duplicate_ids(cleaned_records)
    print(f"Duplicates found : {len(duplicate_orders)}")
    print(f"Affected IDs     : {duplicate_orders}")
    print("--- STATUS FREQUENCY (after cleaning) ---")
    status_freq = count_statuses(cleaned_records)
    print(f"COMPLETED  : {status_freq['COMPLETED']}")
    print(f"VALID      : {status_freq['VALID']}")
    print(f"FAILED     : {status_freq['FAILED']}")
    print(f"PENDING    : {status_freq['PENDING']}")
    print("--- VALIDATION RESULT ---")
    valid = [i for i in cleaned_records if i["status"] == "COMPLETED" or i["status"] == "VALID"]
    # print(f"Valid (ready to load)  : {len(valid)}")
    # print(f"Invalid (quarantined)  : {len(cleaned_records) - len(valid)}")
    print(f"Valid (ready to load)  : {status_freq['COMPLETED'] + status_freq['VALID']}")
    print(f"Invalid (quarantined)  : {status_freq['FAILED'] + status_freq['PENDING']}")
    print("--- VALID ORDERS ---")
    for order in cleaned_records:
        if is_valid(order) and order["order_id"] not in duplicate_orders:
            print(f"Order {order['order_id']} | ₹ {order['amount']:<8} | Status: {order['status']:<12} | Currency: {order['currency']}")

run_pipeline(raw_orders)

# My Output
# ==================================================
#      WEEK 1 PROJECT - DATA VALIDATION PIPELINE
# ==================================================
# Total records received : 15
# --- CLEANING REPORT ---
# Negative amounts floored : 2
# Fields normalized : 15
# --- DUPLICATE ORDER IDs ---
# Duplicates found : 2
# Affected IDs     : [3001, 3003]
# --- STATUS FREQUENCY (after cleaning) ---
# COMPLETED  : 3
# VALID      : 9
# FAILED     : 2
# PENDING    : 1
# --- VALIDATION RESULT ---
# Valid (ready to load)  : 12
# Invalid (quarantined)  : 3
# --- VALID ORDERS ---
# Order 3006 | ₹ 340.0    | Status: VALID        | Currency: EUR
# Order 3008 | ₹ 1200.0   | Status: COMPLETED    | Currency: INR
# Order 3009 | ₹ 75.5     | Status: VALID        | Currency: USD
# Order 3011 | ₹ 450.0    | Status: VALID        | Currency: INR
# Order 3013 | ₹ 670.0    | Status: COMPLETED    | Currency: INR

# ============================================================
# SQL QUESTIONS — Answer as comments below each question
# ============================================================

# Q1: From the orders table, get order_id and amount for all orders
#     where currency is either 'INR' or 'USD' — use IN, not OR
#     Answer: SELECT order_id, amount FROM raw_orders WHERE currency IN ('INR','USD') 

# Q2: Get order_id and amount for all orders where amount is
#     between 100 and 600 (inclusive)
#     Answer: SELECT order_id, amount FROM raw_orders WHERE amount BETWEEN 100 AND 600

# Q3: Get all orders where status is NOT 'VALID' and NOT 'COMPLETED'
#     (hint: use NOT IN)
#     Answer:SELECT * FROM raw_orders WHERE status NOT IN ('VALID', 'COMPLETED')

# ============================================================
# LINUX QUESTION
# ============================================================

# Before running this pipeline, the orders data arrives as a
# file called raw_orders.csv on a Linux server.
# Write the TWO Linux commands you would run first and explain
# why you run each one.
#
# Command 1:
# Why: head raw_orders.csv -- because to check what kind of data i've recived
#
# Command 2:
# Why: wc -l raw_orders.csv -- to check what's the number of records i've recived