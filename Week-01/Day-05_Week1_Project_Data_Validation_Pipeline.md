# Day 05 - Week 1 Project: Mini Data Validation Pipeline

**Date**: 2026-09-30
**Week**: Week 1 - FINAL DAY (Project Day)
**Score**: 72 / 100
**Running Week Average**: ~82%
**Type**: End-to-end applied project — no new theory, pure Week 1 skills

---

## 1. What This Project Proved

```
Week 1 Skills Used in This Project:

Python     -> def, parameters, return, scope, for loops,
              list comprehensions, frequency counter,
              mutable vs immutable (the mutation bug!)

SQL        -> IN, NOT IN, BETWEEN, LIKE, IS NULL

DSA        -> Contains Duplicate pattern (seen set + local list)

Linux      -> head (inspect first rows), wc -l (count records)
```

The project also revealed the Week 1 recurring theme:
**In-place mutation of mutable objects** appeared on Day 2 and again on Day 5.
This is the most important thing to fix going into Week 2.

---

## 2. The Project Brief (For Reference)

INPUT  : 15 raw order records (list of dicts) — dirty data
OUTPUT : A formatted pipeline run report showing:
  - How many records were cleaned
  - Which order_ids are duplicates
  - Status frequency after cleaning
  - How many records are valid vs invalid
  - The actual list of valid orders ready to load

---

## 3. The Raw Dataset

```python
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
```

Dirty data present:
- Negative amounts:   3002 (-75.00), 3007 (-200.00)
- Zero amounts:       3004, 3010
- Wrong casing:       "completed", "valid", "  VALID  ", "  completed "
- Whitespace in:      "  VALID  ", " gbp ", " INR "
- Duplicate order_id: 3001 (appears twice), 3003 (appears twice)
- Invalid statuses:   FAILED, PENDING

---

## 4. The Correct Solution

```python
def clean_record(record):
    """Cleans a single order record and returns a new cleaned copy."""
    return {
        "order_id":    record["order_id"],
        "customer_id": record["customer_id"],
        "amount":      max(record["amount"], 0.0),
        "status":      record["status"].strip().upper(),
        "currency":    record["currency"].strip().upper(),
    }


def is_valid(record):
    """Returns True if record has positive amount and VALID or COMPLETED status."""
    return record["amount"] > 0 and record["status"] in ("VALID", "COMPLETED")


def get_duplicate_ids(orders):
    """Returns a sorted list of order_ids that appear more than once."""
    seen = set()
    duplicates = []
    for order in orders:
        if order["order_id"] in seen:
            duplicates.append(order["order_id"])
        seen.add(order["order_id"])
    return sorted(duplicates)        # sort ONCE, after the loop ends


def count_statuses(orders):
    """Counts how many times each status appears in the dataset."""
    status_freq = {}
    for order in orders:
        status_freq[order["status"]] = status_freq.get(order["status"], 0) + 1
    return status_freq


def run_pipeline(orders):
    """Orchestrates: clean -> deduplicate -> validate -> report."""
    # Count negatives BEFORE cleaning (so we still see the original values)
    negative_count = sum(1 for r in orders if r["amount"] < 0)

    # Clean - creates NEW records, does NOT mutate the originals
    cleaned = [clean_record(r) for r in orders]

    # Detect duplicate order IDs
    duplicate_ids = get_duplicate_ids(cleaned)

    # Count statuses
    status_freq = count_statuses(cleaned)

    # Separate valid / invalid / duplicate
    # ALL three groups must add up to total (15)
    valid_orders   = [r for r in cleaned if is_valid(r) and r["order_id"] not in duplicate_ids]
    invalid_orders = [r for r in cleaned if not is_valid(r) and r["order_id"] not in duplicate_ids]
    duplicate_recs = [r for r in cleaned if r["order_id"] in duplicate_ids]

    print("=" * 60)
    print("       WEEK 1 PROJECT - DATA VALIDATION PIPELINE")
    print("=" * 60)
    print(f"  Total records received : {len(orders)}")
    print()
    print("--- CLEANING REPORT ---")
    print(f"  Negative amounts floored : {negative_count}")
    print(f"  Fields normalized        : {len(cleaned)}")
    print()
    print("--- DUPLICATE ORDER IDs ---")
    print(f"  Duplicates found : {len(duplicate_ids)}")
    print(f"  Affected IDs     : {duplicate_ids}")
    print()
    print("--- STATUS FREQUENCY (after cleaning) ---")
    for status, count in sorted(status_freq.items()):
        print(f"  {status:<12} : {count}")
    print()
    print("--- VALIDATION RESULT ---")
    print(f"  Valid   (ready to load)  : {len(valid_orders)}")
    print(f"  Invalid (quarantined)    : {len(invalid_orders)}")
    print(f"  Skipped (duplicates)     : {len(duplicate_recs)}")
    print()
    print("--- VALID ORDERS ---")
    for order in valid_orders:
        print(f"  Order {order['order_id']} | Rs. {order['amount']:<8} | "
              f"Status: {order['status']:<12} | Currency: {order['currency']}")
    print()
    print("=" * 60)
    print("  Pipeline run complete. 2026-09-30")
    print("=" * 60)

    return valid_orders, invalid_orders


valid, invalid = run_pipeline(raw_orders)
```

