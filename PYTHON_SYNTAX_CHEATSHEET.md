# Python Syntax Cheatsheet

> **Target:** Python 3.11+  
> **Purpose:** Quick reference for syntax you can use in any Python project — web apps, scripts, data, tests, CLI tools.  
> **How to use:** Use the table of contents to jump to a section. Each entry shows minimal syntax + a one-line note.

---

## Table of Contents

1. [Module & Imports](#1-module--imports)
2. [Variables & Literals](#2-variables--literals)
3. [Operators](#3-operators)
4. [Control Flow](#4-control-flow)
5. [Loops](#5-loops)
6. [Comprehensions](#6-comprehensions)
7. [Functions](#7-functions)
8. [Classes & OOP](#8-classes--oop)
9. [Type Hints](#9-type-hints)
10. [Decorators](#10-decorators)
11. [Data Structures — Operations](#11-data-structures--operations)
12. [Unpacking & Spread](#12-unpacking--spread)
13. [Context Managers](#13-context-managers)
14. [Generators & Iterators](#14-generators--iterators)
15. [Async / Await](#15-async--await)
16. [Exceptions](#16-exceptions)
17. [Files, Paths & Serialization](#17-files-paths--serialization)
18. [Stdlib Essentials](#18-stdlib-essentials)
19. [itertools & functools](#19-itertools--functools)
20. [collections Module](#20-collections-module)
21. [Regex (re)](#21-regex-re)
22. [Datetime & Timezones](#22-datetime--timezones)
23. [Logging](#23-logging)
24. [CLI Scripts](#24-cli-scripts)
25. [Testing (pytest)](#25-testing-pytest)
26. [Context Variables & Threading](#26-context-variables--threading)
27. [Special Dunders](#27-special-dunders)
28. [Pattern Matching (match/case)](#28-pattern-matching-matchcase)
29. [Web/API Quick Reference](#29-webapi-quick-reference)
30. [Syntax Quick Lookup Table](#30-syntax-quick-lookup-table)

---

## 1. Module & Imports

```python
# Standard import
import os
import json
import sys

# Import specific names
from pathlib import Path
from datetime import datetime, timezone

# Alias
import numpy as np
from collections import defaultdict as dd

# Postponed annotation evaluation (recommended in new projects)
from __future__ import annotations

# Relative imports (inside packages only)
from .utils import helper          # same package
from ..models import User          # parent package
from . import submodule

# Lazy import (avoid circular imports or heavy startup)
def get_heavy_module():
    import heavy_library
    return heavy_library

# Re-exports
from .serialization import profile  # noqa: F401
__all__ = ["profile", "user"]

# Check if running as script vs imported
if __name__ == "__main__":
    main()
```

| Pattern | Use when |
|---------|----------|
| `import x` | Namespace clarity (`os.path`) |
| `from x import y` | Short, frequent use |
| `from __future__ import annotations` | Cleaner type hints, forward refs |
| Lazy import | Circular deps, optional deps, slow modules |

---

## 2. Variables & Literals

```python
# Basic assignment
name = "Alice"
count = 0
price = 19.99
active = True
missing = None

# Multiple assignment
x, y, z = 1, 2, 3
a = b = c = 0

# Annotated assignment
total: int = 0
items: list[str] = []

# Constants (convention — uppercase, not enforced)
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30.0

# Delete
del variable_name
del obj["key"]
```

### Strings

```python
# f-strings (preferred)
msg = f"Hello, {name}!"
aligned = f"{name:<20} {score:>6.2f}"   # left/right align, width, decimals
hex_id = f"{user_id:#x}"

# f-string debug (3.8+)
debug = f"{count=}"                      # "count=42"

# Other formats
old = "Hello, {}".format(name)
percent = "Score: %.2f" % score
raw = r"C:\new\folder"                   # backslashes literal
multiline = """line one
line two"""

# String methods (common)
s.strip()          s.lower()         s.upper()
s.startswith("x")  s.endswith(".py") s.replace("a", "b")
s.split(",")       ",".join(parts)    s.find("sub")
```

### Numbers

```python
int("42")          float("3.14")     bool(1)
int("ff", 16)      # hex
divmod(10, 3)      # (3, 1)
round(3.14159, 2)  # 3.14
abs(-5)            pow(2, 8)         2 ** 8
```

---

## 3. Operators

### Arithmetic

```python
a + b    a - b    a * b    a / b       # true division → float
a // b   a % b    a ** b   -a    +a
```

### Comparison & Identity

```python
a == b   a != b   a < b   a <= b   a > b   a >= b
a is b           # same object (use for None, True, False)
a is not b
a in seq         a not in seq
```

### Logical (short-circuit)

```python
a and b    a or b    not a
# and/or return last evaluated operand, not always bool
result = default or compute()
```

### Assignment operators

```python
x += 1    x -= 1    x *= 2    x /= 2
x //= 1   x %= 2    x **= 2
x &= m    x |= m    x ^= m    x <<= 1   x >>= 1
```

### Walrus operator (3.8+)

```python
# Assign inside expression
if (n := len(items)) > 10:
    print(f"Too many: {n}")

while (line := f.readline()):
    process(line)

[y for x in data if (y := transform(x)) > 0]
```

### Bitwise

```python
a & b    a | b    a ^ b    ~a    a << 2    a >> 2
```

### Chained comparisons

```python
0 < x < 100
a == b == c
```

---

## 4. Control Flow

```python
# if / elif / else
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

# Ternary
status = "active" if is_active else "inactive"

# Truthiness — False: None, False, 0, 0.0, "", [], {}, set()
if items:              # non-empty
if not user:
if value is not None:   # explicit None check (0 and "" may be valid)
```

---

## 5. Loops

```python
# for
for item in iterable:
    process(item)

# while
while condition:
    condition = update()

# break / continue / else
for x in data:
    if x is None:
        continue
    if x == target:
        break
else:
    print("loop completed without break")

# range
for i in range(5):           # 0, 1, 2, 3, 4
for i in range(2, 10):       # 2..9
for i in range(0, 10, 2):    # 0, 2, 4, 6, 8
list(range(3))               # [0, 1, 2]
```

---

## 6. Comprehensions

```python
# List comprehension
squares = [x * x for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]

# Dict comprehension
by_id = {u.id: u for u in users}
inverted = {v: k for k, v in mapping.items()}

# Set comprehension
unique = {word.lower() for word in words}

# Generator expression (lazy — no list allocated)
total = sum(x * x for x in range(1000))
first = next(x for x in items if x.valid)

# Nested
matrix = [[i * j for j in range(3)] for i in range(3)]
rows = [{k: row.get(k) for k in headers} for row in reader]

# Dict/set from iterables
dict([("a", 1), ("b", 2)])
set("hello")
```

---

## 7. Functions

```python
# Basic
def greet(name: str) -> str:
    """Return a greeting."""
    return f"Hello, {name}"

# Default arguments — NEVER use mutable defaults
def append_ok(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Positional-only (before /)
def connect(host, /, port=5432):
    ...

# Keyword-only (after *)
def create(*, name: str, age: int = 0):
    ...

# Combined
def fn(a, b, /, c, d=0, *, e, f=None):
    ...

# *args / **kwargs
def log(*args, **kwargs):
    print(args, kwargs)

def wrapper(fn, *args, **kwargs):
    return fn(*args, **kwargs)

# lambda (single expression only)
sorted(items, key=lambda x: (-x.score, x.name))

# Nested + nonlocal
def counter():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc

# global (module-level mutation — use sparingly)
count = 0
def increment():
    global count
    count += 1

# Return multiple values (tuple)
def min_max(values):
    return min(values), max(values)

lo, hi = min_max([1, 5, 3])

# Type-only parameters (3.12+)
def process(data: bytes, /, *, encoding: str = "utf-8") -> str:
    ...
```

---

## 8. Classes & OOP

```python
# Basic class
class Person:
    species = "human"                    # class attribute

    def __init__(self, name: str, age: int = 0) -> None:
        self.name = name                 # instance attribute
        self._age = age                  # "private" by convention

    def greet(self) -> str:
        return f"Hi, I'm {self.name}"

# Inheritance
class Employee(Person):
    def __init__(self, name: str, role: str) -> None:
        super().__init__(name)
        self.role = role

# @property
class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    @property
    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    @area.setter
    def area(self, value: float) -> None:
        self.radius = (value / 3.14159) ** 0.5

# @staticmethod — no self/cls
class Math:
    @staticmethod
    def clamp(x: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, x))

# @classmethod — receives class as first arg
class User:
    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(data["name"])

# dataclass
from dataclasses import dataclass, field, asdict, astuple

@dataclass
class Point:
    x: float
    y: float
    tags: list[str] = field(default_factory=list)

@dataclass(frozen=True, order=True)   # immutable, comparable
class Config:
    host: str
    port: int = 8080

# Enum
from enum import Enum, StrEnum, IntEnum, auto

class Status(str, Enum):
    PENDING = "pending"
    DONE = "done"

class Color(StrEnum):
    RED = "red"
    BLUE = "blue"

# Abstract base class
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get(self, id: int) -> object:
        ...

    @abstractmethod
    def save(self, obj: object) -> None:
        ...

# __slots__ — memory optimization, fixed attributes
class SlotPoint:
    __slots__ = ("x", "y")
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

# Make instance callable
class Multiplier:
    def __init__(self, factor: int) -> None:
        self.factor = factor
    def __call__(self, x: int) -> int:
        return x * self.factor

double = Multiplier(2)
double(5)   # 10
```

---

## 9. Type Hints

```python
from __future__ import annotations

# Primitives
name: str
count: int
ratio: float
flag: bool
nothing: None = None

# Modern union (3.10+) — preferred
value: str | None = None
result: int | float

# Legacy union (still valid)
from typing import Optional, Union
value: Optional[str] = None
result: Union[int, float]

# Collections (modern)
names: list[str]
scores: dict[str, float]
unique: set[int]
pair: tuple[str, int]
coords: tuple[float, float, float]

# Legacy collections
from typing import List, Dict, Set, Tuple
names: List[str]

# Callable
from collections.abc import Callable
Handler = Callable[[int, str], bool]
def apply(fn: Callable[[int], int], x: int) -> int:
    return fn(x)

# Literal — constrained values
from typing import Literal
Mode = Literal["read", "write", "append"]
mode: Mode = "read"

# TypedDict — structured dicts
from typing import TypedDict, Required, NotRequired

class UserDict(TypedDict):
    name: str
    age: NotRequired[int]

# Final — cannot reassign
from typing import Final
MAX_SIZE: Final = 100

# TypeVar & Generic
from typing import TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, item: T) -> None:
        self._items.append(item)
    def pop(self) -> T:
        return self._items.pop()

# Protocol — structural subtyping (duck typing with types)
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable) -> None:
    obj.draw()

# Self (3.11+)
from typing import Self

class Builder:
    def set_name(self, name: str) -> Self:
        self.name = name
        return self

# Annotated — attach metadata to types (FastAPI Depends, etc.)
from typing import Annotated
UserId = Annotated[int, "positive user id"]

# cast — tell type checker only (no runtime effect)
from typing import cast
s = cast(str, maybe_string)

# TypeAlias (3.10+)
from typing import TypeAlias
JsonDict: TypeAlias = dict[str, object]

# overload — different signatures for same function
from typing import overload

@overload
def process(x: int) -> int: ...
@overload
def process(x: str) -> str: ...
def process(x: int | str) -> int | str:
    ...
```

---

## 10. Decorators

```python
# Function decorator
def timer(fn):
    import time
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        print(f"{fn.__name__}: {time.perf_counter() - start:.3f}s")
        return result
    return wrapper

@timer
def slow():
    ...

# Decorator with arguments
def repeat(n: int):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = fn(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("hi")

# Preserve metadata
from functools import wraps

def logged(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

# Built-in decorators
@property
@staticmethod
@classmethod
@abstractmethod
@dataclass
@contextmanager
@lru_cache
@cached_property

# Class decorator
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
```

---

## 11. Data Structures — Operations

### list

```python
items = []
items.append(x)          items.extend(iterable)
items.insert(0, x)       items.pop()            items.pop(0)
items.remove(x)          items.clear()
items.copy()             items.reverse()        items.sort(key=fn)
items.index(x)           items.count(x)
items[1:4]               items[:3]              items[::-1]
len(items)               min(items)             max(items)
list(reversed(items))    sorted(items, key=fn)
```

### dict

```python
d = {"a": 1, "b": 2}
d["c"] = 3               d.get("x", default=0)
d.setdefault("k", [])    d.pop("a")             d.popitem()
d.keys()                 d.values()             d.items()
del d["b"]               "a" in d
d | e                    d |= e                 # 3.9+ merge
{**d1, **d2}             d1.update(d2)
dict.fromkeys(["a", "b"], 0)
```

### set

```python
s = {1, 2, 3}
s.add(4)                 s.discard(99)          s.remove(4)   # KeyError if missing
s.clear()                s.copy()
s | t    s & t    s - t    s ^ t
s.union(t)               s.intersection(t)
s.issubset(t)            s.issuperset(t)
frozenset([1, 2, 3])     # immutable set
```

### tuple

```python
t = (1, 2, 3)
single = (42,)           # trailing comma required
x, y, z = t              # unpack
t[0]                     t[1:3]
# named tuple
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
p.x
```

---

## 12. Unpacking & Spread

```python
# Tuple unpacking
a, b = 1, 2
first, *rest, last = [1, 2, 3, 4, 5]    # first=1, rest=[2,3,4], last=5
a, b = b, a                                # swap

# Function call spreading
args = [1, 2, 3]
fn(*args)
kwargs = {"encoding": "utf-8", "errors": "replace"}
open("file.txt", **kwargs)

# Merge iterables
combined = [*list_a, *list_b]
merged = {**dict_a, **dict_b}

# Starred in function definitions
def mixed(a, *args, b=0, **kwargs):
    ...
```

---

## 13. Context Managers

```python
# with statement
with open("file.txt", encoding="utf-8") as f:
    data = f.read()

# Multiple contexts
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read())

# Custom — class-based
class Managed:
    def __enter__(self):
        self.resource = acquire()
        return self.resource
    def __exit__(self, exc_type, exc, tb):
        release(self.resource)
        return False   # don't suppress exceptions

# Custom — decorator
from contextlib import contextmanager

@contextmanager
def temp_file(path):
    f = open(path, "w")
    try:
        yield f
    finally:
        f.close()
        os.remove(path)

# Helpers
from contextlib import suppress, closing, redirect_stdout
with suppress(FileNotFoundError):
    os.remove("tmp.txt")
```

---

## 14. Generators & Iterators

```python
# Generator function
def count_up(n: int):
    for i in range(n):
        yield i

# yield from — delegate to sub-generator
def chain_iters(a, b):
    yield from a
    yield from b

# Generator expression
squares = (x * x for x in range(10))
total = sum(x for x in data if x > 0)

# Iterator protocol
it = iter([1, 2, 3])
next(it)    # 1
next(it)    # 2

# Send / throw (advanced)
def accumulator():
    total = 0
    while True:
        val = yield total
        if val is not None:
            total += val

# itertools.islice, tee, etc. — see Section 19
```

---

## 15. Async / Await

```python
import asyncio

# Async function
async def fetch(url: str) -> str:
    await asyncio.sleep(0.1)
    return "data"

# Run from sync code
asyncio.run(main())

# Async context manager
class AsyncResource:
    async def __aenter__(self):
        return self
    async def __aexit__(self, *args):
        await self.close()

async with AsyncResource() as r:
    ...

# Concurrent tasks
results = await asyncio.gather(task1(), task2(), return_exceptions=True)

# Create task (fire and forget with reference)
task = asyncio.create_task(background_job())

# Async generator
async def stream():
    for item in items:
        yield item
        await asyncio.sleep(0)

# asyncio.to_thread — run blocking code in thread pool (3.9+)
result = await asyncio.to_thread(blocking_io, arg)
```

---

## 16. Exceptions

```python
# try / except / else / finally
try:
    result = risky()
except ValueError as exc:
    handle(exc)
except (TypeError, KeyError) as exc:
    handle(exc)
except Exception:
    log.exception("unexpected")
    raise
else:
    # runs only if no exception raised
    use(result)
finally:
    cleanup()   # always runs

# raise
raise ValueError("invalid input")
raise CustomError("msg") from original_exc   # exception chaining

# Custom exception hierarchy
class AppError(Exception):
    """Base for app errors."""

class NotFoundError(AppError):
    def __init__(self, resource: str) -> None:
        super().__init__(f"{resource} not found")
        self.resource = resource

# Re-raise current exception
except Exception:
    raise

# Exception groups (3.11+)
try:
    raise ExceptionGroup("errors", [ValueError(1), TypeError(2)])
except* ValueError as eg:
    ...

# assert (tests/dev only — disabled with python -O)
assert x > 0, "x must be positive"
```

---

## 17. Files, Paths & Serialization

```python
# pathlib (preferred)
from pathlib import Path

root = Path(__file__).resolve().parent
config = root / "config" / "app.json"

config.exists()          config.is_file()       config.is_dir()
config.read_text(encoding="utf-8")
config.write_text("content", encoding="utf-8")
config.read_bytes()      config.write_bytes(b"...")
config.mkdir(parents=True, exist_ok=True)
config.unlink()          config.rename(new_path)

for path in root.rglob("*.py"):
    print(path.relative_to(root))

# os / os.path (legacy but still common)
import os
os.path.join("a", "b")
os.environ.get("HOME")
os.getenv("API_KEY", "default")
os.listdir(".")
os.makedirs("a/b", exist_ok=True)

# JSON
import json
data = json.loads('{"a": 1}')
text = json.dumps(data, indent=2, ensure_ascii=False)
Path("out.json").write_text(text, encoding="utf-8")

# CSV
import csv
with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["column"])

with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["a", "b"])
    writer.writeheader()
    writer.writerow({"a": 1, "b": 2})

# Pickle (Python-only, not secure for untrusted data)
import pickle
pickle.dump(obj, open("obj.pkl", "wb"))
obj = pickle.load(open("obj.pkl", "rb"))

# Binary read/write
with open("file.bin", "rb") as f:
    data = f.read()
```

---

## 18. Stdlib Essentials

```python
# Builtins
len(x)     min(x)     max(x)     sum(x)     abs(x)
any(iter)  all(iter)  sorted(iter, key=fn, reverse=True)
reversed(iter)   enumerate(iter, start=0)   zip(a, b, strict=True)
map(fn, items)   filter(fn, items)
isinstance(x, cls)   issubclass(A, B)
hasattr(obj, "name")   getattr(obj, "name", default)   setattr(obj, "name", val)
iter(obj)   next(it)   id(obj)   hash(obj)
print(..., sep=", ", end="\n", file=sys.stderr)
input("Prompt: ")

# copy
import copy
shallow = copy.copy(obj)
deep = copy.deepcopy(obj)

# math
import math
math.ceil(3.2)   math.floor(3.8)   math.sqrt(2)
math.log(x)      math.pow(2, 10)   math.isnan(x)

# random
import random
random.randint(1, 10)
random.choice(items)
random.shuffle(items)          # in-place
random.sample(items, k=3)

# secrets (cryptographic)
import secrets
secrets.token_hex(16)
secrets.token_urlsafe(32)
secrets.choice(items)

# hashlib
import hashlib
hashlib.sha256(b"data").hexdigest()

# subprocess
import subprocess
result = subprocess.run(["git", "status"], capture_output=True, text=True, check=True)
result.stdout

# sys
import sys
sys.argv                     sys.exit(1)
sys.path.insert(0, str(root))
```

---

## 19. itertools & functools

```python
# itertools
from itertools import (
    chain,          # flatten iterables
    combinations,   # combinations(iterable, r)
    permutations,
    product,        # cartesian product
    cycle, repeat,
    islice,         # slice iterator without materializing
    groupby,        # group consecutive equal keys (sort first!)
    tee,            # split iterator into n
    zip_longest,    # zip with fillvalue
    accumulate,     # running total
    count,          # infinite counter
)

list(combinations([1, 2, 3], 2))     # [(1,2), (1,3), (2,3)]
list(chain([1, 2], [3, 4]))           # [1, 2, 3, 4]
list(islice(range(100), 5))          # [0, 1, 2, 3, 4]

data = sorted(items, key=lambda x: x.category)
for cat, group in groupby(data, key=lambda x: x.category):
    ...

# functools
from functools import (
    partial,         # partial(fn, arg=val)
    reduce,          # reduce(fn, iterable, initial)
    wraps,           # preserve __name__ in decorators
    lru_cache,       # memoize
    cached_property, # compute once per instance
    total_ordering,  # fill in comparison methods
)

from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

@lru_cache
def expensive(x: int) -> int:   # maxsize=128 default
    ...

double = partial(pow, 2)        # double(3) → 8? pow(2,3)=8

from functools import reduce
product = reduce(lambda a, b: a * b, [1, 2, 3, 4], 1)
```

---

## 20. collections Module

```python
from collections import (
    defaultdict,     # auto-init missing keys
    Counter,         # count hashable elements
    deque,           # double-ended queue, O(1) append/pop both ends
    OrderedDict,     # insertion order (dict has this since 3.7)
    namedtuple,      # lightweight immutable records
    ChainMap,        # layered dict lookup
)

# defaultdict
groups: defaultdict[str, list] = defaultdict(list)
groups["east"].append(item)

# Counter
from collections import Counter
counts = Counter(words)
counts.most_common(5)
counts["the"] += 1
counts + counts2

# deque — queues, BFS
from collections import deque
q = deque([start])
while q:
    node = q.popleft()
    q.extend(neighbors)

# ChainMap
import os
config = ChainMap(os.environ, defaults, hardcoded)
```

---

## 21. Regex (re)

```python
import re

# Match / search / findall
m = re.search(r"\d+", "abc123")
if m:
    m.group(0)    m.start()    m.end()

re.findall(r"\w+", text)
re.findall(r"(\d+)-(\d+)", text)   # capture groups

# Substitute / split
re.sub(r"\s+", " ", text)
re.sub(r"(\d+)", r"[\1]", text)    # backreference
re.split(r"[,\s]+", text)

# Compile for reuse
pattern = re.compile(r"^[\w.-]+@[\w.-]+\.\w+$")
pattern.match(email)

# Flags
re.IGNORECASE    re.MULTILINE    re.DOTALL
re.search(r"^start", text, re.MULTILINE)

# Raw strings — always use r"..." for regex patterns
```

---

## 22. Datetime & Timezones

```python
from datetime import datetime, date, time, timedelta, timezone

# Naive datetime
now = datetime.now()
today = date.today()
dt = datetime(2026, 7, 31, 10, 30, 0)

# Timezone-aware (always prefer in production)
utc_now = datetime.now(timezone.utc)
manila = timezone(timedelta(hours=8))
local = datetime.now(manila)

# Parse / format
dt = datetime.fromisoformat("2026-07-31T10:30:00+00:00")
dt.isoformat()
dt.strftime("%Y-%m-%d %H:%M:%S")

# Arithmetic
later = now + timedelta(days=7, hours=2)
delta = later - now
delta.total_seconds()

# date / time components
dt.year   dt.month   dt.day   dt.hour   dt.weekday()
```

---

## 23. Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

logger.debug("detail")
logger.info("started")
logger.warning("deprecated")
logger.error("failed")
logger.exception("with traceback")   # ERROR + exc_info

# Structured-ish
logger.info("user login", extra={"user_id": 42})

# Module-level config in libraries — don't basicConfig in libraries
```

---

## 24. CLI Scripts

```python
# Entry point
def main() -> None:
    ...

if __name__ == "__main__":
    main()

# argparse
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Process files",
    epilog="Example: python script.py input.csv --dry-run",
)
parser.add_argument("input", type=Path, help="Input file")
parser.add_argument("-o", "--output", type=Path, default=Path("out.csv"))
parser.add_argument("--dry-run", action="store_true")
parser.add_argument("--limit", type=int, default=100, metavar="N")
parser.add_argument("-v", "--verbose", action="count", default=0)
parser.add_argument("--mode", choices=["fast", "safe"], default="safe")
args = parser.parse_args()

# sys.argv manual
import sys
if len(sys.argv) < 2:
    print("Usage: ...")
    sys.exit(1)

# Typer / Click (third-party — popular alternatives)
# pip install typer click
```

---

## 25. Testing (pytest)

```python
import pytest

# Basic
def test_add():
    assert add(1, 2) == 3

def test_approx():
    assert 0.1 + 0.2 == pytest.approx(0.3)

# Exceptions
def test_raises():
    with pytest.raises(ValueError, match="invalid"):
        bad_fn()

# Fixture
@pytest.fixture
def db():
    session = create_session()
    yield session
    session.close()

@pytest.fixture(scope="module")
def app_client():
    return TestClient(app)

# Parametrize
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_cases(a, b, expected):
    assert add(a, b) == expected

# Skip / xfail
@pytest.mark.skip(reason="not implemented")
@pytest.mark.skipif(sys.platform == "win32", reason="unix only")
@pytest.mark.xfail(reason="known bug")

# Mock
from unittest.mock import patch, MagicMock, AsyncMock

@patch("mymodule.external_api")
def test_with_mock(mock_api):
    mock_api.return_value = {"ok": True}
    ...

# pytest.raises as context
with patch.object(settings, "debug", True):
    ...
```

---

## 26. Context Variables & Threading

```python
# contextvars — request-scoped state in async apps
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar("request_id", default="")

def middleware():
    token = request_id.set("abc-123")
    try:
        handle_request()
    finally:
        request_id.reset(token)

# threading (basic)
import threading
t = threading.Thread(target=worker, args=(arg,))
t.start()
t.join()

# concurrent.futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fn, items))

# multiprocessing — CPU-bound parallelism
from multiprocessing import Pool
with Pool(4) as p:
    p.map(fn, items)
```

---

## 27. Special Dunders

| Dunder | Purpose |
|--------|---------|
| `__init__(self, ...)` | Constructor |
| `__str__(self)` | Human-readable (`str(obj)`) |
| `__repr__(self)` | Developer-readable (`repr(obj)`) |
| `__len__(self)` | `len(obj)` |
| `__getitem__(self, key)` | `obj[key]` |
| `__setitem__(self, key, val)` | `obj[key] = val` |
| `__iter__(self)` | `for x in obj` |
| `__enter__` / `__exit__` | Context manager |
| `__call__(self, ...)` | Callable instance |
| `__eq__(self, other)` | `==` |
| `__lt__` etc. | Ordering (`<`, `sort`) |
| `__hash__(self)` | `hash(obj)`, set/dict keys |
| `__bool__(self)` | Truthiness |
| `__getattr__(self, name)` | Missing attribute access |
| `__setattr__(self, name, val)` | Attribute assignment |

```python
class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __len__(self) -> int:
        return 2

    def __getitem__(self, i: int) -> float:
        return (self.x, self.y)[i]
```

---

## 28. Pattern Matching (match/case)

Python 3.10+ structural pattern matching.

```python
def handle_status(status: str) -> str:
    match status:
        case "ok":
            return "success"
        case "error" | "failed":          # OR pattern
            return "failure"
        case _:
            return "unknown"

# Match with binding
def describe(value) -> str:
    match value:
        case 0:
            return "zero"
        case [x, y]:
            return f"pair: {x}, {y}"
        case [x, *rest]:
            return f"head {x}, rest {rest}"
        case {"name": name, "age": age}:
            return f"{name} is {age}"
        case int(n) if n > 0:
            return f"positive int {n}"
        case _:
            return "other"

# Match class instances
case Point(x=0, y=0):
    ...
case Point(x=x, y=y):
    ...
```

---

## 29. Web/API Quick Reference

Common patterns when building APIs (FastAPI, Flask, Django REST, etc.).

```python
# Environment config
import os
DATABASE_URL = os.environ["DATABASE_URL"]
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# HTTP client (requests — third party)
# pip install requests httpx
import httpx
response = httpx.get("https://api.example.com/data", timeout=30.0)
response.raise_for_status()
data = response.json()

# FastAPI route sketch
from fastapi import FastAPI, Depends, HTTPException, Query, status

app = FastAPI()

@app.get("/items")
def list_items(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    return {"page": page, "limit": limit}

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate):
    ...

# Pydantic model sketch
from pydantic import BaseModel, Field, field_validator

class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    price: float = Field(ge=0)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()

# SQLAlchemy query sketch
# rows = session.query(Model).filter(Model.active == True).limit(10).all()
```

---

## 30. Syntax Quick Lookup Table

| I want to… | Syntax |
|------------|--------|
| Import a module | `import mod` / `from mod import x` |
| Type a nullable string | `str \| None` |
| Loop with index | `for i, x in enumerate(items):` |
| Loop two lists together | `for a, b in zip(xs, ys):` |
| Build list from loop | `[f(x) for x in items if cond(x)]` |
| Build dict from loop | `{k: v for k, v in pairs}` |
| Default empty list arg | `field(default_factory=list)` |
| Read a file | `Path(p).read_text(encoding="utf-8")` |
| Parse JSON | `json.loads(text)` |
| Handle errors | `try: ... except Exc as e: ... finally: ...` |
| Raise with cause | `raise NewError("msg") from e` |
| Lazy sequence | `(x for x in items if cond(x))` |
| Memoize function | `@lru_cache` |
| Count occurrences | `Counter(items)` |
| Group by key | `groupby(sorted(data, key=fn), key=fn)` |
| Queue BFS | `deque` + `popleft()` |
| Sort custom order | `sorted(items, key=lambda x: x.score, reverse=True)` |
| Partial application | `partial(fn, arg=val)` |
| Run async main | `asyncio.run(main())` |
| CLI args | `argparse.ArgumentParser()` |
| Test exception | `pytest.raises(ValueError)` |
| Mock external call | `@patch("module.fn")` |
| Match structure | `match x: case {"k": v}: ...` |
| Assign in if | `if (n := len(x)) > 0:` |
| Merge dicts | `{**a, **b}` or `a \| b` |
| Spread args | `fn(*args, **kwargs)` |
| Context manager | `with open(...) as f:` |
| DB session cleanup | `try: yield db finally: db.close()` |
| Enum constants | `class Color(str, Enum): RED = "red"` |
| Abstract interface | `class Port(ABC): @abstractmethod` |
| Duck typing types | `class Proto(Protocol): def fn(self): ...` |

---

## Learning Path Suggestion

| Stage | Focus sections |
|-------|------------------|
| **Beginner** | 1–6, 11, 17 |
| **Intermediate** | 7–10, 12–16, 18, 22–25 |
| **Advanced** | 19–21, 26–28 |
| **Web projects** | 9, 15, 25, 29 |

---

*Generated for personal reference. Python 3.11+ syntax. Third-party libraries (FastAPI, requests, pytest) noted where relevant.*
