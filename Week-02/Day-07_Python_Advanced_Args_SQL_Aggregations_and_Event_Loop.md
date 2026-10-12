# Day 07 - Python Functional Deep Dive, SQL Aggregation Masterclass, and JS Event Loop

**Date**: 2026-10-12
**Week**: Week 2 - Real Data Sources & Analytics Engineering
**Score**: 97% (29/30) - Masterclass execution on Checkpoints
**Running Average**: ~85%
**Topics**:
- Python: `*args`, `**kwargs`, Unpacking, `map()`, `filter()`, `sorted()`, Comprehensions, Copying, Generics
- SQL: `GROUP BY`, `HAVING`, Aggregates (`COUNT(*)` vs `COUNT(col)`), `CASE WHEN`, Execution Order
- DSA: Heap vs Hash Map Deep Dive
- JS: Event Loop mechanics, Microtasks vs Macrotasks, Node.js vs Browser runtime

---

## 1. Executive Summary - Where Today's Skills Fit in the DE Architecture

```
                       REAL-WORLD ANALYTICS & ETL ARCHITECTURE
                       
    [Raw Data Source: CSV / API / Database]
                       │
                       ▼
    +───────────────────────────────────────────+
    │        Python Transformation Layer        │
    │                                           │
    │  *args / **kwargs  --> Flexible ingestion │
    │  * / ** unpacking  --> Safe record cloning│
    │  list / dict comp  --> In-memory cleaning │
    │  generators ()     --> Streaming 10M rows │
    │  any() / all()     --> Pipeline validation│
    +───────────────────────────────────────────+
                       │
                       ▼
    +───────────────────────────────────────────+
    │            MySQL / Data Warehouse         │
    │                                           │
    │  GROUP BY status, currency                │
    │  COUNT(order_id) vs COUNT(*)              │
    │  CASE WHEN amount > 1000 THEN 'HIGH'      │
    │  HAVING SUM(amount) > 5000                │
    │  Execution Order: FROM -> WHERE -> GROUP  │
    +───────────────────────────────────────────+
                       │
                       ▼
    +───────────────────────────────────────────+
    │         Web Dashboard / Node API          │
    │                                           │
    │  Single-Threaded Event Loop               │
    │  Call Stack -> Microtasks -> Macrotasks   │
    │  Non-blocking async DB queries            │
    +───────────────────────────────────────────+
```

---

## 2. MODULE 1 - Python Functional & Argument Mastery

---

### 2.1 The Problem `*args` and `**kwargs` Solve

**Analogy**: 
Imagine an airport luggage policy. 
- A **strict baggage rule** requires exactly 1 carry-on suitcase of 55cm. If you bring 2 bags or a backpack, security rejects you. That is `def add(a, b)`.
- An **expandable cargo container** says: "Throw in as many bags as you have, we will pack them into one pallet." That is `*args`.
- A **customs manifest** says: "Hand me any number of labeled parcels with tags." That is `**kwargs`.

---

### 2.2 Positional vs Keyword Arguments: The Foundation

Before using `*` and `**`, you must understand how Python maps arguments:

```python
def make_order(order_id, amount, currency="INR"):
    """Creates an order summary."""
    return f"Order {order_id}: {amount} {currency}"

# 1. Positional Arguments (mapped by ORDER):
print(make_order(101, 500.0))
# Output: Order 101: 500.0 INR

# 2. Keyword Arguments (mapped by NAME):
print(make_order(amount=950.0, order_id=102, currency="USD"))
# Output: Order 102: 950.0 USD
```

Rule: Positional arguments MUST always come before keyword arguments in function calls.
`make_order(amount=500, 101)` raises `SyntaxError: positional argument follows keyword argument`.

---

### 2.3 `*args` with Normal Parameters

`*args` collects any extra positional arguments into a **tuple**.

```
ASCII MEMORY PICTURE:

   call: log_pipeline("orders_etl", "ingest", "validate", "load")
                              │          │          │          │
                              ▼          └──────────┬──────────┘
                           job_name                 │
                       "orders_etl"                 ▼
                                                  args (tuple)
                                        ("ingest", "validate", "load")
```