Expected output:
```
============================================================
       WEEK 1 PROJECT - DATA VALIDATION PIPELINE
============================================================
  Total records received : 15

--- CLEANING REPORT ---
  Negative amounts floored : 2
  Fields normalized        : 15

--- DUPLICATE ORDER IDs ---
  Duplicates found : 2
  Affected IDs     : [3001, 3003]

--- STATUS FREQUENCY (after cleaning) ---
  COMPLETED    : 3
  FAILED       : 2
  PENDING      : 1
  VALID        : 9

--- VALIDATION RESULT ---
  Valid   (ready to load)  : 5
  Invalid (quarantined)    : 6
  Skipped (duplicates)     : 4

--- VALID ORDERS ---
  Order 3006 | Rs. 340.0    | Status: VALID        | Currency: EUR
  Order 3008 | Rs. 1200.0   | Status: COMPLETED    | Currency: INR
  Order 3009 | Rs. 75.5     | Status: VALID        | Currency: USD
  Order 3011 | Rs. 450.0    | Status: VALID        | Currency: INR
  Order 3013 | Rs. 670.0    | Status: COMPLETED    | Currency: INR

============================================================
  Pipeline run complete. 2026-09-30
============================================================
```

Note: 5 + 6 + 4 = 15. Every record is accounted for. These numbers MUST add up.

---

## 5. Code Review — What You Submitted vs What's Correct

### CRITICAL BUG: In-Place Mutation (appeared on Day 2 AND Day 5)

```python
# YOUR VERSION — mutates original data permanently
def clean_record(records):
    for record in records:
        record["amount"] = max(record["amount"], 0.0)   # DESTROYS original!
        record["status"] = record["status"].strip().upper()

# CORRECT — creates a new dict, leaves original untouched
def clean_record(record):                               # singular, not plural
    return {
        "order_id":    record["order_id"],
        "amount":      max(record["amount"], 0.0),      # new dict
        "status":      record["status"].strip().upper(),
        "currency":    record["currency"].strip().upper(),
        "customer_id": record["customer_id"],
    }
```

WHY THIS MATTERS:
After your clean_record runs, raw_orders[0]["status"] is now "COMPLETED".
The original value "completed" is gone forever.
You can never audit what the raw data looked like.
You can never re-run cleaning with different rules.
You can never debug why a record was changed.

THE RULE: Functions must not modify mutable objects passed to them.
Return a new object. Leave the original untouched.

---

### CRITICAL BUG: Report Numbers Must Match

```
YOUR REPORT:
  Valid (ready to load)  : 12   <- counts VALID + COMPLETED statuses
  Valid orders printed   :  5   <- actually passes is_valid() check

These are different numbers. 12 != 5.
A report that claims 12 are valid but only loads 5 is a data integrity failure.
```

Root cause: You used status_freq['COMPLETED'] + status_freq['VALID'] for the count,
but is_valid() also checks amount > 0. Records 3002 and 3007 have VALID status
after cleaning but amount = 0.0 (floored from negatives). They fail is_valid().

