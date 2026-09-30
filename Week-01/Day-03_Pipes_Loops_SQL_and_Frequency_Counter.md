# Day 03 - Linux Pipes | Python Loops | SQL Foundations | Frequency Counter | JS Scope

**Date**: 2026-09-28
**Week**: Week 1 - Absolute Foundations
**Mentor Score**: 84% (42/50)
**Tracks**: Linux streams & pipes | Python for loops | SQL primary keys & basic queries | Frequency counter | JS block scope

---

## 1. Executive Summary

```
PRODUCTION DE WORKFLOW - WHERE TODAY FITS:

[1. Linux: inspect incoming file]
   grep "ERROR" pipeline.log | wc -l

[2. Python: loop over records, validate each row]
   for record in records:
       if record["status"] == "VALID": ...

[3. SQL: query what was loaded to the database]
   SELECT name, city
   FROM customers
   WHERE is_active = TRUE AND city = 'Bangalore';

[4. DSA: count log levels, statuses, IDs in pipelines]
   frequency[status] = frequency.get(status, 0) + 1
```

---

## 2. Linux: Standard Streams, Pipes & Redirects

### 2.1 What Are Standard Streams?

```
+----------------------------------------------+
|            EVERY LINUX PROGRAM               |
|                                              |
|  stdin  (Standard Input)  = Channel 0        |
|    -> WHERE it reads data FROM (keyboard)    |
|                                              |
|  stdout (Standard Output) = Channel 1        |
|    -> WHERE it sends normal output (screen)  |
|                                              |
|  stderr (Standard Error)  = Channel 2        |
|    -> WHERE it sends errors (screen)         |
+----------------------------------------------+
```

Why it matters: You can redirect each channel independently.
Normal output to one file, errors to another.
In production: python pipeline.py >> run.log 2>> errors.log

---

### 2.2 > Operator (Redirect - Overwrite)

> takes stdout of a command and writes it to a file instead of the screen.

```bash
grep "ERROR" pipeline.log > errors_only.txt
```
Output on screen: nothing (output went to file)

```bash
cat errors_only.txt
```
Output:
```
[01:59:02] ERROR: Failed to acquire DB connection.
[02:15:10] ERROR: Disk space warning on /var/log.
```

WARNING: > OVERWRITES the file completely every time.
Use >> to keep old content.

---

### 2.3 >> Operator (Append)

```
>  : Overwrites (blank page, then write)
>> : Appends   (keep existing, write at end)
```

Real DE Scenario - Hourly pipeline accumulating daily errors:
```bash
grep "ERROR" morning_run.log  > daily_errors.txt    # 6 AM: creates/overwrites
grep "ERROR" midmorning_run.log >> daily_errors.txt  # 7 AM: adds to file
grep "ERROR" afternoon_run.log  >> daily_errors.txt  # 8 AM: keeps adding
```

Production pattern for Python pipelines:
```bash
python pipeline.py >> run.log 2>> errors.log
```

---

### 2.4 | Pipe (Chain Commands)

Output of left command becomes input of right command.
Like an assembly line - each tool does ONE job.

Example 1 - Count errors in a 50 GB file:
```bash
grep "ERROR" pipeline.log | wc -l
```
Output: 47

Internal flow:
```
pipeline.log -> [grep "ERROR"] -> matching lines -> [wc -l] -> 47
```

Example 2 - Preview first 5 errors:
```bash
grep "ERROR" pipeline.log | head -n 5
```

Example 3 - Filter by two patterns (chained greps):
```bash
grep "CRITICAL" api.log | grep "2026-09-28"
```
Finds lines containing BOTH "CRITICAL" AND today's date.

---

### 2.5 Case Sensitivity in grep - A Real Bug

```bash
# WRONG - only matches "Error", misses "ERROR" and "error"
grep "Error" pipeline.log

# CORRECT (exact case)
grep "ERROR" pipeline.log

# CORRECT (case-insensitive flag)
grep -i "error" pipeline.log    # Matches ERROR, Error, error
```

In production logs, always check what casing the system uses.
Missing errors because of wrong case is a real on-call trap.