```python
def log_pipeline(job_name, *stages):
    """Logs pipeline name and all arbitrary stages."""
    print(f"Pipeline: {job_name}")
    print(f"Stages tuple: {stages} (Count: {len(stages)})")
    for idx, stage in enumerate(stages, 1):
        print(f"  Step {idx}: {stage}")

log_pipeline("orders_etl", "ingest", "validate", "load")
```
Output:
```
Pipeline: orders_etl
Stages tuple: ('ingest', 'validate', 'load') (Count: 3)
  Step 1: ingest
  Step 2: validate
  Step 3: load
```

Notice: `job_name` takes the first argument. `*stages` collects whatever is left.

---

### 2.4 `**kwargs` with Normal Parameters

`**kwargs` collects extra named arguments into a **dictionary**.

```python
def create_customer(customer_id, name, **attributes):
    """Creates a customer profile with arbitrary metadata."""
    print(f"Customer ID: {customer_id} | Name: {name}")
    print(f"Attributes dict: {attributes}")
    for key, value in attributes.items():
        print(f"  - {key}: {value}")

create_customer(101, "Akshay Kumar", city="Bangalore", age=28, plan="Enterprise")
```
Output:
```
Customer ID: 101 | Name: Akshay Kumar
Attributes dict: {'city': 'Bangalore', 'age': 28, 'plan': 'Enterprise'}
  - city: Bangalore
  - age: 28
  - plan: Enterprise
```

---

### 2.5 Strict Argument Ordering Rules in Python

Python enforces a strict parameter hierarchy in function definitions:

```
        THE UNIVERSAL PARAMETER ORDER HIERARCHY
        
  def func( pos_only, /, positional, default=val, *args, kw_only, **kwargs ):
              │       │      │             │        │       │        │
              │       │      │             │        │       │        └─ Collects extra kwargs (dict)
              │       │      │             │        │       └────────── Must be passed as key=value
              │       │      │             │        └────────────────── Collects extra pos args (tuple)
              │       │      │             └─────────────────────────── Has a fallback value
              │       │      └───────────────────────────────────────── Standard positional/keyword
              │       └──────────────────────────────────────────────── Positional-only boundary
              └──────────────────────────────────────────────────────── MUST be passed positionally
```

Example of Keyword-Only Arguments (`*` or after `*args`):
```python
def connect_db(host, port, *, timeout=30, ssl=True):
    """Keyword-only parameters protect against accidental parameter swapping."""
    return f"Connecting to {host}:{port} (timeout={timeout}, ssl={ssl})"

# Valid:
print(connect_db("localhost", 3306, timeout=10))

# Invalid - will raise TypeError: connect_db() takes 2 positional arguments but 3 were given
# connect_db("localhost", 3306, 10)
```

Why Data Engineers use Keyword-Only arguments:
When configuring database connections or Airflow operators, passing `30, True` positionally leads to silent catastrophic bugs if order changes. Forcing `timeout=30, ssl=True` makes production code self-documenting.

---

### 2.6 The Great Distinction: Packing vs Unpacking (`*` and `**`)

Beginners constantly confuse packing with unpacking. They are mirror opposites:

```
+-------------------------------------------------------------------------+
| OPERATION  | WHERE IT HAPPENS         | WHAT IT DOES                   |
+-------------------------------------------------------------------------+
| PACKING    | Function Definition      | Collects separate values into   |
|            | def f(*args, **kwargs)   | a tuple or dict.                |
+-------------------------------------------------------------------------+
| UNPACKING  | Function Call / Literal  | Explodes a collection into      |
|            | f(*my_list, **my_dict)   | individual values.              |
+-------------------------------------------------------------------------+
```

#### Positional Unpacking with `*`
```python
def calculate_box(length, width, height):
    return length * width * height

dims = [10, 20, 5]

# Without unpacking:
# calculate_box(dims[0], dims[1], dims[2]) -- verbose and brittle!

# With unpacking:
volume = calculate_box(*dims)
print(f"Volume: {volume}")
# Output: Volume: 1000
```

