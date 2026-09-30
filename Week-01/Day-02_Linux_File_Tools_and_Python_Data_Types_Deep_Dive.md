# Day 02 - Linux File Tools & Python Data Types: The Complete DE Reference

**Date**: 2026-09-25
**Week**: Week 1 - Absolute Foundations
**Mentor Score**: 82% (33/40) - Solid fundamentals. One critical bug caught. Strong independent code.
**Topics**: Linux File Inspection Toolkit | All Python Data Types (9 types) | In-Place Modifier Rule
**Deferred to Day 3**: SQL table foundations | DSA frequency counter | JS block scope

---

## 1. Executive Summary - What We Built Today & Why It Matters

```
WHERE TODAY'S SKILLS FIT IN YOUR FUTURE DE PIPELINE

     [Partner sends 30 GB orders.csv]
              |
              v
      +-----------------+
      |  Linux Server   |  <-- You SSH in here
      |                 |
      | head orders.csv |  "What columns does this file have?"
      | wc -l orders.csv|  "How many rows did they send?"
      | grep "ERROR"    |  "Did anything fail during transfer?"
      | tail -f run.log |  "Watch the ingestion job live"
      +-----------------+
              |
              v
      +-----------------+
      |  Python Script  |  <-- You write this
      |                 |
      | str  -> clean fields (strip, lower, split)
      | dict -> represent each row as a record
      | list -> hold all records in memory
      | set  -> deduplicate customer IDs
      | int  -> count rows, calculate batch sizes
      | bool -> flag valid vs invalid records
      | None -> represent missing/null values
      | tuple-> hold config (host, port, db_name)
      +-----------------+
              |
              v
      [Clean data loaded into PostgreSQL / S3]
```

---

## 2. MODULE 1 - Linux File Inspection Toolkit

### The Core Problem

Opening a 30 GB file in Windows Notepad = RAM explosion + freeze.
Linux tools read only the bytes needed to answer your question. Never more.

---

### 2.1 head (Peek at the Top)

**Analogy**: You receive a mystery package. Before unpacking all 2,000 items,
you look at the label on the top layer. That is `head`.

**What it does**: Prints the first N lines of a file. Default = 10.

**Real DE Scenario**: A data partner sends customers.csv (15 GB).
You need the column names before writing your ETL script.

```bash
head customers.csv
```
Output:
```
customer_id,name,email,city,signup_date
1001,Rahul Sharma,rahul@gmail.com,Bangalore,2023-01-15
1002,Priya Patel,priya@yahoo.com,Mumbai,2023-01-16
...
```

```bash
head -n 3 customers.csv
```
Output:
```
customer_id,name,email,city,signup_date
1001,Rahul Sharma,rahul@gmail.com,Bangalore,2023-01-15
1002,Priya Patel,priya@yahoo.com,Mumbai,2023-01-16
```

Key flag: -n <number> -- controls how many lines to show.

---

### 2.2 tail (Peek at the Bottom)

**Analogy**: A pipeline writes logs continuously, always appending to the bottom.
The latest events are at the tail. Like reading the last pages of a diary.

**What it does**: Prints the last N lines. Default = 10.

**Real DE Scenario**: Your Airflow pipeline failed at 2 AM.
The newest error is always at the very bottom of the log file.

```bash
tail pipeline.log
```
Output:
```
[01:55:01] INFO: Batch 98 loaded successfully.
[01:56:14] INFO: Batch 99 loaded successfully.
[01:57:30] WARNING: DB response degraded (450ms).
[01:58:10] WARNING: Connection pool exhausted.
[01:59:02] ERROR: Failed after 3 retries.
[01:59:03] CRITICAL: Pipeline aborted at record #482910.
```

```bash
tail -f pipeline.log
```
Keeps your terminal OPEN. Every new log line appears in real time.
Press Ctrl+C to stop. This is the on-call engineer's #1 tool.

Key flags:
- -n <number>  how many lines from the bottom
- -f           follow/stream in real time

---

### 2.3 wc (Word/Line Count)

**Analogy**: Weighing a parcel before opening it. You verify the count before processing.

**Real DE Scenario**: Business team says "We sent 10,000 orders today." You verify.