---

### 2.6 Unifying Picture

```
         YOUR KEYBOARD
              |
           [stdin]
              |
              v
+-----------------------------+
|       Linux Program         |
+-----------------------------+
        |           |
    [stdout]     [stderr]
        |           |
        |           +-> terminal (errors)
        |
   +----+-------+----------+
   |            |          |
[screen]     [> file]   [| next command]
(default)   (redirect)    (pipe)
```

---

### 2.7 Level-Up Path

```
Level 1 (YOU ARE HERE):
  >    redirect to file (overwrite)
  >>   append to file
  |    pipe output of one command to next

Level 2 (Week 2):
  2>   redirect ONLY stderr
  &>   redirect BOTH stdout + stderr
  python pipeline.py >> run.log 2>> errors.log

Level 3 (Production DE):
  tee    -> save to file AND show on screen
  zcat   -> pipe compressed .gz files
  xargs  -> convert stdin into command arguments
```

---

## 3. Python: for Loops & Iteration

### 3.1 The Analogy

A postal worker with 1,000 letters:
1. Pick up first letter
2. Read address, deliver it
3. Pick up next letter
4. Repeat until bag is empty

A for loop is Python's postal worker.

---

### 3.2 Basic for Loop

```python
# JavaScript (C-style)
for (let i = 0; i < 5; i++) { console.log(i); }

# Python - no index management needed
names = ["Alice", "Bob", "Charlie"]
for name in names:
    print(name)
```
Output: Alice / Bob / Charlie

No let, no i++, no len(). Python handles all of it internally.

---

### 3.3 range() - Generating Number Sequences

```
range(5)        -> 0, 1, 2, 3, 4
range(2, 7)     -> 2, 3, 4, 5, 6
range(0, 10, 2) -> 0, 2, 4, 6, 8
```

```python
for i in range(5):
    print(f"Processing batch {i}")
```
Output: Processing batch 0 / 1 / 2 / 3 / 4

Real DE Pattern - Retry logic:
```python
MAX_RETRIES = 3
for attempt in range(1, MAX_RETRIES + 1):
    print(f"Attempt {attempt} of {MAX_RETRIES}: Connecting to database...")
print("All retries exhausted. Sending alert.")
```

---

### 3.4 enumerate() - Index AND Item Together

```python
# JavaScript habit - DO NOT use this in Python
for i in range(len(files)):
    print(i, files[i])

# Python way
files = ["orders.csv", "customers.csv", "products.csv"]
for index, file in enumerate(files):
    print(f"[{index}] Processing: {file}")
```
Output:
```
[0] Processing: orders.csv
[1] Processing: customers.csv
[2] Processing: products.csv
```

enumerate() returns a tuple (index, item) on each iteration.

---

### 3.5 Looping Over a Dictionary

```python
order = {"order_id": 1001, "amount": 499.95, "status": "COMPLETED"}

# Pattern 1: Keys only
for key in order:
    print(key)

# Pattern 2: Values only
for value in order.values():
    print(value)

# Pattern 3: Both key AND value (most common in DE)
for key, value in order.items():
    print(f"  {key:<15}: {value}")
```
Output (Pattern 3):
```
  order_id       : 1001
  amount         : 499.95
  status         : COMPLETED
```

:<15 left-aligns the key in a 15-character wide field.

---

### 3.6 Looping Over a List of Dicts - The Real DE Pattern

In real pipelines, data is always a list of dicts (each dict = one record/row).

```python
records = [
    {"order_id": 1001, "amount": 499.95, "status": "COMPLETED"},
    {"order_id": 1002, "amount": -50.00, "status": "INVALID"},
    {"order_id": 1003, "amount": 820.00, "status": "COMPLETED"},
]

valid_records   = []
invalid_records = []

for record in records:
    if record["status"] == "COMPLETED" and record["amount"] > 0:
        valid_records.append(record)
    else:
        invalid_records.append(record)

print(f"Valid: {len(valid_records)} | Invalid: {len(invalid_records)}")
```

---

### 3.7 break and continue

