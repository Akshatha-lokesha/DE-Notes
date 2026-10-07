# Day 06 - CSV Reading | Python to MySQL | SQL JOINs | Two Sum | JS Promises

**Date**: 2026-10-07
**Week**: Week 2 - Real Data Sources and Databases
**Score**: 83% (33/40)
**Running Average**: ~82%
**Tracks**: Python CSV + MySQL ETL | SQL INNER/LEFT JOINs | Two Sum (LC 1) | JS Promises + async/await

---

## 1. What Week 2 Is About

```
Week 1: Hardcoded data in Python lists
              |
              v
Week 2: Real data flowing through a real pipeline

raw_orders.csv  -->  Python cleans it  -->  MySQL stores it  -->  SQL queries it
```

Every concept from Week 1 still applies.
The only thing that changes is WHERE the data comes from and WHERE it goes.

---

## 2. Python: Reading CSV Files

### 2.1 The Analogy

A CSV file is a spreadsheet saved as plain text.
Python's csv module is a translator that converts each row into a Python dict.

```
raw_orders.csv (text on disk):
  order_id,amount,status,currency,customer_id
  3001,499.95,VALID,INR,101
  3002,-75.00,VALID,USD,102

csv.DictReader (what you get in Python):
  {"order_id": "3001", "amount": "499.95", "status": "VALID", ...}
  {"order_id": "3002", "amount": "-75.00", "status": "VALID", ...}
```

Each row becomes a dict. Column headers become keys.
This is IDENTICAL to the raw_orders list from Week 1.
Your clean_record() and is_valid() functions work UNCHANGED.

---

### 2.2 csv.reader vs csv.DictReader

```python
import csv

# csv.reader -- gives a LIST per row (access by index -- fragile)
with open('orders.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row[0], row[1])   # order_id, amount by POSITION

# csv.DictReader -- gives a DICT per row (access by name -- safe)
with open('orders.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["order_id"], row["amount"])   # by NAME -- always correct
```

RULE: Always use DictReader for DE work.
Column POSITIONS can change when schema evolves.
Column NAMES rarely change.
Accessing by name makes your code resilient.

---

### 2.3 The Critical Detail: Everything is a String

When CSV reads data, EVERY value comes in as a string.
Even numbers:

```
row["amount"]      is "499.95"   -- string, not float
row["order_id"]    is "3001"     -- string, not int
```

Your clean_record() must do type conversion:

```python
def clean_record(record):
    """Cleans one CSV row and returns a properly typed new dict."""
    return {
        "order_id":    int(record["order_id"]),            # "3001" -> 3001
        "amount":      max(float(record["amount"]), 0.0),  # "-75.0" -> 0.0
        "status":      record["status"].strip().upper(),
        "currency":    record["currency"].strip().upper(),
        "customer_id": int(record["customer_id"]),
    }
```

---

### 2.4 Full CSV Reading Pattern

```python
import csv

def load_from_csv(filepath):
    """Reads a CSV file and returns a list of raw string dicts."""
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))
    return records

orders = load_from_csv('raw_orders.csv')
print(f"Loaded {len(orders)} records")
print("First record:", orders[0])
```
Output:
```
Loaded 10 records
First record: {'order_id': '3001', 'amount': '499.95', 'status': 'VALID', 'currency': 'INR', 'customer_id': '101'}
```

---

## 3. Python to MySQL: INSERT INTO

### 3.1 The Full ETL Flow

```
raw_orders.csv
      |
      v  csv.DictReader
list of raw string dicts
      |
      v  clean_record()
list of cleaned, typed dicts
      |
      v  is_valid()
valid orders only
      |
      v  cursor.execute(INSERT INTO ... VALUES (%s,%s,%s,%s,%s))
orders table in MySQL
      |
      v  conn.commit()
data permanently saved
```

This is Extract (CSV), Transform (Python), Load (MySQL). That is ETL.
The job title "Data Engineer" means you build this pipeline.