```bash
wc -l orders.csv
```
Output: 10001 orders.csv

Why 10001 not 10000? Line 1 is the column header. Data rows = 10000. Correct.

Key flags:
- -l  count lines (most common for DE)
- -w  count words
- -c  count bytes

---

### 2.4 grep (Global Regular Expression Print)

**Analogy**: A phone directory with 500,000 entries.
You scan specifically for "Sharma" without reading every name.

**What it does**: Searches for a pattern and prints every matching line.

```bash
grep "ERROR" pipeline.log
```
Output:
```
[01:59:02] ERROR: Failed to acquire DB connection after 3 retries.
[02:15:10] ERROR: Disk space warning on /var/log.
```

```bash
grep -c "ERROR" pipeline.log
```
Output: 2  (just the count, not the lines)

Key flags:
- -i  case-insensitive (matches ERROR, Error, error)
- -n  show line numbers where matches were found
- -c  count how many lines matched

---

### 2.5 Windows/JS to Linux Translation Table

| Windows / Web Dev Concept         | Linux Terminal Command    | What it actually does              |
|:----------------------------------|:--------------------------|:-----------------------------------|
| Open file in Notepad (top 5 lines)| head -n 5 file.txt        | Reads only 5 lines, never loads file |
| Scroll to bottom of file          | tail -n 10 file.txt       | Shows last 10 lines instantly      |
| Watch DevTools console live       | tail -f app.log           | Streams new log lines as written   |
| Line count in VS Code status bar  | wc -l file.txt            | Prints total number of lines       |
| Ctrl+F to search in VS Code       | grep "keyword" file.txt   | Extracts all matching lines        |

---

### 2.6 Level-Up Path for Linux File Tools

```
Level 1 (YOU ARE HERE - Day 2):
  head, tail, wc, grep
  -> Inspect files without crashing your machine.

Level 2 (Day 3):
  Pipes:    cat file.txt | grep "ERROR" | wc -l
  Redirect: grep "ERROR" pipeline.log > errors_only.txt

Level 3 (Week 2):
  find  -> locate files anywhere on the server
  df/du -> check disk space remaining
  ps/top -> see running processes

Level 4 (Production DE):
  ssh   -> connect to remote AWS EC2 server
  scp   -> copy files securely between servers
  cron  -> schedule Python pipelines automatically
```

---

### 2.7 Unifying Picture: The File Inspection Toolkit

```
                YOU (On-Call DE at 2 AM)
                        |
                   "What happened?"
                        |
           +------------+-------------+
           |            |             |
       [ head ]      [ grep ]      [ tail ]
     "What does     "Find all     "Show me
      this file      ERROR lines   the latest
      look like?"    right now"    events"
           |            |             |
           +------------+-------------+
                        |
                     [ wc -l ]
                 "How many rows total?"
```

---

## 3. MODULE 2 - Python Data Types: Complete DE Reference

### 3.1 The Master Map

```
ALL PYTHON DATA TYPES (DE-Relevant)
|
+-- IMMUTABLE (Cannot change after creation - safe to share freely)
|   +-- int        Whole numbers:    1, 100, -55, 0
|   +-- float      Decimal numbers:  3.14, -0.5
|   +-- str        Text:             "ERROR", "SELECT * FROM orders"
|   +-- bool       Truth values:     True, False
|   +-- tuple      Fixed sequence:   ("host", 5432, "dbname")
|   +-- NoneType   Emptiness:        None
|
+-- MUTABLE (Can change - be careful when sharing between functions)
    +-- list       Ordered, changeable:  [1, 2, 3]
    +-- dict       Key -> Value:         {"name": "Akshay"}
    +-- set        Unique, unordered:    {1, 2, 3}
```

Why this distinction matters in DE:
When you pass a MUTABLE object to a function, that function can silently corrupt
your original data. Immutable objects are always safe to share.

---

### 3.2 int (Integer)

Whole number, no decimal. No size limit in Python.

```python
record_count = 5_000_000    # _ is a visual separator
error_code   = -1
print(type(record_count))   # <class 'int'>
```