#### Dictionary Unpacking with `**`
```python
order_data = {
    "order_id": 3001,
    "amount": 499.95,
    "status": "VALID",
    "currency": "INR",
    "customer_id": 101
}

# SQL insert query placeholder unpacking:
def format_row(order_id, amount, status, currency, customer_id):
    return f"INSERT: {order_id} | {amount} {currency}"

print(format_row(**order_data))
# Output: INSERT: 3001 | 499.95 INR
```

#### Safe Record Cloning with Dictionary Unpacking
This is how you solve the in-place mutation trap permanently!
```python
raw_order = {"order_id": 3002, "amount": -75.0, "status": "failed"}

# Creates a brand-new dict in memory without touching raw_order:
cleaned_order = {
    **raw_order,
    "amount": max(raw_order["amount"], 0.0),
    "status": raw_order["status"].upper()
}

print("Cleaned:", cleaned_order)
print("Original:", raw_order)  # Unaltered!
```
Output:
```
Cleaned: {'order_id': 3002, 'amount': 0.0, 'status': 'FAILED'}
Original: {'order_id': 3002, 'amount': -75.0, 'status': 'failed'}
```

---

### 2.7 Default Arguments & The Infamous Mutable Default Trap

**The Trap**:
```python
def append_order(order_id, orders=[]):  # DANGEROUS! orders is evaluated ONCE at import
    orders.append(order_id)
    return orders

print(append_order(101))  # [101]
print(append_order(102))  # [101, 102] <- BUG! Shares the exact same list across calls!
```

**The FAANG-Standard Fix (Sentinel `None`)**:
```python
def append_order(order_id, orders=None):
    """Always use None as default for mutable containers."""
    if orders is None:
        orders = []
    orders.append(order_id)
    return orders

print(append_order(101))  # [101]
print(append_order(102))  # [102] - Clean, independent list!
```

---

### 2.8 Functions as First-Class Citizens & Higher-Order Functions

In Python, functions are objects like integers or strings. You can:
1. Assign them to variables.
2. Pass them as arguments to other functions.
3. Return them from functions (Closures).

```python
def clean_currency(val):
    return val.strip().upper()

def clean_amount(val):
    return max(float(val), 0.0)

# Pipeline dictionary mapping column name to its cleaning function:
cleaners = {
    "currency": clean_currency,
    "amount": clean_amount
}

raw_field = " inr "
cleaned_field = cleaners["currency"](raw_field)
print(f"Cleaned field: '{cleaned_field}'")
# Output: Cleaned field: 'INR'
```

---

### 2.9 Lambda Functions: Strengths & Strict Limitations

A lambda is a single-expression anonymous function.
Syntax: `lambda arg1, arg2: expression`

```python
# Appropriate Lambda (One-line transformer or sort key):
get_amount = lambda r: r["amount"]

# INAPPROPRIATE Lambda (Complex logic, assignments, multiple statements):
# lambda x: if x > 0: ... <- SyntaxError! Lambda CANNOT contain statements or loops!
```

Rule: If logic requires more than one simple expression or is used in multiple places, ALWAYS use `def`.

---

### 2.10 `sorted()` vs `list.sort()` Deep Dive

```
+--------------------------------------------------------------------------+
| METHOD         | MUTATES ORIGINAL? | RETURNS         | WORKS ON          |
+--------------------------------------------------------------------------+
| list.sort()    | YES (in-place)    | None            | Lists only        |
| sorted(iter)   | NO (safe copy)    | New sorted list | Any iterable      |
+--------------------------------------------------------------------------+
```

```python
orders = [
    {"id": 101, "amount": 450.0},
    {"id": 102, "amount": 120.0},
    {"id": 103, "amount": 980.0}
]

# Sort by amount descending using sorted() + lambda key:
sorted_by_amt = sorted(orders, key=lambda x: x["amount"], reverse=True)

print("Top order:", sorted_by_amt[0])
print("Original orders[0]:", orders[0])  # Safe and intact!
```
Output:
```
Top order: {'id': 103, 'amount': 980.0}
Original orders[0]: {'id': 101, 'amount': 450.0}
```

---

### 2.11 Lazy Evaluation: `map()` and `filter()` vs Comprehensions

`map()` and `filter()` are **generators/iterators**. They do NOT compute values immediately!

