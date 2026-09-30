# Day 04 - Python Functions | SQL IN/BETWEEN/LIKE/NULL | Contains Duplicate | JS Closures

**Date**: 2026-09-29
**Week**: Week 1 - Absolute Foundations
**Mentor Score**: 73% (29/40) revised to 73% + Practice 87% (26/30)
**Running Average**: ~81%
**Tracks**: Python functions & scope | SQL advanced filtering | DSA Contains Duplicate (LC 217) | JS Closures

---

## 1. Executive Summary

```
WHAT TODAY'S SKILLS UNLOCK:

Python Functions:
  Every pipeline is a set of functions that call each other.
  load() -> clean() -> validate() -> load_to_db()

SQL Filtering:
  IN, BETWEEN, LIKE, IS NULL are the tools that
  answer real business questions from a database.

Contains Duplicate:
  O(N) duplicate detection using a set.
  Used in primary key validation before loading data.

JS Closures:
  Private state in JavaScript without classes.
  The pattern behind counters, factories, and module patterns.
```

---

## 2. Python: Functions

### 2.1 The Analogy: A Vending Machine

```
YOU                    VENDING MACHINE               YOU GET BACK
──────                 ──────────────────            ────────────
Press B3      ──────>  [Takes your input]   ──────>  A Pepsi can
Give ₹20              [Does internal work]
                       [Returns a product]

function_call(input) -> [does the work] -> returns output
```

Three things happen every time:
1. You give it INPUT (arguments/parameters)
2. It does work internally (the function body)
3. It gives you back OUTPUT (the return value)

A function is a REUSABLE block of logic with a name.
Define it once. Call it thousands of times.

---

### 2.2 Python vs JavaScript Syntax

```javascript
// JavaScript
function validateRecord(record) {
    if (record.amount > 0 && record.status === "VALID") {
        return true;
    }
    return false;
}
```

```python
# Python — same concept, different syntax
def validate_record(record):
    if record["amount"] > 0 and record["status"] == "VALID":
        return True
    return False
```

Key differences:
- function keyword  ->  def in Python
- No {} braces — indentation defines the body
- No const/let needed for function definition
- === becomes == in Python

---

### 2.3 The 4 Parts of Every Python Function

```python
def function_name(parameter_1, parameter_2):  # DEFINITION + PARAMETERS
    result = parameter_1 + parameter_2         # BODY (the work)
    return result                              # RETURN VALUE

output = function_name(10, 20)                # CALLING the function
print(output)                                 # 30
```

```
def           -> keyword: "I am defining a function"
function_name -> the name you choose (snake_case always)
parameters    -> inputs the function receives (0, 1, or many)
body          -> indented code that runs when called
return        -> what the function sends back to the caller
```

---

### 2.4 Functions With No Return Value

Some functions DO things but return nothing:

```python
def print_pipeline_header(pipeline_name, run_date):
    print("=" * 45)
    print(f"  PIPELINE: {pipeline_name}")
    print(f"  DATE    : {run_date}")
    print("=" * 45)

print_pipeline_header("orders_ingestion", "2026-09-29")
```
Output:
```
=============================================
  PIPELINE: orders_ingestion
  DATE    : 2026-09-29
=============================================
```

This function does work (printing) but returns None implicitly.
Printing, logging, and writing to files are all valid function purposes.

---

### 2.5 Default Parameters

```python
def calculate_tax(amount, tax_rate=0.18):   # 0.18 is the DEFAULT
    tax = amount * tax_rate
    return round(tax, 2)

tax1 = calculate_tax(1000)          # Uses default 18%  -> 180.0
tax2 = calculate_tax(1000, 0.05)    # Uses custom 5%    -> 50.0

print(f"Tax on 1000 at 18%: {tax1}")
print(f"Tax on 1000 at  5%: {tax2}")
```
Output:
```
Tax on 1000 at 18%: 180.0
Tax on 1000 at  5%: 50.0
```