Critical operators:
```python
total_rows = 10000
batch_size = 256

batches_needed = total_rows // batch_size   # Floor division -> 39
leftover_rows  = total_rows % batch_size    # Modulo/remainder -> 16
print(2 ** 10)                              # Power -> 1024
```

Real DE Pattern - Batch Processing:
```python
def process_in_batches(all_records, batch_size=256):
    total        = len(all_records)
    full_batches = total // batch_size
    remainder    = total % batch_size
    print(f"Total    : {total:,}")
    print(f"Batches  : {full_batches}")
    print(f"Leftover : {remainder}")

process_in_batches(list(range(10016)))
# Total    : 10,016
# Batches  : 39
# Leftover : 16
```

When to use int: row counts, batch sizes, loop counters, record IDs, error counts.

---

### 3.3 float (Floating Point Decimal)

Number with a decimal point. 64-bit precision.

The Float Precision Trap - real financial bugs have been caused by this:
```python
print(0.1 + 0.2)    # 0.30000000000000004  -- NOT 0.3!
```

The Production Fix for Financial Data:
```python
from decimal import Decimal
price = Decimal("0.10")
tax   = Decimal("0.20")
print(price + tax)    # 0.30  -- Exact!
```

Rule: Use float for metrics/analytics. Use Decimal for money.

Type conversion:
```python
int(99.9)     # 99  -- TRUNCATES, does NOT round!
float(5)      # 5.0
```

---

### 3.4 str (String) - The Most Used DE Type

A DE spends 40% of Python work manipulating strings.
Every log line, file path, SQL query, column name, config value is a string.

Creating strings:
```python
pipeline_name = "sales_orders_ingestion"
query = f"SELECT * FROM orders WHERE status = 'ACTIVE'"
```

All Critical String Methods:

.lower() / .upper() - Normalize incoming data
```python
status = "Completed"
print(status.lower())                  # completed
print("completed" == status.lower())   # True
```
DE use: Vendors send "ACTIVE", "active", "Active" - normalize before DB load.

.strip() / .lstrip() / .rstrip() - Remove whitespace
```python
dirty = "   Bangalore   \n"
print(repr(dirty.strip()))    # 'Bangalore'
print(repr(dirty.lstrip()))   # 'Bangalore   \n'
print(repr(dirty.rstrip()))   # '   Bangalore'
```
DE use: CSV fields have trailing spaces. "WHERE city = 'Bangalore'" returns 0 results
if you loaded '  Bangalore  ' instead. Always strip.

.split() - Break string into a list
```python
log_line = "2026-09-22,01:59:02,ERROR,Connection timeout"
fields = log_line.split(",")
print(fields)      # ['2026-09-22', '01:59:02', 'ERROR', 'Connection timeout']
print(fields[2])   # ERROR
```

", ".join(list) - Assemble list into one string
```python
columns  = ["order_id", "customer_id", "amount", "status"]
sql_cols = ", ".join(columns)
print(sql_cols)    # order_id, customer_id, amount, status
```
DE use: Dynamically building SQL SELECT clauses.

.replace(old, new) - Swap substrings
```python
raw_phone = "+91-98765-43210"
clean = raw_phone.replace("-", "").replace("+", "")
print(clean)    # 919876543210
```

.startswith(x) / .endswith(x) - Routing logic
```python
file_path = "/data/raw/orders_2026.csv"
if file_path.endswith(".csv"):
    print("Parsing as CSV")
elif file_path.endswith(".parquet"):
    print("Parsing as Parquet")
```

"x" in string / .find("x") - Search inside strings
```python
log = "[01:59:02] ERROR: Connection timeout"
print("ERROR" in log)        # True
print(log.find("ERROR"))     # 12
print(log.find("CRITICAL"))  # -1  (.find returns -1 when not found)
```

f-strings - The modern way to embed variables
```python
pipeline = "customer_orders"
rows     = 1_250_000
duration = 47
msg = f"Pipeline '{pipeline}' loaded {rows:,} rows in {duration}s"
print(msg)
# Pipeline 'customer_orders' loaded 1,250,000 rows in 47s
```
Note: :, adds comma separators to large numbers automatically.