```python
numbers = [-10, 20, -30, 40]

m = map(lambda x: x * 2, numbers)
f = filter(lambda x: x > 0, numbers)

print(m)  # <map object at 0x...> (Zero computations performed yet)
print(f)  # <filter object at 0x...> (Zero computations performed yet)

# Must be materialized with list() or a for loop:
print(list(m))  # [-20, 40, -60, 80]
print(list(f))  # [20, 40]
```

#### Why Comprehensions are Preferred in Modern Python
```python
# map + filter functional chain:
result_func = list(map(lambda x: x * 2, filter(lambda x: x > 0, numbers)))

# Equivalent List Comprehension (Much more readable!):
result_comp = [x * 2 for x in numbers if x > 0]

print(result_comp)  # [40, 80]
```

---

### 2.12 Dictionary, Set Comprehensions & Generator Expressions

```python
orders = [
    {"id": 101, "status": "VALID", "amount": 500},
    {"id": 102, "status": "FAILED", "amount": 0},
    {"id": 103, "status": "VALID", "amount": 750}
]

# 1. Dictionary Comprehension (id -> amount lookup table):
amount_lookup = {o["id"]: o["amount"] for o in orders if o["status"] == "VALID"}
print("Lookup dict:", amount_lookup)
# Output: Lookup dict: {101: 500, 103: 750}

# 2. Set Comprehension (extract unique statuses):
unique_statuses = {o["status"] for o in orders}
print("Statuses set:", unique_statuses)
# Output: Statuses set: {'VALID', 'FAILED'}

# 3. Generator Expression (Streaming calculation without loading into RAM):
# Uses () instead of []
total_amount_gen = (o["amount"] for o in orders)
print(total_amount_gen)  # <generator object <genexpr> at 0x...>
print("Total sum:", sum(total_amount_gen))  # 1250
```

Why Generators Matter in Data Engineering:
If a file has 50 million rows, `[r for r in file]` consumes 16 GB of RAM and crashes with `OutOfMemoryError`. A generator expression `(r for r in file)` consumes **less than 1 KB of RAM**, streaming rows one by one.

---

### 2.13 `zip()`, `enumerate()`, `any()`, `all()`: Essential DE Utilities

```python
# 1. zip(): Combines parallel sequences
columns = ["order_id", "customer_id", "amount"]
row_values = [3001, 101, 499.95]

order_record = dict(zip(columns, row_values))
print("Zipped record:", order_record)
# Output: Zipped record: {'order_id': 3001, 'customer_id': 101, 'amount': 499.95}

# 2. enumerate(): Index tracking without manual counters
statuses = ["PENDING", "PROCESSING", "COMPLETED"]
for step, status in enumerate(statuses, start=1):
    print(f"Step {step}: {status}")

# 3. any() and all(): Pipeline validation assertions
amounts = [100.0, 250.0, -5.0, 400.0]

has_negative = any(amt < 0 for amt in amounts)
all_positive = all(amt > 0 for amt in amounts)

print(f"Has negative records? {has_negative}")  # True
print(f"Are all records valid? {all_positive}")  # False
```

---

### 2.14 Shallow Copy vs Deep Copy

```python
import copy

original_batch = [
    {"batch_id": 1, "metadata": {"source": "s3", "retries": 0}}
]

# Shallow copy:
shallow_batch = original_batch.copy()

# Deep copy:
deep_batch = copy.deepcopy(original_batch)

# Mutating nested metadata:
original_batch[0]["metadata"]["retries"] = 5

print("Shallow copy saw mutation?", shallow_batch[0]["metadata"]["retries"])  # 5 (SHARED!)
print("Deep copy saw mutation?", deep_batch[0]["metadata"]["retries"])        # 0 (COMPLETELY ISOLATED!)
```

---

## 3. MODULE 2 - SQL Aggregation Masterclass (`GROUP BY`, `HAVING`, Aggregates)

---

### 3.1 The Analogy: The Laundry Sorting Bins