Default parameters go LAST in the parameter list.
Parameters without defaults go FIRST.

---

### 2.6 Returning Multiple Values (Tuple)

```python
def validate_batch(records):
    valid   = []
    invalid = []

    for record in records:
        if record["amount"] > 0 and record["status"] == "VALID":
            valid.append(record)
        else:
            invalid.append(record)

    return valid, invalid    # Returns a TUPLE of two lists

records = [
    {"id": 1, "amount": 500.0, "status": "VALID"},
    {"id": 2, "amount": -10.0, "status": "INVALID"},
    {"id": 3, "amount": 250.0, "status": "VALID"},
]

valid_records, invalid_records = validate_batch(records)
print(f"Valid  : {len(valid_records)}")     # 2
print(f"Invalid: {len(invalid_records)}")   # 1
```

Functions returning multiple values always return them as a tuple.
Unpack them immediately with multiple variables on the left side.

---

### 2.7 Function Scope - Variables Live and Die Inside Functions

```
GLOBAL scope (outside all functions):
  pipeline_name = "orders"       <- visible everywhere

  +-----------------------------+
  |  run_pipeline() function    |
  |  batch_size = 256           | <- LOCAL: dies when function ends
  |  can READ pipeline_name     | <- global is readable from inside
  +-----------------------------+
  ^
  Outside CANNOT see inside.
  batch_size is gone after function ends.
```

```python
pipeline_name = "orders"        # GLOBAL variable

def run_pipeline():
    batch_size = 256             # LOCAL variable - only inside this function
    print(f"Running: {pipeline_name}")   # Can READ global
    print(f"Batch: {batch_size}")

run_pipeline()

print(pipeline_name)   # Works - global
print(batch_size)      # NameError: batch_size is not defined
```
Output:
```
Running: orders
Batch: 256
orders
NameError: name 'batch_size' is not defined
```

THE RULE:
Functions can READ global variables.
Functions should NOT modify global variables.
Pass everything as PARAMETERS. Return results.
This makes functions safe, testable, and reusable.

---

### 2.8 Naming Convention + f-string Rule

```
Classes     -> CamelCase:    class DataPipeline
Variables   -> snake_case:   total_count, error_message
Functions   -> snake_case:   def run_pipeline()
Constants   -> UPPER_SNAKE:  MAX_RETRIES = 3

Never shadow Python built-ins:
  id, type, list, dict, set, input, print, range, len, sum, max, min
  Use: num, val, record, customer_id, item -- not 'id'

Variable naming communicates intent:
  sets    -> just says "it's a set"
  seen    -> says "it tracks what we've already seen"  BETTER

f-string quote rule:
  f"Order {cleaned['order_id']}"   <- single quotes inside double-quoted f-string
  f'Order {cleaned["order_id"]}'   <- double quotes inside single-quoted f-string
  Keep quote types different. Works in all Python versions.
```

---

### 2.9 Building a DE Pipeline With Functions

```python
def load_records(filepath):
    """Simulates loading records from a CSV file."""
    return [
        {"id": 1, "amount": 500.0,  "status": "VALID"},
        {"id": 2, "amount": -10.0,  "status": "INVALID"},
        {"id": 3, "amount": 0.0,    "status": "VALID"},
        {"id": 4, "amount": 820.0,  "status": "VALID"},
        {"id": 5, "amount": 150.0,  "status": "INVALID"},
    ]

def clean_record(record):
    """Cleans a single record. Returns a cleaned copy."""
    return {
        "id":     record["id"],
        "amount": max(record["amount"], 0.0),
        "status": record["status"].strip().upper(),
    }

def validate_record(record):
    """Returns True if record is safe to load."""
    return record["amount"] > 0 and record["status"] == "VALID"

def run_pipeline(filepath):
    """Orchestrates the full ETL flow."""
    raw     = load_records(filepath)
    cleaned = [clean_record(r) for r in raw]
    valid   = [r for r in cleaned if validate_record(r)]
    invalid = [r for r in cleaned if not validate_record(r)]

    print(f"Loaded  : {len(raw)}")
    print(f"Valid   : {len(valid)}")
    print(f"Invalid : {len(invalid)}")
    return valid, invalid

valid, invalid = run_pipeline("orders.csv")
```
Output:
```
Loaded  : 5
Valid   : 3
Invalid : 2
```