String Methods Reference Card:
| Method               | What it does                   | DE Use Case                      |
|:---------------------|:-------------------------------|:---------------------------------|
| .lower() / .upper()  | Change case                    | Normalizing incoming data        |
| .strip()             | Remove surrounding whitespace  | Cleaning CSV fields              |
| .split(",")          | Break into list on delimiter   | Parsing CSV/log lines            |
| ", ".join(list)      | Assemble list into string      | Building SQL SELECT clauses      |
| .replace(old, new)   | Swap substring                 | Cleaning phone numbers, IDs      |
| .startswith(x)       | Check prefix                   | File type routing                |
| .endswith(x)         | Check suffix                   | File type routing                |
| "x" in string        | Check if substring exists      | Log level detection              |
| .find("x")           | Position of substring (-1=absent)| Parsing structured logs        |
| f"...{var}..."       | Embed variables                | SQL queries, log messages        |
| len(string)          | Count characters               | Validating field lengths         |

---

### 3.5 bool (Boolean)

Only two values: True and False. Capital T and F (unlike JS lowercase true/false).

Hidden fact: bool is a subclass of int. True == 1, False == 0.
```python
print(True + True)    # 2
print(True + 1)       # 2
print(int(True))      # 1
print(int(False))     # 0
```

Real DE Pattern - Counting valid records:
```python
records = [
    {"status": "VALID",   "amount": 100.0},
    {"status": "INVALID", "amount": -5.0},
    {"status": "VALID",   "amount": 200.0},
    {"status": "INVALID", "amount": 0.0},
]
valid_count = sum(r["status"] == "VALID" for r in records)
print(f"Valid: {valid_count}")    # Valid: 2
```
r["status"] == "VALID" -> True (1) or False (0). sum() adds them. Pythonic.

---

### 3.6 None (NoneType - Python's null)

The explicit absence of a value.
```python
last_run      = None
error_message = None
print(type(None))    # <class 'NoneType'>
```

Critical Rule - Always check with "is None", not "== None":
```python
if last_run is None:    # CORRECT
    print("First run.")
if last_run == None:    # WRONG - violates PEP8, linters flag this
    pass
```

Real DE Pattern - Handling NULLs from databases:
```python
records = [
    {"order_id": 1001, "discount": 50.0},
    {"order_id": 1002, "discount": None},    # NULL in database -> None in Python
]
for r in records:
    discount = r["discount"] or 0.0    # None is falsy -> becomes 0.0
    final = 500.0 - discount
    print(f"Order {r['order_id']}: {final}")
# Order 1001: 450.0
# Order 1002: 500.0
```

---

### 3.7 list (Mutable Ordered Sequence)

Mental model:
```
A train with numbered seats.
Seat 0 is the first coach. Seat -1 is the last.

Index:   0      1      2      3
       [101,  202,  303,  404]
                              ^-- index -1
```

All Critical List Methods:
```python
orders = [101, 202, 303, 404]

orders.append(505)        # Add ONE item to END
orders.insert(1, 999)     # Insert 999 at position 1
last   = orders.pop()     # Remove + return LAST item
second = orders.pop(1)    # Remove + return item at index 1
orders.remove(303)        # Remove FIRST occurrence of value 303
orders.sort()             # Sort IN-PLACE (returns None!)
orders.reverse()          # Reverse IN-PLACE (returns None!)
print(len(orders))        # Count items
print(orders[0:2])        # Slice: items at index 0 and 1
```

.sort() vs sorted() - The Trap Interviewers Test:
```python
amounts = [500, 100, 300, 200, 400]

sorted_amounts = sorted(amounts)    # NEW list, original UNCHANGED
print(sorted_amounts)   # [100, 200, 300, 400, 500]
print(amounts)          # [500, 100, 300, 200, 400]  <-- untouched!

amounts.sort()          # Modifies ORIGINAL, returns None

wrong = amounts.sort()  # THE BUG
print(wrong)            # None  <-- in-place modifier trap!
```

---

### 3.8 dict (Key -> Value Store)

Mental model:
```
A PO Box wall at a post office.
Every unique key (box number) opens an exact value (parcel).
No sequential searching - you go directly to the right box.
Lookup is O(1) regardless of how many keys exist.
```