---

### 3.2 The %s Rule -- Burn This In

```python
# NEVER DO THIS -- SQL injection vulnerability
order_id = 3001
cursor.execute(f"INSERT INTO orders VALUES ({order_id}, ...)")
#                                           ^^^^^^^^^^^^
#  If order_id came from user input and contained:
#  3001; DROP TABLE orders; --
#  Your f-string would execute that as SQL. Table destroyed.

# ALWAYS DO THIS -- parameterized query
cursor.execute("INSERT INTO orders (order_id) VALUES (%s)", (order_id,))
#  MySQL treats the value as DATA, not SQL code.
#  Malicious strings are escaped automatically.
```

%s is not optional. It is a hard security rule in every DE and backend role.

---

### 3.3 conn.commit() -- Why It Is Mandatory

MySQL uses transactions. INSERT holds data in a pending state.
commit() writes it to disk permanently.

```
Without commit():
  INSERT runs --> data pending --> conn.close() --> DATA IS LOST SILENTLY

With commit():
  INSERT runs --> data pending --> conn.commit() --> DATA SAVED
                                                --> conn.close() --> done
```

Forgetting commit() is one of the most common beginner DE bugs.
Pipeline runs with no errors. Table is empty. You don't know why.
Now you know why.

---

### 3.4 Credentials -- Never Hardcode

```python
# WRONG -- real password visible in file
def get_connection():
    return mysql.connector.connect(password="mypassword123")

# CORRECT -- credentials from environment variables
import os

def get_connection():
    """Returns a MySQL connection using environment variables."""
    return mysql.connector.connect(
        host     = os.environ.get("DB_HOST", "localhost"),
        user     = os.environ.get("DB_USER", "root"),
        password = os.environ.get("DB_PASSWORD"),
        database = os.environ.get("DB_NAME", "de_learning")
    )
```

Set in PowerShell before running:
```powershell
$env:DB_PASSWORD = "yourpassword"
python pipeline.py
```

Why this matters:
  Files get shared, committed to Git, sent in emails.
  Hardcoded passwords get exposed.
  Environment variables stay on your machine only.
This is a professional standard. No exceptions.

---

### 3.5 Complete ETL Script

```python
import csv
import os
import mysql.connector


def get_connection():
    """Returns a MySQL connection using environment variables."""
    return mysql.connector.connect(
        host     = os.environ.get("DB_HOST", "localhost"),
        user     = os.environ.get("DB_USER", "root"),
        password = os.environ.get("DB_PASSWORD"),
        database = os.environ.get("DB_NAME", "de_learning")
    )


def clean_record(record):
    """Cleans one CSV row. Returns a new typed dict. Never mutates original."""
    return {
        "order_id":    int(record["order_id"]),
        "amount":      max(float(record["amount"]), 0.0),
        "status":      record["status"].strip().upper(),
        "currency":    record["currency"].strip().upper(),
        "customer_id": int(record["customer_id"]),
    }


def is_valid(record):
    """Returns True if record has positive amount and correct status."""
    return record["amount"] > 0 and record["status"] in ("VALID", "COMPLETED")


def load_csv(filepath):
    """Reads a CSV file and returns a list of raw string dicts."""
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            records.append(dict(row))
    return records


def insert_orders(valid_orders):
    """Inserts validated orders into MySQL. Uses parameterized queries."""
    conn   = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO orders (order_id, amount, status, currency, customer_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    for order in valid_orders:
        values = (
            order["order_id"],
            order["amount"],
            order["status"],
            order["currency"],
            order["customer_id"],
        )
        cursor.execute(sql, values)

    conn.commit()
    print(f"Inserted {len(valid_orders)} rows into orders table.")

    cursor.close()
    conn.close()


# Run the pipeline
raw     = load_csv('raw_orders.csv')
cleaned = [clean_record(r) for r in raw]
valid   = [r for r in cleaned if is_valid(r)]
invalid = [r for r in cleaned if not is_valid(r)]

print(f"Loaded  : {len(raw)}")
print(f"Valid   : {len(valid)}")
print(f"Invalid : {len(invalid)}")

insert_orders(valid)
```
Output:
```
Loaded  : 10
Valid   : 5
Invalid : 5
Inserted 5 rows into orders table.
```