Each function does ONE job. If validation breaks, you know exactly where to look.
This is the architecture of every real pipeline.

---

### 2.10 Code Review - Checkpoint 1 Issues

ISSUE 1 - Redundant if/else for a boolean:
```python
# WRONG - repeating entire print line just to change True/False
if is_valid(cleaned):
    print(f"... | Valid: True")
else:
    print(f"... | Valid: False")

# CORRECT - embed the returned boolean directly
valid = is_valid(cleaned)
print(f"... | Valid: {valid}")
```

ISSUE 2 - f-string quote style:
```python
# Works in Python 3.12+ but not universal convention
f"Order {cleaned["order_id"]}"

# Correct everywhere
f"Order {cleaned['order_id']}"
```

---

## 3. SQL: IN, BETWEEN, LIKE, NULL Handling

### 3.1 IN Operator - Replacing Multiple ORs

Analogy: A guest list at an event. Instead of asking "is it Akshay OR Priya OR Rahul?",
you ask "is this person IN this list?"

Without IN (verbose):
```sql
SELECT name, city
FROM customers
WHERE city = 'Bangalore'
   OR city = 'Mumbai'
   OR city = 'Chennai';
```

With IN (clean):
```sql
SELECT name, city
FROM customers
WHERE city IN ('Bangalore', 'Mumbai', 'Chennai');
```

Both return the same result. IN is cleaner and easier to extend.

NOT IN - Exclude a set of values:
```sql
SELECT name, city
FROM customers
WHERE city NOT IN ('Bangalore', 'Mumbai');
```
Output: Rahul Sharma (Chennai), Arjun Nair (Delhi)

---

### 3.2 BETWEEN Operator - Range Filtering

BETWEEN is inclusive on both ends (>= and <=).

```sql
SELECT name, age
FROM customers
WHERE age BETWEEN 28 AND 32;
```
Output: Akshay Kumar (28), Priya Patel (32), Sneha Reddy (29)

With dates:
```sql
SELECT name, signup_date
FROM customers
WHERE signup_date BETWEEN '2024-01-01' AND '2024-02-28';
```
BETWEEN with dates: always use single quotes, ISO format (YYYY-MM-DD).

---

### 3.3 LIKE Operator - Pattern Matching

LIKE searches for a text pattern. Two wildcard characters:
```
%   -> matches ANY number of characters (including zero)
_   -> matches exactly ONE character
```

Examples:
```sql
-- Names starting with 'A'
SELECT name FROM customers WHERE name LIKE 'A%';
-- Output: Akshay Kumar, Arjun Nair

-- Names ending with 'Nair'
SELECT name FROM customers WHERE name LIKE '%Nair';
-- Output: Arjun Nair

-- Names containing 'Patel' anywhere
SELECT name FROM customers WHERE name LIKE '%Patel%';
-- Output: Priya Patel

-- Names with exactly 5 characters (one _ per character)
SELECT name FROM customers WHERE name LIKE '_____';
```

CASE SENSITIVITY:
  PostgreSQL: LIKE is case-sensitive. Use ILIKE for case-insensitive.
  MySQL:      LIKE is case-insensitive by default.

---

### 3.4 NULL Handling - THE RULE YOU MUST BURN IN

CRITICAL: In SQL you CANNOT use = NULL or != NULL. They will NEVER work.