```python
# continue - skip current item, go to next
for order_id in [1001, 1002, None, 1004]:
    if order_id is None:
        continue          # Skip null. No else needed after continue.
    print(f"Processing order: {order_id}")
```

```python
# break - stop the entire loop immediately
for record in records:
    if record["status"] == "CRITICAL_FAILURE":
        print("CRITICAL detected - halting!")
        break
```

After continue, there is NO need for an else block.
continue already skips the rest of the loop body for that iteration.

---

### 3.8 Naming Convention Reminder

```
Classes     -> CamelCase:   class DataPipeline
Variables   -> snake_case:  total_count, error_message
Functions   -> snake_case:  def run_pipeline()
Constants   -> UPPER_SNAKE: MAX_RETRIES = 3

if run['rows'] == 0:    <- Python (no parentheses)
if(run['rows'] == 0):   <- JavaScript habit (drop this)
```

---

### 3.9 JS to Python Loop Translation

| JavaScript                           | Python                           |
|:-------------------------------------|:---------------------------------|
| for (let i=0; i<5; i++)              | for i in range(5):               |
| for (const item of arr)              | for item in list:                |
| arr.forEach((item, i) => ...)        | for i, item in enumerate(list):  |
| Object.entries(obj).forEach([k,v])   | for k, v in dict.items():        |
| break                                | break                            |
| continue                             | continue                         |

---

## 4. SQL: Database Tables, Primary Keys & Basic Queries

### 4.1 Table vs Spreadsheet

```
Google Sheets (no rules):          Database Table (rules enforced by engine):

Name    | Age | Email             customer_id | name    | age | email
--------|-----|------             ------------|---------|-----|------
Akshay  | 28  | ak@gmail.com      1001        | Akshay  | 28  | ak@gmail.com
Akshay  | 28  | ak@gmail.com  DUP BLOCKED! Duplicate primary key
Bob     |     | not_email     BAD BLOCKED! NULL not allowed
```

---

### 4.2 Core Vocabulary

```
TABLE   = The container (like a spreadsheet tab)
   |
   +-- COLUMN = One characteristic (customer_id, name, email, city)
   |
   +-- ROW = One complete entity (1001, "Akshay", "ak@gmail.com", "Bangalore")
   |
   +-- PRIMARY KEY = Unique identifier for every row
   |      NEVER NULL, NEVER DUPLICATE, NEVER CHANGES
   |
   +-- DATA TYPE = What kind of data the column holds
          INT, VARCHAR(255), DATE, DECIMAL(10,2), BOOLEAN
```

---

### 4.3 Primary Key

Analogy: Your Aadhaar Number.
Two people can be named "Akshay Kumar" but have different Aadhaar numbers.
The Aadhaar number uniquely identifies exactly one person in all of India.

```
customers:
customer_id | name          | email              | city
(PRIMARY KEY)
1001        | Akshay Kumar  | ak@gmail.com       | Bangalore
1002        | Priya Patel   | priya@yahoo.com    | Mumbai
1004        | Akshay Kumar  | ak2@gmail.com      | Delhi
             ^
             Two people named "Akshay Kumar" but different customer_id -> distinguishable
```

Rules:
1. UNIQUE - no two rows share the same value
2. NOT NULL - can never be empty
3. IMMUTABLE - should not change after creation

---

### 4.4 Foreign Keys & Table Relationships

```
CUSTOMERS TABLE                    ORDERS TABLE
customer_id | name                 order_id | customer_id | amount
------------|-----                 ---------|-------------|-------
1001        | Akshay               3001     | 1001        | 499.95
1002        | Priya                3002     | 1001        | 129.00
                                   3003     | 1002        | 899.00
                                                ^
                                                FOREIGN KEY
                                     (references customer_id in customers)
```

Rule: Cannot insert order with customer_id = 9999 if customer 9999 does not exist.
The database rejects it. Prevents orphaned records.
One customer -> Many orders = ONE-TO-MANY relationship.

---

### 4.5 SQL Column Data Types