All Critical Dictionary Methods:
```python
order = {"order_id": 1001, "amount": 499.95, "status": "PENDING"}

# SAFE access - never crashes, returns default if key missing
order.get("discount", 0.0)           # 0.0 (key missing, default returned)

# UNSAFE access - crashes with KeyError!
order["missing_key"]                 # KeyError: 'missing_key' -> CRASH

# Iteration
for key, value in order.items():     # Most common loop pattern
    print(f"  {key}: {value}")

# Add / Update
order["discount"]  = 50.0            # Add new key
order["status"]    = "COMPLETED"     # Update existing key

# .pop(key) - Remove and return value
removed = order.pop("discount")      # removed = 50.0

# .update() - Merge another dict IN-PLACE (returns None!)
order.update({"warehouse": "BLR-01"})
# NEVER: print(order.update(...)) -> prints None!

# .setdefault(key, default) - Add key ONLY if it does not exist
order.setdefault("priority", "NORMAL")   # Adds priority = "NORMAL"
order.setdefault("status", "PENDING")    # status exists -> NO change

# Membership check
print("order_id" in order)    # True
print("tax" in order)         # False
```

JS vs Python - critical difference:
```python
# JavaScript: missing key -> undefined (no crash)
# Python:     missing key -> KeyError  (hard crash!)

user = {"name": "Akshay"}
print(user["age"])          # KeyError: CRASH
print(user.get("age"))      # None    <- safe
print(user.get("age", 0))   # 0       <- safe with default
```

---

### 3.9 set (Unique, Unordered Collection)

Mental model:
```
A fingerprint scanner at a conference.
If the same person enters 5 times, counted only once.
Order does not matter. Membership check is O(1) instant.
```

All Critical Set Methods:
```python
active_users = {"u101", "u202", "u303"}
vip_users    = {"u202", "u404"}

active_users.add("u404")         # Add one item (no duplicates)
active_users.discard("u999")     # Remove SAFELY - no crash if missing
# active_users.remove("u999")   # Would crash with KeyError!

# Set OPERATIONS
all_users   = active_users | vip_users    # Union: in EITHER
both        = active_users & vip_users    # Intersection: in BOTH
only_active = active_users - vip_users    # Difference: in A not B

print(all_users)     # {'u101', 'u202', 'u303', 'u404'}
print(both)          # {'u202', 'u404'}
print(only_active)   # {'u101', 'u303'}
```

Why sets beat lists for membership checks:
```python
"192.168.1.1" in blacklist_list    # O(N) - scans every element, slow!
"192.168.1.1" in blacklist_set     # O(1) - hash table, always instant!
```

---

### 3.10 tuple (Immutable Fixed Sequence)

Mental model:
```
A tamper-proof sealed evidence bag.
Once sealed and logged, nobody can add, remove, or swap anything.

list  -> Shopping cart (add, remove, change anytime)
tuple -> Sealed evidence bag (locked permanently at creation)
```

Creating tuples:
```python
db_config = ("prod-db.company.com", 5432, "postgres")
coords    = (12.9716, 77.5946)

single    = (42,)     # ONE-ITEM tuple - the trailing comma is MANDATORY!
not_tuple = (42)      # Just an int in parentheses!

print(type(single))      # <class 'tuple'>
print(type(not_tuple))   # <class 'int'>
```

Accessing (identical to lists):
```python
db_config = ("prod-db.company.com", 5432, "postgres")
print(db_config[0])     # prod-db.company.com
print(db_config[-1])    # postgres (last)
print(db_config[0:2])   # ('prod-db.company.com', 5432)
```

Only 2 methods exist (because immutable):
```python
codes = (200, 404, 200, 500, 200, 404)

# .count(value) - How many times does this value appear?
print(codes.count(200))    # 3
print(codes.count(404))    # 2

# .index(value) - What position is this value at?
stages = ("extract", "validate", "transform", "load")
print(stages.index("transform"))    # 2

# Safe usage - guard with 'in' first:
if "archive" in stages:
    pos = stages.index("archive")
```

Tuple Unpacking - The Most Powerful Feature:
```python
db_config = ("prod-db.company.com", 5432, "postgres")

host, port, user = db_config    # Unpack into named variables
print(f"Connecting to {host}:{port} as {user}")
# Connecting to prod-db.company.com:5432 as postgres
```