**Analogy**: 
Imagine dumping 100 mixed clothes on the floor. 
- You don't inspect each shirt individually. 
- You set up **3 sorting hampers**: Whites, Colors, Delicates. That is `GROUP BY`.
- You count how many shirts are in Whites, or weigh the total laundry basket. That is `COUNT(*)` and `SUM()`.
- If a laundry hamper has fewer than 5 clothes, you don't run the washing machine yet. That is `HAVING COUNT(*) >= 5`.

```
ASCII VISUALIZATION OF GROUP BY:

   Raw orders table:
   [3001, 'INR', 500]
   [3002, 'USD', 100]
   [3003, 'INR', 300]
   [3004, 'EUR', 200]
   [3005, 'INR', 200]

             │
             ▼  GROUP BY currency
   ┌──────────────────────┬──────────────────────┬──────────────────────┐
   │     'INR' Bucket     │     'USD' Bucket     │     'EUR' Bucket     │
   │  3001 (500)          │  3002 (100)          │  3004 (200)          │
   │  3003 (300)          │                      │                      │
   │  3005 (200)          │                      │                      │
   └──────────────────────┴──────────────────────┴──────────────────────┘
             │                      │                      │
             ▼ COUNT(*), SUM(amt)   ▼ COUNT(*), SUM(amt)   ▼ COUNT(*), SUM(amt)
        Count: 3, Sum: 1000    Count: 1, Sum: 100     Count: 1, Sum: 200
```

---

### 3.2 Aggregate Functions Deep Dive

Aggregate functions collapse multiple rows into a single scalar value.

```sql
COUNT(*)        -- Counts all rows (including rows with NULLs)
COUNT(column)   -- Counts rows where column IS NOT NULL
COUNT(DISTINCT) -- Counts unique non-NULL values
SUM(column)     -- Sums all non-NULL values
AVG(column)     -- Computes arithmetic mean (ignores NULLs)
MIN(column)     -- Smallest value
MAX(column)     -- Largest value
```

#### The Critical Interview Trap: `COUNT(*)` vs `COUNT(column)` vs `COUNT(DISTINCT column)`

Suppose a table `orders` has 4 rows:
```
order_id | discount
---------+---------
1        | 50.00
2        | 100.00
3        | NULL
4        | 50.00
```

```sql
SELECT
    COUNT(*)                 AS total_rows,           -- Returns 4
    COUNT(discount)          AS non_null_discounts,   -- Returns 3 (ignores NULL!)
    COUNT(DISTINCT discount) AS unique_discounts      -- Returns 2 (50.00 and 100.00)
FROM orders;
```

---

### 3.3 The Golden Rule of `GROUP BY`

> **Every column in the `SELECT` list must either be listed in the `GROUP BY` clause OR enclosed inside an aggregate function (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).**

```sql
-- INVALID QUERY (Produces error or undefined behavior):
SELECT status, order_id, COUNT(*)
FROM orders
GROUP BY status;
```
*Why is this invalid?*
Because the bucket for `'VALID'` contains multiple order IDs (e.g. 3001, 3003). SQL cannot collapse multiple distinct order IDs into a single row unless you aggregate them!

```sql
-- VALID QUERY:
SELECT status, COUNT(order_id) AS total_orders, SUM(amount) AS total_revenue
FROM orders
GROUP BY status;
```

---

### 3.4 `WHERE` vs `HAVING`: The Fundamental Distinction

```
+--------------------------------------------------------------------------+
| CLAUSE   | WHEN IT EXECUTES           | WHAT IT FILTERS                  |
+--------------------------------------------------------------------------+
| WHERE    | BEFORE grouping & aggs     | Individual rows                  |
| HAVING   | AFTER grouping & aggs      | Aggregated groups / buckets      |
+--------------------------------------------------------------------------+
```

```sql
-- Scenario: Find currencies where high-value orders (> 100) generate total revenue > 1000
SELECT
    currency,
    COUNT(*)    AS order_count,
    SUM(amount) AS total_revenue
FROM orders
WHERE amount > 100            -- 1. Filters rows FIRST (removes small orders)
GROUP BY currency             -- 2. Groups remaining rows
HAVING SUM(amount) > 1000;    -- 3. Filters groups AFTER calculation
```

---

### 3.5 Grouping by Multiple Columns

You can create composite buckets based on multiple dimensions:

```sql
SELECT
    c.city,
    o.currency,
    COUNT(o.order_id) AS order_count,
    SUM(o.amount)     AS total_amount
FROM orders AS o
INNER JOIN customers AS c ON c.customer_id = o.customer_id
GROUP BY c.city, o.currency;
```
Output:
```
city      | currency | order_count | total_amount
Bangalore | INR      | 2           | 839.95
Bangalore | GBP      | 1           | 820.00
Delhi     | INR      | 2           | 1870.00
Mumbai    | USD      | 1           | 75.50
```

#### Why Group by `customer_id, name`?
```sql
SELECT c.customer_id, c.name, SUM(o.amount)
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;  -- Prevents collision if 2 customers share the name 'Rahul Sharma'
```

---

### 3.6 Advanced: `LEFT JOIN` Aggregations & `COALESCE()`

**Classic Interview Trap**: Counting orders for customers who have NEVER ordered.

```sql
-- TRAP QUERY:
SELECT c.name, COUNT(*) AS order_count
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
-- ERROR: Customers with 0 orders get count = 1 because the joined NULL row counts as 1 row!

-- PRODUCTION QUERY:
SELECT
    c.name,
    COUNT(o.order_id)            AS total_orders, -- COUNT(col) ignores NULL! Returns 0!
    COALESCE(SUM(o.amount), 0.0) AS total_spent   -- COALESCE replaces NULL with 0.0!
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

---

### 3.7 `CASE WHEN` Conditional Aggregations

`CASE WHEN` allows in-query data transformation and pivot reporting:

```sql
SELECT
    c.name,
    COUNT(o.order_id) AS total_orders,
    SUM(CASE WHEN o.status = 'COMPLETED' THEN o.amount ELSE 0 END) AS completed_revenue,
    SUM(CASE WHEN o.status = 'FAILED' THEN 1 ELSE 0 END)           AS failed_order_count
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

---

### 3.8 The Master Blueprint: SQL Logical Query Execution Order

When you write SQL, it is executed in an entirely different order than written:

```
        WRITTEN SYNTAX                   LOGICAL EXECUTION ORDER
        
    1.  SELECT ...                 ┌───► 1.  FROM & JOIN (Load tables & join)
    2.  FROM ...                   │     2.  WHERE (Filter individual rows)
    3.  JOIN ... ON ...            │     3.  GROUP BY (Create buckets)
    4.  WHERE ...                  │     4.  HAVING (Filter aggregated buckets)
    5.  GROUP BY ...               ┼───► 5.  SELECT (Evaluate expressions & aliases)
    6.  HAVING ...                 │     6.  DISTINCT (Remove duplicate result rows)
    7.  ORDER BY ...               │     7.  ORDER BY (Sort result rows)
    8.  LIMIT ...                  └───► 8.  LIMIT / OFFSET (Slice top N rows)
```

**Why this matters**:
1. You cannot use aliases in `WHERE`: `SELECT amount * 2 AS double_amt FROM orders WHERE double_amt > 100` FAILS because `WHERE` executes at Step 2, long before `SELECT` aliases are defined at Step 5.
2. You cannot use aggregates in `WHERE`: `WHERE COUNT(*) > 1` FAILS because rows haven't been grouped yet.

---

## 4. MODULE 3 - DSA: Heap vs Hash Map Deep Dive

In Day 6 Checkpoint 3, you referred to a dictionary as a "heap". In FAANG interviews, mixing up these terms is an immediate rejection flag. Here is the definitive distinction:

```
+-------------------------------------------------------------------------------+
| DIMENSION         | HASH MAP (dict in Python)     | HEAP (heapq in Python)    |
+-------------------------------------------------------------------------------+
| Underlying Data   | Hash Table (Array of buckets  | Complete Binary Tree      |
| Structure         | with hash function)           | (Stored as a flat array)  |
+-------------------------------------------------------------------------------+
| Primary Operation | Key-to-Value mapping          | Priority / Extrema lookup |
|                   | seen[val] = idx               | heapq.heappop(min_heap)   |
+-------------------------------------------------------------------------------+
| Key Lookup Time   | O(1) average                  | O(N) (Not searchable!)    |
+-------------------------------------------------------------------------------+
| Min/Max Finding   | O(N) (Must scan all keys)     | O(1) peek, O(log N) pop   |
+-------------------------------------------------------------------------------+
| Element Insertion | O(1) average                  | O(log N)                  |
+-------------------------------------------------------------------------------+
| Real DE Use Case  | Deduplication, Two Sum lookup | Top-K streaming metrics,  |
|                   | Frequency counting            | Merging K sorted logs     |
+-------------------------------------------------------------------------------+
```