| SQL Type      | What it stores             | Python equiv | DE Example         |
|:--------------|:---------------------------|:-------------|:-------------------|
| INT           | Whole numbers              | int          | IDs, counts        |
| BIGINT        | Very large whole numbers   | int          | Transaction IDs    |
| DECIMAL(10,2) | Exact decimal              | Decimal      | Prices, taxes      |
| VARCHAR(255)  | Text up to 255 chars       | str          | Names, emails      |
| TEXT          | Unlimited text             | str          | Logs, JSON         |
| DATE          | Date only                  | datetime.date| Order dates        |
| TIMESTAMP     | Date + time                | datetime     | Audit trails       |
| BOOLEAN       | True/False                 | bool         | is_active          |

---

### 4.6 SQL Queries: SELECT, FROM, WHERE

Sample table:
```
customers:
customer_id | name           | city       | age | is_active | signup_date
1001        | Akshay Kumar   | Bangalore  | 28  | TRUE      | 2024-01-15
1002        | Priya Patel    | Mumbai     | 32  | TRUE      | 2024-02-20
1003        | Rahul Sharma   | Chennai    | 25  | FALSE     | 2024-01-30
1004        | Sneha Reddy    | Bangalore  | 29  | TRUE      | 2024-03-10
1005        | Arjun Nair     | Delhi      | 35  | FALSE     | 2024-01-05
```

SELECT all columns (exploration only - never in production code):
```sql
SELECT *
FROM customers;
```

SELECT specific columns:
```sql
SELECT name, city, age
FROM customers;
```

WHERE - filter rows:
```sql
SELECT name, city, age
FROM customers
WHERE is_active = TRUE;
```
Output: Akshay (28), Priya (32), Sneha (29)

WHERE with AND:
```sql
SELECT name, city, age
FROM customers
WHERE is_active = TRUE
  AND city = 'Bangalore';
```
Output: Akshay (28), Sneha (29)

WHERE with OR:
```sql
SELECT name, city, age
FROM customers
WHERE city = 'Bangalore'
   OR city = 'Mumbai';
```
Output: Akshay (28), Priya (32), Sneha (29)

---

### 4.7 THE 3 SQL RULES - NEVER FORGET

```
RULE 1: String literals ALWAYS use SINGLE quotes
  CORRECT:  WHERE city = 'Bangalore'
  WRONG:    WHERE city = "Bangalore"
            (double quotes = identifier, not a string value)

RULE 2: Every OR condition needs a FULL column comparison
  CORRECT:  WHERE city = 'Chennai' OR city = 'Delhi'
  WRONG:    WHERE city = 'Chennai' OR 'Delhi'
            (SQL does not know what 'Delhi' alone means)

RULE 3: AND binds BEFORE OR - use parentheses when mixing
  CORRECT:  WHERE (city = 'Chennai' OR city = 'Delhi') AND age > 30
  WRONG:    WHERE city = 'Chennai' OR city = 'Delhi' AND age > 30
            (SQL reads this as: Chennai OR (Delhi AND age > 30))
            (Completely different results!)
```

AND/OR precedence is identical to Python:
  Python: and before or
  SQL:    AND before OR
  Fix: USE PARENTHESES when mixing them.

---

### 4.8 Today's Correct SQL Answers

Q1 - Signed up after 2024-02-01:
```sql
SELECT name, signup_date
FROM customers
WHERE signup_date > '2024-02-01';
```
Result: Priya Patel (2024-02-20), Sneha Reddy (2024-03-10)

Q2 - Inactive customers:
```sql
SELECT *
FROM customers
WHERE is_active = FALSE;
```
Result: Rahul Sharma (1003), Arjun Nair (1005)

Q3 - Chennai or Delhi, AND age > 30:
```sql
SELECT name, age
FROM customers
WHERE (city = 'Chennai' OR city = 'Delhi')
  AND age > 30;
```
Result: Arjun Nair (Delhi, 35) ONLY.
Rahul Sharma (Chennai, 25) does NOT match because 25 > 30 is false.

---

## 5. DSA: Frequency Counter Pattern

### 5.1 The Problem

Count how many times each unique item appears in a collection.
Real DE use: "How many COMPLETED, PENDING, FAILED orders today?"

### 5.2 The Mental Model: Tally Marks