Functions returning multiple values - always as tuples:
```python
def get_stats(records):
    total = len(records)
    valid = sum(1 for r in records if r["status"] == "VALID")
    return (total, valid, total - valid)

total, valid, invalid = get_stats(records)
print(f"Total: {total} | Valid: {valid} | Invalid: {invalid}")
```

Tuple as dictionary keys (lists CANNOT do this):
```python
cache = {}
key   = ("orders_pipeline", "2026-09-25")
cache[key] = {"rows": 1_250_000, "duration_s": 47}
print(cache[("orders_pipeline", "2026-09-25")])
```

What happens when you try to mutate:
```python
db_config = ("prod-db.company.com", 5432, "postgres")
db_config[1] = 3306          # TypeError: tuple object does not support item assignment
db_config.append("new_db")   # AttributeError: tuple has no attribute append
```

Tuple vs List - Decision Guide:
| Question                                      | Use list | Use tuple |
|:----------------------------------------------|:---------|:----------|
| Will this data change?                        | Yes      | No        |
| Is the order and count fixed?                 | No       | Yes       |
| Is this a config or coordinate?               | No       | Yes       |
| Passing to a function that might mutate it?   | No       | Yes       |
| Needed as a dictionary key?                   | Cannot   | Yes       |

---

## 4. The In-Place Modifier Rule - The #1 Python Trap

```
RULE: Methods that MODIFY IN-PLACE return None.
      NEVER assign or print them directly.

WRONG:
  result = my_list.sort()              -> result is None!
  print(my_dict.update({...}))         -> prints None!

CORRECT:
  my_list.sort()                       -> then use my_list
  my_dict.update({...})                -> then print my_dict
```

Methods that return None (modify in-place):
- list.sort(), list.reverse(), list.append(), list.extend()
- dict.update(), dict.clear()
- set.add(), set.discard()

Methods that return a NEW object (original untouched):
- sorted(list)    -> new sorted list
- str.strip(), str.lower(), str.replace()  -> new string
- set | set, set & set, set - set          -> new set

---

## 5. Data Type Selection - Unifying Mental Picture

```
WHICH PYTHON TYPE DO I REACH FOR?
         |
         +-- Text / strings                  --> str
         +-- Whole number                    --> int
         +-- Decimal number (not money)      --> float
         +-- Exact decimal (money/finance)   --> Decimal
         +-- True or False                   --> bool
         +-- Value does not exist yet        --> None
         +-- Ordered, WILL change            --> list   [ ]
         +-- Ordered, MUST NOT change        --> tuple  ( )
         +-- Unique items, O(1) lookup       --> set    { }
         +-- Key -> Value lookup             --> dict  {k: v}
```

---

## 6. FAANG Interview Question Vault

### Junior Level

Q1: What is the difference between a list and a tuple in Python?
Benchmark answer: "Both are ordered sequences. A list is mutable - you can add, remove, and change
elements. A tuple is immutable - once created, it cannot be modified. I use tuples for data that
should never change: database configs, GPS coordinates, function return values. I use lists when I
need to build up, filter, or transform a sequence."
Red flag: "Tuples use () and lists use []" - this is syntax, not concept.

---

Q2: Why use dict.get("key", default) instead of dict["key"]?
Benchmark answer: ".get() is safe access. If the key does not exist, it returns the default instead
of crashing with a KeyError. In data pipelines we always use .get() because incoming records from
external systems are often missing fields - crashing on a missing key would take down the entire
pipeline."

---

Q3: What does this print and why?
```python
nums = [3, 1, 2]
result = nums.sort()
print(result)
```
Benchmark answer: "It prints None. .sort() modifies the list in-place and returns None. This is the
in-place modifier trap. Correct approach: nums.sort() on one line, print(nums) on the next."
Red flag: Saying it prints [1, 2, 3].

---

### Mid Level

Q4: You have a 50 GB CSV on a Linux server and need to check if it has ERROR lines.
What is the single most efficient command?
Benchmark answer: grep -c "ERROR" pipeline.log counts matches without loading the full file.
Or grep "ERROR" pipeline.log | head -n 5 to preview the first 5 errors.