The count you print and the records you print must use the SAME filter.

---

### MAJOR: No Docstrings

Spec said: "Every function must have a docstring."
Zero functions had one. Every function needs at least one line:

```python
def clean_record(record):
    """Cleans a single order record and returns a new cleaned copy."""
```

---

### MAJOR: sort() Inside Loop

```python
# YOUR VERSION — sorts the list on every single loop iteration
for order in orders:
    if order["order_id"] in seen:
        duplicates.append(order["order_id"])
    seen.add(order["order_id"])
    duplicates.sort()    # runs 15 times unnecessarily

# CORRECT — sort once, after the loop
    return sorted(duplicates)
```

---

### MAJOR: Global Variable Used Inside Function

```python
# YOUR VERSION — uses global name inside a function
def run_pipeline(orders):
    print(f"Total records received : {len(raw_orders)}")  # raw_orders is global!

# CORRECT — use the parameter
    print(f"Total records received : {len(orders)}")
```

---

### MINOR: Unicode Crash on Windows PowerShell

The Rs. (rupee symbol) crashed in PowerShell due to cp1252 encoding.
Always use "Rs." instead of the Unicode symbol when writing to terminal on Windows.

---

## 6. SQL Answers

```sql
-- Q1: Orders where currency is INR or USD
SELECT order_id, amount
FROM orders
WHERE currency IN ('INR', 'USD');

-- Q2: Orders where amount is between 100 and 600
SELECT order_id, amount
FROM orders
WHERE amount BETWEEN 100 AND 600;

-- Q3: Orders where status is not VALID or COMPLETED
SELECT *
FROM orders
WHERE status NOT IN ('VALID', 'COMPLETED');
```

SQL rules passed this session:
  RULE 1 (single quotes)   -> All 3 queries: CORRECT
  RULE 4 (uppercase keywords) -> Q1 and Q2: CORRECT, Q3 was lowercase SELECT

---

## 7. Linux Answers

```bash
# Command 1: Inspect the first few rows to understand the data structure
head raw_orders.csv

# Command 2: Count total number of records (rows)
wc -l raw_orders.csv
```

Both correct. The reasoning was clear.

UPGRADE for production:
  head -n 5 raw_orders.csv     <- see exactly 5 rows
  wc -l raw_orders.csv         <- count rows (includes header, so actual data = result - 1)
  cat raw_orders.csv | head    <- pipe version

---

## 8. Week 1 Complete — All Skills Summary

```
PYTHON (Days 1-5):
  Data types  : int, float, str, bool, None, list, dict, set, tuple
  Loops       : for, range(), enumerate(), break, continue
  Functions   : def, parameters, return, default params, scope
  Concepts    : mutable vs immutable, side effects, frequency counter
  Pattern     : clean() -> validate() -> load() pipeline architecture

LINUX (Days 1-4):
  File inspection : head, tail, cat, wc -l, grep
  Redirects       : > (overwrite), >> (append)
  Pipe            : | (chain commands)
  Standard streams: stdin, stdout, stderr

SQL (Days 3-5):
  Basics       : SELECT, FROM, WHERE, AND, OR
  Filtering    : IN, NOT IN, BETWEEN, LIKE (%), IS NULL, IS NOT NULL
  Rules        : single quotes, full OR conditions, AND/OR precedence,
                 uppercase keywords

DSA (Days 2-5):
  Frequency counter: dict + .get() -> Counter()
  Contains Duplicate: brute O(N^2) vs set O(N) -> one-liner
  Mental model: use the right data structure for the operation

JS (Days 2-5):
  Data types   : all 9 types
  Scope        : var vs let/const, block scope, scope chain
  Closures     : outer scope captured by inner function,
                 even after outer function returns
  Bug trap     : var-in-loop prints same value for all callbacks
```

---

## 9. FAANG Interview Questions — Week 1 Level