```
Whiteboard:
  COMPLETED  |||
  PENDING    ||
  FAILED     |

New "COMPLETED" arrives:
  Is it on the board? YES -> add 1 tally
  Is it on the board? NO  -> write it with count = 1
```

### 5.3 Three Levels of Implementation

Level 1 - if/else (write this in interviews):
```python
frequency = {}
for status in statuses:
    if status in frequency:
        frequency[status] += 1
    else:
        frequency[status] = 1
```

Level 2 - .get() one-liner (Pythonic):
```python
frequency = {}
for status in statuses:
    frequency[status] = frequency.get(status, 0) + 1
```
frequency.get(status, 0) returns current count or 0 if key missing. Then +1.

Level 3 - Counter (production):
```python
from collections import Counter
frequency = Counter(statuses)
print(frequency.most_common(2))    # Top 2 most frequent
```

### 5.4 Understanding sorted() with lambda

```python
sorted_fq = dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))
```

Breaking it down:
```
frequency.items()
  -> [("INFO", 5), ("ERROR", 3), ("WARN", 2)]

key=lambda x: x[1]
  -> For each tuple x, use x[1] (the count) to determine sort order
  -> lambda x: x[1]  is identical to:
     def get_count(x):
         return x[1]

reverse=True
  -> Highest count first

dict(...)
  -> Convert sorted list of tuples back to a dict
```

### 5.5 Today's Log Level Counter Solution

```python
frequency = {}
for log_line in log_lines:
    level = log_line.split()[2]    # split()[2] = log level field
    frequency[level] = frequency.get(level, 0) + 1

sorted_fq = dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))

for level, count in sorted_fq.items():
    print(f"{level:<12}: {count}")
```
Output:
```
INFO        : 5
ERROR       : 3
WARN        : 2
```

---

## 6. JavaScript: Block Scope & Scope Chain

### 6.1 The Analogy: Filing Cabinets Inside Filing Cabinets

```
BUILDING (Global scope)
  |
  +-- ROOM A (Function scope)
  |     |
  |     +-- DRAWER 1 (Block scope: if/for/while)
  |
  +-- ROOM B (Another function)

THE RULE:
  From inside a drawer, you can see INTO the drawer AND OUT to the room.
  From outside the room, you CANNOT look into the drawer.
  Scope chain: inner sees outer. Outer CANNOT see inner.
```

### 6.2 var vs let/const

```javascript
// var is FUNCTION-scoped - leaks out of blocks!
function example() {
    if (true) {
        var x = 10;
    }
    console.log(x);     // 10 - var LEAKS out of if block!
}

// let/const are BLOCK-scoped - stay inside {}
function example2() {
    if (true) {
        let y = 20;
    }
    console.log(y);     // ReferenceError: y is not defined
}
```

Always use let or const. Never use var in modern JavaScript.

### 6.3 The Scope Chain

```javascript
const company = "DataCorp";          // Global

function runPipeline() {
    const pipeline = "orders";       // Function scope

    function logStatus() {
        const status = "SUCCESS";    // Inner scope

        console.log(status);    // Own scope -> "SUCCESS"
        console.log(pipeline);  // Not here, look out -> "orders"
        console.log(company);   // Not here, look out -> "DataCorp"
    }
    logStatus();
}
```
Output: SUCCESS / orders / DataCorp
Chain direction: inner -> outer. Never the reverse.

### 6.4 Variable Shadowing

When inner scope declares same-named variable as outer scope,
the inner one SHADOWS (hides) the outer one.

```javascript
const status = "GLOBAL_STATUS";

function checkPipeline() {
    const status = "PIPELINE_STATUS";   // Shadows global

    function logResult() {
        const status = "RESULT_STATUS"; // Shadows pipeline
        console.log(status);            // "RESULT_STATUS"
    }

    logResult();
    console.log(status);                // "PIPELINE_STATUS"
}

checkPipeline();
console.log(status);                    // "GLOBAL_STATUS"
```
Output: RESULT_STATUS / PIPELINE_STATUS / GLOBAL_STATUS