---

## 5. MODULE 4 - JavaScript: Event Loop Masterclass

---

### 5.1 The Core Truth

JavaScript is **single-threaded**. It has exactly ONE call stack. It executes ONE instruction at a time.
Yet Node.js servers handle 50,000 concurrent database queries without locking up. The **Event Loop** is the engine that makes this possible.

---

### 5.2 The 4-Part Event Loop Anatomy

```
   ┌──────────────────────────────────────────────────────────────┐
   │                          CALL STACK                          │
   │  Synchronous JS executes here (LIFO order).                  │
   │  If a function takes 10 seconds of CPU, EVERYTHING freezes!  │
   └──────────────────────────────┬───────────────────────────────┘
                                  │ Hands async work off
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                 RUNTIME WEB APIs / LIBUV                     │
   │  Timers (setTimeout), Network (fetch), File I/O (fs.readFile)│
   │  Executes OUTSIDE the JS thread in background C++ threads!   │
   └──────────────────────────────┬───────────────────────────────┘
                                  │ Async task finishes
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                   PRIORITY QUEUE STRUCTURE                   │
   │                                                              │
   │  1. MICROTASK QUEUE (High Priority):                         │
   │     Promises (.then, .catch), queueMicrotask, process.nextTick│
   │                                                              │
   │  2. MACROTASK / CALLBACK QUEUE (Normal Priority):            │
   │     setTimeout, setInterval, setImmediate, I/O callbacks    │
   └──────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                         EVENT LOOP                           │
   │  Rule 1: Check if Call Stack is completely EMPTY.            │
   │  Rule 2: Drain ALL Microtasks until Microtask queue is empty.│
   │  Rule 3: Pick ONE Macrotask and push to Call Stack.          │
   │  Rule 4: Repeat indefinitely!                                │
   └──────────────────────────────────────────────────────────────┘
```

---

### 5.3 Microtasks vs Macrotasks: Priority Proof

```javascript
console.log("1. Sync Start");

setTimeout(() => {
    console.log("4. Macrotask (setTimeout)");
}, 0);

Promise.resolve().then(() => {
    console.log("2. Microtask 1");
}).then(() => {
    console.log("3. Microtask 2");
});

console.log("End of Sync Script");
```
Output:
```
1. Sync Start
End of Sync Script
2. Microtask 1
3. Microtask 2
4. Macrotask (setTimeout)
```

Why `setTimeout` runs last even with `0ms`:
1. `console.log` runs synchronously on the Call Stack.
2. `setTimeout` schedules its callback in the **Macrotask Queue**.
3. `Promise.resolve().then()` schedules its callback in the **Microtask Queue**.
4. When Call Stack empties, the Event Loop checks the Microtask Queue FIRST.
5. Microtask 1 runs, queues Microtask 2. Microtask 2 runs.
6. Only when the Microtask Queue is completely drained does the Event Loop process the Macrotask Queue (`setTimeout`).

---

### 5.4 Browser vs Node.js Event Loop Differences

```
+--------------------------------------------------------------------------+
| FEATURE             | BROWSER ENVIRONMENT       | NODE.JS RUNTIME        |
+--------------------------------------------------------------------------+
| Underlying Engine   | V8 / SpiderMonkey / WebKit| V8 + libuv (C library) |
| Macrotasks          | setTimeout, setInterval   | Timers, I/O, check     |
| Microtasks          | Promises, queueMicrotask  | Promises, nextTick     |
| Highest Priority    | queueMicrotask()          | process.nextTick()     |
| Render Phase        | Paints DOM between tasks  | No DOM rendering       |
+--------------------------------------------------------------------------+
```

---

## 6. FAANG Interview Question Vault

