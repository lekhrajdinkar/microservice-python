## A. list of Library/modules
### built-in library

| Category            | Library/Module                                                  | Description                                                                   |
| ------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| File I/O            | `open`, `io`, `os`, `pathlib`                                   | File handling, path manipulation, low-level and high-level APIs               |
| Networking          | `socket`, `http.client`, `urllib`                               | Low-level and high-level network communication                                |
| Concurrency         | `threading`, `asyncio`, `concurrent.futures`, `multiprocessing` | Multithreading, async programming, parallel execution                         |
| Regular Expressions | `re`                                                            | Pattern matching and text parsing                                             |
| Data Serialization  | `json`, `pickle`, `marshal`                                     | Serialize/deserialize objects                                                 |
| Date & Time         | `datetime`, `time`, `calendar`                                  | Date/time manipulation and formatting                                         |
| Error Handling      | `BaseException`, `Exception`, `traceback`                       | Exception hierarchy and debugging                                             |
| Functional Tools    | `functools`, `itertools`, `lambda`, `callable`                  | Functional programming helpers                                                |
| Math & Numbers      | `math`, `cmath`, `decimal`, `fractions`, `random`               | Basic to advanced math operations                                             |
| Collections         | `collections`, `heapq`, `queue`                                 | Advanced containers: `deque`, `Counter`, `defaultdict`, `namedtuple`, `Queue` |
| Dataclasses         | `dataclasses`                                                   | `@dataclass` to auto-generate boilerplate methods                             |
| Generics/Typing     | `typing`, `collections.abc`                                     | Type hinting, abstract base classes                                           |

### 3rd party

| Area                 | Library                                             | Description                                    |
| -------------------- | --------------------------------------------------- | ---------------------------------------------- |
| Web Framework        | `fastapi`, `flask`, `django`                        | Web API and backend development                |
| ASGI Server          | `uvicorn`                                           | Production-grade ASGI server for FastAPI       |
| HTTP Requests        | `httpx`, `requests`, `aiohttp`                      | Sync and async HTTP clients                    |
| Data Science         | `numpy`, `pandas`, `scipy`, `matplotlib`, `seaborn` | Data processing, stats, and visualization      |
| Task Scheduling      | `celery`, `apscheduler`                             | Distributed task queues and schedulers         |
| Caching              | `redis`, `diskcache`, `cachetools`                  | In-memory or file-based caching                |
| Parsing & Validation | `pydantic`, `marshmallow`                           | Data validation and parsing for APIs           |
| Testing              | `pytest`, `unittest`, `hypothesis`                  | Unit, functional, and property-based testing   |
| Environment Config   | `python-decouple`, `dotenv`                         | Manage env variables and config files          |
| Security             | `bcrypt`, `cryptography`, `hashlib`                 | Password hashing, encryption                   |
| Performance          | `cython`, `numba`, `joblib`                         | Speed up code with C extensions or parallelism |
| Logging & Monitoring | `loguru`, `structlog`, `sentry-sdk`                 | Structured logging and error monitoring        |

---
## B. Design patterns 🅿️ 
### 1. profile / performance
- python -m timeit -s "lst = list(range(1000))" "sum(lst)"
- python -m cProfile your_script.py