---

Q5: What is the time complexity of membership checks in list vs set? Why does it matter in DE?
Benchmark answer: "List is O(N) - scans every element. Set is O(1) - uses a hash table.
When checking a customer ID against 10 million blacklisted IDs, a list takes seconds.
A set is instant. We always convert lookup lists to sets for performance."

---

Q6: Why does Python have both float and Decimal? When would you use each?
Benchmark answer: "float is fast but imprecise: 0.1 + 0.2 gives 0.30000000000000004.
For metrics and analytics where tiny errors do not matter, float is fine. For financial data -
prices, taxes, invoices - float errors cause accounting bugs. Decimal provides exact decimal
arithmetic. Any money calculation in a DE pipeline must use Decimal."

---

### Senior Level

Q7: Explain why passing a mutable object to a function is dangerous in a distributed pipeline.
Benchmark answer: "Python passes mutable objects by reference. If a function modifies a list or
dict passed to it, the original is also changed - this is a side effect. In a Spark job running
across 200 executors, an accidental in-place mutation in one transformation stage can silently
corrupt the data fed to downstream stages. The fix: use immutable types like tuples, copy the
object before modifying it, or write pure functions that return new objects rather than modifying
inputs."

---

## 7. Today's Code Review - Your Exercises

Overall Score: 82% (33/40)

| Exercise             | Score | Key Issue                                                  |
|:---------------------|:------|:-----------------------------------------------------------|
| String Cleaning      | 9/10  | Space before \n in f-string causes leading indent          |
| Dictionary Ops       | 6/10  | print(dict.update()) prints None - in-place modifier trap  |
| Set Deduplication    | 10/10 | Perfect - all three set operations correct                 |
| Tuple Pipeline       | 8/10  | Variable naming: Total/Error should be total/error_count   |

The corrected Exercise 2:
```python
ordered_record = {"order_id": 2001, "amount": 850.0}

discount = ordered_record.get("discount", 0.0)
ordered_record.setdefault("tax", 153.0)
final_val = ordered_record["amount"] + ordered_record["tax"] - discount

ordered_record.update({"amount": final_val})    # Separate from print!
print(ordered_record)
# {'order_id': 2001, 'amount': 1003.0, 'tax': 153.0}
```

Python naming conventions to follow every single time:
```
Classes     -> CamelCase:    class DataPipeline
Variables   -> snake_case:   total_count, error_message, final_val
Functions   -> snake_case:   def run_pipeline(), def process_batch()
Constants   -> UPPER_SNAKE:  MAX_RETRIES = 3, BATCH_SIZE = 256
```

---

## 8. Debugging Challenges (Attempt Before Day 3 - No Hints)

Bug 1: What is wrong here and what error does it throw?
```python
pipeline_configs = ("host", "5432", "postgres")
pipeline_configs[1] = "3306"
print(pipeline_configs)
```

Bug 2: What does this actually print? Why?
```python
data = {"order": 1001, "amount": 500}
data.update({"status": "COMPLETED"})
print(data.update({"verified": True}))
```

Bug 3: Why does this fail and how do you fix it?
```python
user_ids = [101, 202, 303, 404, 101, 202]
unique = set(user_ids)
unique.append(505)
print(unique)
```

---

## 9. Spaced Repetition Checklist

Review on Day 3, Day 9, and Day 30. Cover the answer. Say it out loud first.

- [ ] What is the difference between list and tuple? When do you use each?
- [ ] Why use .get("key", default) instead of dict["key"]? What crash does it prevent?
- [ ] What do in-place methods (.sort(), .update(), .append()) return?
- [ ] What is 0.1 + 0.2 in Python? How do you fix it for financial data?
- [ ] What is the O(1) vs O(N) difference between set and list membership checks?
- [ ] How do you correctly check if a variable is None?
- [ ] What is tuple unpacking? When does a function return a tuple?
- [ ] Name 5 string methods and their DE use cases - from memory, no notes.

---

Day 02 complete - 2026-09-25
Next: Day 03 - SQL Table Foundations, DSA Frequency Counter & JS Block Scope