Q: What is the difference between mutable and immutable in Python?
A: Immutable objects (int, str, float, bool, tuple) cannot be changed after creation.
   Any operation that "changes" them creates a NEW object in memory.
   Mutable objects (list, dict, set) can be changed in place.
   This means functions that receive mutable objects can accidentally modify the
   caller's data if they are not careful to create new objects instead of
   modifying the ones they received.

Q: Why should functions avoid modifying the objects they receive as parameters?
A: Because the caller passed the object and may still be using it.
   Modifying it inside the function is a hidden side effect that can cause bugs
   that are extremely hard to trace. Best practice: create a new object, modify that,
   and return it. Leave the original untouched.

Q: You have 10 million records. You need to check if any order_id is duplicated.
   What approach do you use and why?
A: Use a set for O(1) lookups. Iterate once through the records, adding each order_id
   to the set. If an ID is already in the set, it is a duplicate. Total time: O(N).
   The brute force comparison of every pair is O(N^2) and is completely unworkable
   at 10 million records.

Q: In SQL, you want to find all customers where the phone number is not recorded.
   A colleague wrote "WHERE phone = NULL". Will this work?
A: No. NULL represents the absence of a value. Equality comparison against NULL
   is undefined - it returns NULL, not TRUE. The query will silently return 0 rows.
   The correct syntax is: WHERE phone IS NULL

---

## 10. Debugging Challenges for Week 2 Day 1

Bug 1: What is wrong and what does this print?
```python
def add_tax(orders, rate=0.18):
    for order in orders:
        order["amount"] = order["amount"] * (1 + rate)
    return orders

batch = [{"id": 1, "amount": 100.0}, {"id": 2, "amount": 200.0}]
taxed = add_tax(batch)
print(taxed[0]["amount"])    # Line A
print(batch[0]["amount"])    # Line B - what does this print and why?
```

Bug 2: What does this SQL return?
```sql
SELECT name, city
FROM customers
WHERE city LIKE 'B%' AND is_active = TRUE
   OR age > 30;
```

Bug 3: What is wrong with this JS and how do you fix it?
```javascript
function makeLogger(prefix) {
    return function(message) {
        console.log(prefix + ": " + message);
    };
}

const log = makeLogger;    // Bug is here
log("error")("Something went wrong");
```

---

## 11. Spaced Repetition Checklist

Review on Day 6, Day 12, and Day 35. Cover answers. Say out loud.

- [ ] What does in-place mutation mean? Give a one-line example of it happening.
- [ ] What is the difference between clean_record(record) returning a new dict
      vs modifying record["key"] = value inside the function?
- [ ] If a report shows "Valid: 12" but only 5 records load, what went wrong?
- [ ] SQL: Write a query using IN and BETWEEN together in the same WHERE clause.
- [ ] SQL: Write a query using NOT IN.
- [ ] DSA: Contains Duplicate one-liner from memory.
- [ ] JS: What does a closure capture when there is no let/const inside the inner function?
- [ ] Linux: What is the difference between head and wc -l?

---

## 12. Week 2 Preview

```
What is coming next:

Day 6  (Week 2, Day 1)
  -> MySQL setup: connect Python to MySQL
     - How to start MySQL on Windows
     - mysql-connector-python
     - First SELECT from Python
  -> Python: CSV file reading with csv.DictReader
  -> SQL: JOINs (INNER, LEFT) — the most important SQL concept

Day 7  (Week 2, Day 2)
  -> Python: Writing to files, CSV writing
  -> SQL: GROUP BY, aggregate functions (COUNT, SUM, AVG, MAX, MIN)
  -> DSA: Two Sum (LC 1)

Day 8  (Week 2, Day 3)
  -> FULL ETL: CSV file -> Python cleaning -> MySQL INSERT
     This is the real pipeline. raw_orders.csv -> orders table in MySQL.

Day 9  (Week 2, Day 4)
  -> SQL: Subqueries, HAVING clause
  -> Python: Exception handling (try/except) for pipeline errors

Day 10 (Week 2, Day 5)
  -> Week 2 Project: Full ETL pipeline with real MySQL
```

---

Day 05 complete - 2026-09-30
Score: 72 / 100
Week 1 Average: ~82%
Next: Week 2 Day 1 - MySQL connection + CSV reading + SQL JOINs