```sql
-- WRONG - always returns 0 rows (not an error, just silent failure!)
SELECT * FROM customers WHERE discount = NULL;

-- CORRECT
SELECT * FROM customers WHERE discount IS NULL;

-- WRONG
SELECT * FROM customers WHERE discount != NULL;

-- CORRECT
SELECT * FROM customers WHERE discount IS NOT NULL;
```

WHY does = NULL not work?
NULL is the ABSENCE of a value - not a value itself.
Checking equality against nothingness has no meaning.
NULL = NULL -> returns NULL (not TRUE, not FALSE).
NULL IS NULL -> returns TRUE. Only IS NULL works.

COALESCE - Treat NULL as a default value:
```sql
SELECT
    order_id,
    amount,
    COALESCE(discount, 0)                    AS discount,
    amount - COALESCE(discount, 0)           AS final_amount
FROM orders;
```
COALESCE(discount, 0) means:
  "Use discount if it exists, otherwise use 0."
  This is SQL's equivalent of Python's: record.get("discount", 0.0)

---

### 3.5 Combining Everything - Production Level Query

```sql
SELECT
    customer_id,
    name,
    city,
    age,
    email
FROM customers
WHERE is_active = TRUE
  AND city IN ('Bangalore', 'Mumbai', 'Delhi', 'Chennai', 'Hyderabad')
  AND age BETWEEN 25 AND 35
  AND (email LIKE '%@gmail.com' OR email LIKE '%@yahoo.com')
  AND signup_date BETWEEN '2024-01-01' AND '2024-12-31';
```

This is real production SQL for customer segmentation.

---

### 3.6 THE 4 SQL RULES (cumulative from Days 3 and 4)

```
RULE 1: String literals ALWAYS use SINGLE quotes
  CORRECT:  WHERE city = 'Bangalore'
  WRONG:    WHERE city = "Bangalore"

RULE 2: Every OR condition needs a FULL column comparison
  CORRECT:  WHERE city = 'Chennai' OR city = 'Delhi'
  WRONG:    WHERE city = 'Chennai' OR 'Delhi'

RULE 3: AND binds BEFORE OR - use parentheses when mixing
  CORRECT:  WHERE (city = 'Chennai' OR city = 'Delhi') AND age > 30
  WRONG:    WHERE city = 'Chennai' OR city = 'Delhi' AND age > 30

RULE 4: SQL keywords are UPPERCASE by convention
  CORRECT:  SELECT name FROM customers WHERE age > 28;
  WRONG:    select name from customers where age > 28;
            (works but looks unprofessional)
```

---

### 3.7 Today's Correct SQL Practice Answers

```sql
-- Q1: City IN Bangalore or Delhi
SELECT name, city
FROM customers
WHERE city IN ('Bangalore', 'Delhi');

-- Q2: Age between 25 and 29
SELECT name, age
FROM customers
WHERE age BETWEEN 25 AND 29;

-- Q3: Name starts with A
SELECT name
FROM customers
WHERE name LIKE 'A%';

-- Q4: Discount is NULL
SELECT name, discount
FROM customers
WHERE discount IS NULL;

-- Practice: Amount between 100 and 500
SELECT *
FROM orders
WHERE amount BETWEEN 100 AND 500;

-- Practice: Name contains 'a' anywhere
SELECT *
FROM customers
WHERE name LIKE '%a%';

-- Practice: Phone number missing
SELECT *
FROM customers
WHERE phone_number IS NULL;
```

---

## 4. DSA: Contains Duplicate (LeetCode 217)

### 4.1 The Problem

Given a list of integers, return True if any value appears at least twice.
Return False if every element is distinct.

Real DE use: Before loading data, check if a primary key column has duplicates.

### 4.2 Approach 1 - Brute Force: O(N squared) - Never Use

```python
def contains_duplicate_slow(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False
```

10M records -> 100 trillion comparisons. Unacceptable at DE scale.