---

## 4. SQL: JOINs

### 4.1 The Analogy: Two Filing Cabinets

```
CUSTOMERS table             ORDERS table
───────────────             ──────────────
customer_id | name          order_id | customer_id | amount
101         | Akshay        3001     | 101         | 499.95
102         | Priya         3006     | 107         | 340.00
103         | Rahul         3008     | 109         | 1200.00
107         | Sneha
109         | Arjun

A JOIN combines rows from two tables using a shared column.
The shared column here is customer_id.
```

Without JOIN: two queries in Python, manually connect results.
With JOIN: one SQL query, MySQL connects them internally.

---

### 4.2 INNER JOIN -- Matching Rows Only

```
Diagram:

  customers          orders
  101 Akshay  <----> 3001 (customer_id=101)  INCLUDED
  102 Priya    X     (no orders)              EXCLUDED
  103 Rahul    X     (no orders)              EXCLUDED
  107 Sneha   <----> 3006 (customer_id=107)  INCLUDED
  109 Arjun   <----> 3008 (customer_id=109)  INCLUDED

INNER JOIN: only rows where customer_id exists in BOTH tables.
```

```sql
SELECT c.name, c.city, o.order_id, o.amount, o.status
FROM orders AS o
INNER JOIN customers AS c ON o.customer_id = c.customer_id;
```
Output:
```
name    | city      | order_id | amount  | status
Akshay  | Bangalore | 3001     | 499.95  | VALID
Sneha   | Bangalore | 3006     | 340.00  | VALID
Arjun   | Delhi     | 3008     | 1200.00 | COMPLETED
```

Use when: you only want rows that have a match in BOTH tables.

---

### 4.3 LEFT JOIN -- All Left Rows + Matches From Right

```
Diagram:

  customers          orders
  101 Akshay  <----> 3001 (match)             INCLUDED with data
  102 Priya   <----> NULL (no match)          INCLUDED with NULL
  103 Rahul   <----> NULL (no match)          INCLUDED with NULL
  107 Sneha   <----> 3006 (match)             INCLUDED with data
  109 Arjun   <----> 3008 (match)             INCLUDED with data

LEFT JOIN: ALL rows from the LEFT table.
Matching data from the right where available. NULL where not.
```

```sql
SELECT c.name, c.city, o.order_id, o.amount
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id;
```
Output:
```
name    | city      | order_id | amount
Akshay  | Bangalore | 3001     | 499.95
Priya   | Mumbai    | NULL     | NULL
Rahul   | Chennai   | NULL     | NULL
Sneha   | Bangalore | 3006     | 340.00
Arjun   | Delhi     | 3008     | 1200.00
```

Use when: you need ALL rows from the left table, including those with no match.

---

### 4.4 Find Customers Who Have Never Ordered

Classic DE pattern: LEFT JOIN + WHERE right side IS NULL

```sql
SELECT c.name, c.city
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```
Output:
```
name    | city
Priya   | Mumbai
Rahul   | Chennai
```

Logic:
  LEFT JOIN brings in ALL customers.
  Customers with no orders get NULL in order columns.
  WHERE o.order_id IS NULL filters to ONLY those with no orders.

---

### 4.5 Decision Rule

```
"Do I want rows with NO match to appear in the result?"

No  -> INNER JOIN (only matched rows)
Yes -> LEFT JOIN  (all left rows, NULLs where no match)

Common DE uses:
  "List all customers who placed orders"            -> INNER JOIN
  "List all customers, flag those with no orders"   -> LEFT JOIN
  "Find customers who have NEVER ordered"           -> LEFT JOIN + WHERE right IS NULL
```