**Q1: In SQL, why does `WHERE COUNT(order_id) > 5` throw an error, and what is the fix?**
> **Answer**: SQL evaluates queries in a strict logical execution order: `FROM` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `SELECT`. The `WHERE` clause executes at Step 2 to filter individual rows before groups or aggregations exist. The aggregation `COUNT(order_id)` is computed at Step 3 (`GROUP BY`). Therefore, group-level filtering must be placed in the `HAVING` clause (`HAVING COUNT(order_id) > 5`), which executes at Step 4.

**Q2: What is the difference between `func(*args)` in a function call vs `def func(*args)` in a definition?**
> **Answer**: In a function definition (`def func(*args)`), `*` is a **packing** operator that collects arbitrary positional arguments into a single tuple. In a function call (`func(*args)`), `*` is an **unpacking** operator that explodes a collection into separate positional arguments.

**Q3: When left-joining customers to orders, why does `COUNT(*)` give incorrect order counts for customers with 0 orders?**
> **Answer**: `COUNT(*)` counts the total number of rows produced by the join. In a `LEFT JOIN`, a customer with no matching orders still produces 1 joined row containing `NULL` values for the order columns. `COUNT(*)` counts that row and returns `1`. The correct approach is `COUNT(o.order_id)`, because `COUNT(column)` ignores `NULL` values and correctly returns `0`.

**Q4: In Python, why should you never write `def append_to(item, target_list=[])`?**
> **Answer**: Default argument expressions in Python are evaluated once at function definition/import time, not at each invocation. If the default is a mutable object like a list, all subsequent calls that omit the argument will share and mutate the exact same list instance in memory. The standard fix is using `target_list=None` and assigning `target_list = []` inside the function body.

**Q5: In JavaScript, what happens if an asynchronous function executes an infinite microtask loop?**
> **Answer**: Because the Event Loop guarantees that all microtasks in the Microtask Queue are drained before any macrotasks or UI rendering updates can run, an endless microtask loop (such as chaining `Promise.resolve().then(...)` recursively) completely starves the Event Loop. Macrotasks (`setTimeout`, I/O) will never execute, and in a browser, the webpage will freeze completely without rendering.

---

## 7. Debugging Challenges for Day 8

**Bug 1 (Python Unpacking Trap)**: What is wrong with this code?
```python
def load_order(order_id, amount, currency="INR"):
    return {"id": order_id, "total": amount, "curr": currency}

raw_data = {"order_id": 5001, "amount": 250.0, "status": "VALID"}
order = load_order(**raw_data)
print(order)
```

**Bug 2 (SQL Grouping Ambiguity)**: Why does this query fail in strict SQL databases?
```sql
SELECT c.name, o.currency, MAX(o.amount)
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
GROUP BY c.name;
```

**Bug 3 (JavaScript Priority Puzzle)**: What will this script output?
```javascript
setTimeout(() => console.log("Timer 1"), 0);

Promise.resolve().then(() => {
    console.log("Promise 1");
    setTimeout(() => console.log("Timer 2"), 0);
}).then(() => {
    console.log("Promise 2");
});

console.log("Sync");
```

---

## 8. Spaced Repetition Checklist

Review on Day 8, Day 14, and Day 38.

- [ ] What is the difference between `*args` packing in definitions vs `*` unpacking in calls?
- [ ] Write a safe dictionary merge in Python using `**` without mutating original dicts.
- [ ] Why does `COUNT(*)` return 1 on a left-joined row with NULLs while `COUNT(column)` returns 0?
- [ ] What are the 8 steps of SQL logical query execution order from memory?
- [ ] How does `HAVING` differ from `WHERE`?
- [ ] Why should default function arguments in Python never be mutable objects like `[]` or `{}`?
- [ ] In the JS Event Loop, why does a Promise callback execute before `setTimeout(fn, 0)`?
- [ ] What is the difference between a Hash Map and a Min-Heap in terms of structure and search time?

---

Day 07 complete - 2026-10-12
Score: 97% (29/30)
Running Average: ~85%
Next: Day 08 - Full Production ETL Pipeline: CSV Ingestion, Python Cleaning, Batch MySQL Loading with Error Handling