### 4.3 Approach 2 - Set: O(N) - Correct Approach

```python
def contains_duplicate(nums):
    seen = set()              # 'seen' communicates intent

    for num in nums:          # 'num' not 'id' - never shadow built-ins
        if num in seen:       # O(1) lookup - instant regardless of size
            return True
        seen.add(num)

    return False

# Test cases
print(contains_duplicate([1, 2, 3, 1]))   # True
print(contains_duplicate([1, 2, 3, 4]))   # False
print(contains_duplicate([1, 1, 1, 3]))   # True
print(contains_duplicate([]))             # False
```

Trace through [1, 2, 3, 1]:
```
seen = {}
num=1: 1 in {} ? No  -> seen = {1}
num=2: 2 in {1} ? No -> seen = {1, 2}
num=3: 3 in {1,2}? No-> seen = {1, 2, 3}
num=1: 1 in {1,2,3}? YES -> return True
```

### 4.4 One-Liner (Production)

```python
def contains_duplicate(nums):
    return len(nums) != len(set(nums))

# If set is smaller than original list -> duplicates were removed -> True
# [1,2,3,1] -> set {1,2,3} -> len 3 != len 4 -> True
# [1,2,3,4] -> set {1,2,3,4} -> len 4 != len 4 -> False
```

Progression:
  Interview   -> seen = set() loop (shows you understand mechanics)
  Production  -> one-liner (concise, readable, Pythonic)

### 4.5 With Duplicate Identification (No Global Variables)

```python
def contains_duplicate(ids):
    seen = set()           # tracks what we've seen
    duplicates = []        # LOCAL - not global

    for num in ids:        # not 'id'
        if num in seen:
            duplicates.append(num)
        seen.add(num)

    return duplicates      # return the result, don't modify global state

customer_ids = [101, 202, 303, 101, 404, 202, 505]
dupes = contains_duplicate(customer_ids)

if dupes:
    print(f"Result is True")
    print(f"Duplicates found: {sorted(set(dupes))}")
else:
    print("Result is False")
    print("No duplicates found")
```
Output:
```
Result is True
Duplicates found: [101, 202]
```

KEY RULE: Never modify global state from inside a function.
Return what you need. Let the caller decide what to do with it.

### 4.6 Applied to Real DE Validation

```python
def validate_primary_key(records, key_column):
    values = [record[key_column] for record in records]

    if len(values) != len(set(values)):
        duplicate_count = len(values) - len(set(values))
        print(f"VALIDATION FAILED: '{key_column}' has {duplicate_count} duplicate(s)!")
        return False

    print(f"'{key_column}' is clean - all {len(values)} values are unique.")
    return True
```

---

## 5. JavaScript: Closures

NOTE: JS section uses web/frontend/Node.js examples - no DE context.

### 5.1 The Analogy: A Backpack That Remembers