---

### 4.6 Table Aliases

```sql
-- Without aliases (verbose):
SELECT customers.name, orders.amount
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;

-- With aliases (standard in production):
SELECT c.name, o.amount
FROM orders AS o
INNER JOIN customers AS c ON o.customer_id = c.customer_id;
```

Convention: short 1-2 letter alias matching the table name.
  customers -> c
  orders    -> o
  products  -> p

---

### 4.7 Today's Correct SQL Answers

```sql
-- Q1: INNER JOIN
SELECT c.name, o.order_id, o.amount
FROM orders AS o
INNER JOIN customers AS c ON c.customer_id = o.customer_id;

-- Q2: LEFT JOIN (all customers)
SELECT c.name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id;

-- Q3: Customers who have never ordered
SELECT c.name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

All 3 correct. First perfect SQL score.

---

## 5. DSA: Two Sum (LeetCode 1)

### 5.1 The Problem

Given a list of integers and a target, return the INDICES of the two
numbers that add up to the target. Each input has exactly one solution.

```python
two_sum([2, 7, 11, 15], 9)   # -> [0, 1]  (2 + 7 = 9)
two_sum([3, 2, 4], 6)         # -> [1, 2]  (2 + 4 = 6)
```

---

### 5.2 Brute Force: O(N squared) -- Never Use at Scale

```python
def two_sum_slow(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

Two nested loops. Every pair checked.
For N=5: N*(N-1)/2 = 10 comparisons (NOT N^2 = 25)

IMPORTANT: O(N^2) describes the GROWTH RATE, not the exact count.
  "If you double the input, work roughly quadruples."
  Exact formula for unique pairs: N*(N-1)/2

---

### 5.3 Hash Map: O(N) -- The Correct Solution

Insight: for every number n, the number needed is (target - n).
If we've already seen that complement, we have our answer.

```python
def two_sum(nums, target):
    """Returns indices of two numbers that sum to target. O(N) time."""
    seen = {}      # value -> index

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:           # O(1) lookup
            return [seen[complement], i]

        seen[num] = i                    # record: value -> index

    return []                            # no solution found -- always include this!


print(two_sum([2, 7, 11, 15], 9))   # [0, 1]
print(two_sum([3, 2, 4], 6))         # [1, 2]
print(two_sum([3, 3], 6))             # [0, 1]
```
Output:
```
[0, 1]
[1, 2]
[0, 1]
```

---

### 5.4 Manual Trace: two_sum([1, 5, 3, 7, 2], target=8)

```
seen = {}
i=0, num=1: complement=8-1=7.  7 in {}?      No.  seen={1:0}
i=1, num=5: complement=8-5=3.  3 in {1:0}?   No.  seen={1:0, 5:1}
i=2, num=3: complement=8-3=5.  5 in {1:0,5:1}? YES! return [seen[5], 2] = [1, 2]

Result: [1, 2]
Verify: nums[1] + nums[2] = 5 + 3 = 8 = target. Correct.
```

---

### 5.5 Set vs Dict -- When to Use Which

```
Contains Duplicate used a SET:
  seen = set()
  Only needed to know IF a value was present.
  No extra info needed.

Two Sum uses a DICT:
  seen = {}
  Needed to know IF a value was present AND its INDEX.
  Dict maps value -> index.

Rule:
  set  -> presence only (is X in the collection?)
  dict -> presence + extra data (where is X? what is X worth?)
```

---

## 6. JavaScript: Promises and async/await

Note: JS examples use web/browser/Node.js context only.

### 6.1 The Analogy: Ordering at a Restaurant

Synchronous: You stand at the kitchen counter, wait for your food, then sit.
             Nobody else can be served while you wait.

Asynchronous: You give your order. Get a number. Sit down.
              When food is ready, you're called.
              Other customers are served in the meantime.

In JavaScript, everything time-consuming is asynchronous:
  - Fetching from a server
  - Reading a file
  - Waiting for a timer
Promises and async/await are how you handle this cleanly.

---

### 6.2 The Problem: Callback Hell

```javascript
// Old way -- deeply nested callbacks
fetchUser(userId, function(user) {
    fetchPosts(user.id, function(posts) {
        fetchComments(posts[0].id, function(comments) {
            console.log(comments);
            // Even deeper with real code -- pyramid of doom
        });
    });
});
```

Impossible to read. Impossible to debug. Impossible to handle errors properly.

---

### 6.3 Promise -- The Three States

A Promise represents a future value. Always in one of three states:

```
PENDING    -> operation is still running
FULFILLED  -> operation succeeded, value is available
REJECTED   -> operation failed, error is available

Once fulfilled or rejected, a Promise NEVER changes state.
```

```javascript
function fetchUserData(userId) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (userId > 0) {
                resolve({ id: userId, name: "Akshay", role: "admin" });
            } else {
                reject(new Error("Invalid user ID"));
            }
        }, 1000);
    });
}

fetchUserData(101)
    .then(user  => console.log("Got user:", user.name))   // fulfilled
    .catch(err  => console.log("Error:", err.message));   // rejected
```
Output (after 1 second):
```
Got user: Akshay
```

---

### 6.4 async/await -- Promises Made Readable

async/await is syntactic sugar over Promises.
Same behaviour. Cleaner syntax.
Makes async code look and read like synchronous code.

```javascript
// BEFORE (Promise chain):
fetchUserData(101).then(user => console.log(user.name)).catch(err => ...);

// AFTER (async/await -- same thing):
async function showUser(userId) {
    try {
        const user = await fetchUserData(userId);   // wait here until resolved
        console.log("Got user:", user.name);
        console.log("Role:", user.role);
    } catch (error) {
        console.log("Error:", error.message);
    }
}

showUser(101);   // Got user: Akshay / Role: admin
showUser(-1);    // Error: Invalid user ID
```

await pauses execution INSIDE the async function only.
The rest of the program keeps running. It is not a full block.

---

### 6.5 The Three Rules

```
RULE 1: await can ONLY be used inside an async function.
  async function doThis() {
      const x = await somePromise();  // valid
  }
  const x = await somePromise();      // SyntaxError -- not inside async

RULE 2: async functions ALWAYS return a Promise.
  async function greet() { return "hello"; }
  greet()        // returns Promise<"hello">
  await greet()  // returns "hello"

RULE 3: Always use try/catch with async/await.
  Without it, rejected Promises are UNHANDLED.
  Node.js 15+: crashes the process (exit code 1).
  Browser: console error, may silently skip code.
  "Silent failure" is NOT what happens -- unhandled = loud crash.
```

---

### 6.6 Today's Checkpoint Trace

```javascript
async function getData(id) {
    return new Promise((resolve, reject) => {
        if (id > 0) resolve({ id: id, value: id * 10 });
        else reject(new Error("Bad ID"));
    });
}

async function main() {
    try {
        const result = await getData(5);
        console.log(result.value);          // 50 (5 * 10)

        const result2 = await getData(-1);  // rejects -> throws
        console.log(result2.value);         // NEVER RUNS

    } catch (error) {
        console.log("Caught:", error.message);  // "Caught: Bad ID"
    }
}
main();
```
Output:
```
50
Caught: Bad ID
```

Q4 CORRECTION: Without try/catch, getData(-1) causes an UNHANDLED rejection.
  Node.js 15+: process crashes with exit code 1. LOUD, not silent.
  "Silent failure" means error is swallowed (.catch(err => {}) with nothing inside).
  Unhandled rejection = the opposite of silent.

---

## 7. Day 6 Code Review -- Issues to Remember

### CRITICAL (appears every session -- must stop)
1. No docstrings. Every function needs one line.
2. Hardcoded credentials. Always use os.environ.get().

### NAMING VIOLATIONS
3. sqlConnector -> get_connection (snake_case for Python functions, always)
4. csv_reader -> run_etl or process_and_load (name should reflect ALL it does)

### LOGIC ISSUES
5. Brute force comparisons: N*(N-1)/2 not N^2.
   O(N^2) = growth pattern. Not the exact operation count.
6. two_sum() must always end with return [] for the no-solution case.

### SQL (First perfect score)
7. All 3 JOIN queries correct. Aliases, uppercase keywords, IS NULL. ✅

---

## 8. FAANG Interview Question Vault

Q: What is SQL injection and how do parameterized queries prevent it?
A: SQL injection is when malicious input is treated as SQL code instead of data.
   Example: user input "'; DROP TABLE orders; --" inside an f-string SQL statement
   would execute and destroy the table.
   Parameterized queries send the value separately from the SQL string.
   MySQL escapes the value automatically, treating it as pure data.
   This is why %s placeholders are mandatory -- never f-strings in SQL.

Q: What is the difference between INNER JOIN and LEFT JOIN?
A: INNER JOIN returns only rows where the join condition matches in BOTH tables.
   Rows with no match on either side are excluded.
   LEFT JOIN returns ALL rows from the left table.
   For rows with no match in the right table, right-side columns appear as NULL.
   Use LEFT JOIN when you need the complete left table with optional right data.

Q: What does conn.commit() do and what happens if you forget it?
A: MySQL uses transactions. INSERT/UPDATE/DELETE operations are held in a pending
   state until committed. commit() writes them to disk permanently.
   If you forget it, the connection closes, the pending transaction is rolled back,
   and all your inserts are lost -- with no error message. The table looks empty.

Q: Two Sum -- what is the O(N) approach and why is it better than O(N^2)?
A: The O(N) approach uses a hash map. For each number n, we check if (target - n)
   has already been seen. Hash map lookup is O(1), so one pass = O(N) total.
   The O(N^2) brute force checks every pair -- N*(N-1)/2 comparisons.
   At 10 million records: ~50 trillion operations (brute) vs 10 million (hash map).
   The hash map approach is the only viable one at DE scale.

Q: What is the difference between a Promise and async/await in JavaScript?
A: They are the same mechanism. async/await is syntactic sugar over Promises.
   await pauses execution inside an async function until the Promise settles.
   Both handle asynchronous operations -- async/await just reads more like
   synchronous code, making it easier to reason about and debug.

---

## 9. Debugging Challenges for Day 7

Bug 1: What is wrong with this Python code?
```python
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="secret",
        database="de_learning"
    )

def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    results = cursor.fetchall()
    return results

orders = get_all_orders()
print(orders)
```

Bug 2: What does this SQL return? Is it what was intended?
```sql
SELECT c.name, o.amount
FROM customers AS c
INNER JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.amount > 500
   OR c.city = 'Delhi';
```

Bug 3: What is wrong with this JS? What does it print?
```javascript
async function fetchData() {
    return 42;
}

const result = fetchData();
console.log(result);
console.log(result + 1);
```

---

## 10. Spaced Repetition Checklist

Review on Day 7, Day 13, and Day 37.

- [ ] What does csv.DictReader give you per row? What type?
- [ ] Why does clean_record() need to call int() and float() on CSV values?
- [ ] What is SQL injection? Write the wrong way and the right way in one line each.
- [ ] Why does MySQL need conn.commit() after INSERT?
- [ ] What is the difference between INNER JOIN and LEFT JOIN?
- [ ] How do you find all customers who have NEVER placed an order? Write the query.
- [ ] Two Sum: write the O(N) solution from memory (no looking).
- [ ] JS: Can you use await outside an async function?
- [ ] JS: What are the three states of a Promise?
- [ ] JS: What happens to an unhandled Promise rejection in Node.js 15+?

---

Day 06 complete - 2026-10-07
Score: 83% (33/40)
Running Average: ~82%
Next: Day 07 - GROUP BY, aggregates, HAVING, Week 2 DSA + JS