VOCABULARY: This is called VARIABLE SHADOWING.
Interviewers ask "what is variable shadowing?" directly. Know the term.

---

## 7. Day 3 Code Review Summary

| Checkpoint       | Score | Key Issue                                              |
|:-----------------|:------|:-------------------------------------------------------|
| Linux Pipes      | 9/10  | grep "Error" misses "ERROR". Use grep -i or exact case |
| Python Loops     | 9/10  | Drop JS parentheses in if. No else after continue.     |
| SQL Queries      | 6/10  | Double quotes. Repeated column in OR. AND/OR precedence|
| Frequency Counter| 8/10  | Logic correct. Owned the lambda after explanation.     |
| JS Scope         | 9/10  | Correct. Add "variable shadowing" to vocabulary.       |
| **Total**        | **42/50 (84%)** |                                               |

---

## 8. FAANG Interview Question Vault

Junior:
Q: What is a Primary Key? What rules must it follow?
A: Unique identifier for every row. Must be UNIQUE, NOT NULL, IMMUTABLE.
   Example: customer_id = 1001 where no two customers share the same ID.

Q: What is the difference between > and >> in Linux?
A: > redirects output to a file and OVERWRITES it completely each time.
   >> APPENDS to the file without removing existing content.
   In production I use >> to accumulate daily logs across multiple pipeline runs.

Q: What is enumerate() and why is it preferred over range(len(list))?
A: enumerate() gives both index and item as a tuple on each iteration.
   range(len(list)) is a JavaScript habit of manually managing the index.
   enumerate() is more readable, less error-prone, and is the Pythonic standard.

Mid:
Q: Explain AND/OR operator precedence in SQL. Give an example of wrong results.
A: AND has higher precedence than OR - binds before OR.
   WHERE city = 'Chennai' OR city = 'Delhi' AND age > 30
   means Chennai OR (Delhi AND age > 30).
   Fix: WHERE (city = 'Chennai' OR city = 'Delhi') AND age > 30.

Q: Build a frequency counter in Python. Write three versions.
A: if/else version, .get(key, 0) + 1 version, Counter() version. (See Section 5.3)

Senior:
Q: What is the difference between a Primary Key and a Foreign Key?
A: Primary key uniquely identifies each row in its own table (no dups, not null).
   Foreign key references the primary key of another table.
   It enforces referential integrity: you cannot insert a FK value that does not
   exist in the referenced table, and cannot delete a referenced row.
   Together they prevent orphaned records and maintain consistent relationships.

---

## 9. Debugging Challenges for Day 4

Bug 1: What is wrong and what result does it produce?
```sql
SELECT name, age
FROM customers
WHERE city = "Delhi" OR age > 30 AND is_active = FALSE;
```

Bug 2: What does this print and why?
```python
results = []
for i in range(5):
    if i == 3:
        break
    results.append(i * 2)
print(results)
```

Bug 3: Predict exact output and explain each line:
```python
count = 0
for i in range(5):
    count = count + i
print(f"Total: {count}")
count = 0
print(f"Reset: {count}")
```

---

## 10. Spaced Repetition Checklist

Review on Day 4, Day 10, and Day 31. Cover answer. Say it out loud.

- [ ] What is the difference between > and >> in Linux?
- [ ] What does | (pipe) do? Give one real DE example with exact syntax.
- [ ] What does grep -i do vs grep? When would you use each?
- [ ] Python: What is enumerate()? When do you use it instead of range(len())?
- [ ] Python: What is the difference between break and continue?
- [ ] SQL Rule 1: What type of quotes do SQL string literals use?
- [ ] SQL Rule 2: How do you correctly write an OR condition for the same column?
- [ ] SQL Rule 3: What is AND/OR operator precedence? How do you prevent mistakes?
- [ ] DSA: Write the frequency counter in .get() style from memory in 30 seconds.
- [ ] JS: What is variable shadowing? Give a one-sentence definition.

---

Day 03 complete - 2026-09-28
Score: 84% (42/50)
Next: Day 04 - Python Functions | SQL IN/BETWEEN/LIKE/NULL | JS Closures | Contains Duplicate (LC 217)