A student finishes school. The classroom (outer function) is gone.
But the student (inner function) still carries their backpack -
and the backpack contains everything they learned (outer function's variables).

A CLOSURE is when an inner function remembers the variables from its
outer function's scope EVEN AFTER the outer function has finished running.

---

### 5.2 Building a Closure Step by Step

```javascript
function makeGreeter(name) {
    // 'name' is a local variable in makeGreeter

    function greet() {
        // 'greet' can access 'name' from the outer scope
        console.log(`Hello, ${name}!`);
    }

    return greet;    // Return the function itself, NOT its result
}

const greetAkshay = makeGreeter("Akshay");
// makeGreeter has FINISHED running
// But 'name' = "Akshay" is still alive inside greetAkshay's closure!

greetAkshay();    // "Hello, Akshay!"
greetAkshay();    // "Hello, Akshay!" - still works!
```

`greetAkshay` is a CLOSURE.
It is the `greet` function, but it has captured the `name` variable.
Even though `makeGreeter` is done, name is kept alive in memory
because the closure holds a reference to it.

---

### 5.3 Counter Factory - Private State

```javascript
function makeCounter(start = 0) {
    let count = start;      // Private state - nobody outside can touch this

    return {
        increment() { count++; },
        decrement() { count--; },
        reset()     { count = start; },
        value()     { return count; }
    };
}

const pageViews   = makeCounter(0);
const errorCount  = makeCounter(0);

pageViews.increment();
pageViews.increment();
pageViews.increment();
errorCount.increment();

console.log("Page views :", pageViews.value());    // 3
console.log("Errors     :", errorCount.value());   // 1
```

pageViews and errorCount are completely independent.
Each has its own private `count` - protected by closure.
Nobody outside can access `count` directly.
This is ENCAPSULATION through closures.

---

### 5.4 Function Factory Pattern

```javascript
function makeMultiplier(factor) {
    return function(number) {
        return number * factor;
    };
}

const double = makeMultiplier(2);   // closes over: factor = 2
const triple = makeMultiplier(3);   // closes over: factor = 3 (SEPARATE closure!)

console.log(double(5));              // 5 * 2 = 10
console.log(triple(5));              // 5 * 3 = 15
console.log(double(triple(4)));      // triple(4)=12, double(12)=24
```

Q: Does double share factor with triple?
A: NO. Each call to makeMultiplier() creates a BRAND NEW execution context
   with its OWN factor variable. makeMultiplier(2) creates one closure with
   factor=2. makeMultiplier(3) creates a completely separate closure with factor=3.
   They do not share anything.

---

### 5.5 The Classic var Bug in Loops (Interview Trap)

```javascript
// What does this print?
for (var i = 0; i < 3; i++) {
    setTimeout(function() {
        console.log(i);
    }, 100);
}
```
Output (SURPRISING):
```
3
3
3
```

NOT 0, 1, 2. WHY?
var is function-scoped. There is ONLY ONE i shared across all three callbacks.
By the time the timeouts fire, the loop has finished and i = 3.
All three callbacks close over the SAME i, which is now 3.

Fix using let (block-scoped - creates a NEW i for each iteration):
```javascript
for (let i = 0; i < 3; i++) {
    setTimeout(function() {
        console.log(i);
    }, 100);
}
```
Output: 0 / 1 / 2 (each callback captures its OWN i)

This is why var is banned in modern JavaScript.
It breaks closure behavior in loops.

---

### 5.6 Today's Practice Answer

```javascript
function makeAdder(x) {
    return function(y) {
        return x + y;
    };
}
const add5  = makeAdder(5);     // closes over x = 5
const add10 = makeAdder(10);    // closes over x = 10 (separate!)

console.log(add5(3));           // 5 + 3    = 8
console.log(add10(3));          // 10 + 3   = 13
console.log(add5(add10(2)));    // add10(2) = 12, add5(12) = 17
```

EVALUATION TIP: When you see nested calls, ALWAYS evaluate inside-out.
add10(2) executes first -> 12. Then add5(12) executes -> 17.
Write it out on paper. Don't do it in your head.

---

## 6. Day 4 Code Review Summary

| Checkpoint | Score | Key Issue |
|:-----------|:------|:----------|
| Python Functions | 8/10 | f-string quote style; redundant if/else for boolean |
| SQL Filtering | 6/10 | Merged 4 separate queries into 1; WHERE lowercase |
| Contains Duplicate | 7/10 | Global state; 'id' shadows built-in; 'sets' not 'seen' |
| JS Closures | 8/10 | Arithmetic typo (26->24); vague closure explanation |
| **Total** | **29/40 (73%)** | |

Practice Review:
| Practice | Score | Issue |
|:---------|:------|:------|
| No global variables | 8/10 | Still used 'id' and 'sets' after explicit callout |
| SQL three queries | 8/10 | 'where' should be 'WHERE' |
| JS closures output | 10/10 | Perfect |
| **Total** | **26/30 (87%)** | |

Three standing patterns to fix:
1. Read the question fully before writing the answer (SQL Q2 mistake)
2. Action ALL review comments, not just the main one (Practice 1 naming)
3. SQL Rule 4: ALL keywords uppercase, every time

---

## 7. FAANG Interview Question Vault

### Junior Level

Q: What is a function parameter vs a function argument?
A: A parameter is the variable name in the function DEFINITION.
   An argument is the actual value passed when CALLING the function.
   def greet(name):   <- 'name' is a parameter
   greet("Akshay")    <- "Akshay" is an argument

Q: What does COALESCE do in SQL?
A: COALESCE returns the first non-NULL value from a list of expressions.
   COALESCE(discount, 0) returns discount if it exists, otherwise 0.
   It is SQL's equivalent of Python's dict.get("key", default).

Q: Why does "WHERE column = NULL" not work in SQL?
A: Because NULL represents the absence of a value, not a value itself.
   Equality comparison against NULL is undefined - it returns NULL, not TRUE.
   The correct syntax is always IS NULL or IS NOT NULL.

### Mid Level

Q: What is a closure in JavaScript? Give a real use case.
A: A closure is when an inner function retains access to variables from its
   outer function's scope even after the outer function has returned.
   Real use: makeCounter() - each counter maintains private state that cannot
   be accessed or corrupted from outside the function.

Q: What is the time complexity difference between 'num in list' vs 'num in set'?
A: list: O(N) - scans every element until found or exhausted.
   set: O(1) - uses a hash table, constant time regardless of size.
   For the Contains Duplicate problem, using a list as the 'seen' structure
   would make the entire algorithm O(N squared). Using a set makes it O(N).

Q: In Python, what happens when a function modifies a global variable?
A: This is a side effect - the function's behavior depends on and modifies
   external state. This makes the function hard to test, hard to reason about,
   and dangerous in concurrent/multi-threaded environments. Best practice:
   pass everything the function needs as parameters, return results,
   never reach outside the function to modify global state.

---

## 8. Debugging Challenges for Day 5

Bug 1: What is wrong with this function and what happens when you call it?
```python
def get_total(records):
    total = 0
    for record in records:
        total += record["amount"]
    print(total)

result = get_total([{"amount": 100}, {"amount": 200}])
print(f"Total: {result}")
```

Bug 2: What does this SQL return and why is it wrong?
```sql
SELECT name, age
FROM customers
WHERE age BETWEEN 30 AND 25;
```

Bug 3: What does this JS print and why?
```javascript
function outer() {
    let message = "hello";

    function inner() {
        message = "goodbye";    // No 'let' or 'const' here
    }

    inner();
    console.log(message);
}
outer();
```

---

## 9. Spaced Repetition Checklist

Review on Day 5, Day 11, and Day 32. Cover answer. Say it out loud.

- [ ] What is the difference between a parameter and an argument?
- [ ] Write a function with a default parameter from memory.
- [ ] What does a function return when there is no return statement?
- [ ] What is function scope? Can outer code see variables inside a function?
- [ ] SQL: What does IN do? Write one example.
- [ ] SQL: What does BETWEEN do? Is it inclusive or exclusive at the ends?
- [ ] SQL: What does LIKE '%a%' match? What does LIKE 'a%' match?
- [ ] SQL: Why does WHERE column = NULL never work? What do you use instead?
- [ ] DSA: What is the time complexity of 'num in set' vs 'num in list'?
- [ ] JS: What is a closure? Give the backpack analogy in one sentence.
- [ ] JS: Why does the var-in-loop bug print 3,3,3 instead of 0,1,2?

---

Day 04 complete - 2026-09-29
Score: 73% (29/40) + Practice: 87% (26/30)
Running Average: ~81%
Next: Day 05 - Week 1 Project Day (Mini Data Validation Pipeline)