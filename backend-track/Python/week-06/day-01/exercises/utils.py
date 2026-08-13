# Day 21 - 15 utility functions. The first 3 are SOLVED (fully typed,
# worked together in the session). The remaining 12 have complete,
# correct bodies but NO type hints yet - that's your job. Each has a
# docstring describing its parameters and return value; use it to decide
# the right hints (see LESSON.md Sections 2-5).
#
# Check your work: mypy exercises/utils.py
# Goal: "Success: no issues found in 1 source file"


# --- SOLVED (1-3) --------------------------------------------------------

def average(numbers: list[float]) -> float:
    """Return the mean of a list of numbers."""
    return sum(numbers) / len(numbers)


def find_student(students: list[dict], name: str) -> dict | None:
    """Return the first student dict whose 'name' matches, or None."""
    for student in students:
        if student["name"] == name:
            return student
    return None


def format_currency(amount: float) -> str:
    """Format a number as XAF currency, e.g. 1500000 -> '1,500,000 XAF'."""
    return f"{amount:,.0f} XAF"


# --- Your turn (4-15) -----------------------------------------------------

def is_passing(score):
    """Given a score (0-100), return True if it is 50 or above."""
    return score >= 50


def letter_grade(score):
    """Given a score (0-100), return the letter grade as a string ('A'-'F')."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"


def top_scorer(students):
    """Given a list of student dicts (each with 'name' and 'score'), return
    the dict of the student with the highest score. Assume the list is
    never empty."""
    return max(students, key=lambda s: s["score"])


def filter_passing(students):
    """Given a list of student dicts, return only the ones with score >= 50."""
    return [s for s in students if s["score"] >= 50]


def student_names(students):
    """Given a list of student dicts, return a list of just their names (strings)."""
    return [s["name"] for s in students]


def score_bounds(scores):
    """Given a list of integer scores, return a (min, max) pair."""
    return min(scores), max(scores)


def merge_settings(defaults, overrides):
    """Given two dicts mapping string keys to string values, return a new
    dict with overrides applied on top of defaults."""
    return {**defaults, **overrides}


def safe_divide(a, b):
    """Divide a by b. If b is 0, return None instead of raising an error."""
    if b == 0:
        return None
    return a / b


def total_of(*numbers):
    """Accept any number of integer arguments and return their sum."""
    return sum(numbers)


def build_profile(**fields):
    """Accept any number of keyword arguments, all strings, and return them
    as a dict."""
    return fields


def retry_count(attempts, max_attempts=3):
    """Given how many attempts have been made and an optional max (default
    3), return how many attempts remain (never negative)."""
    remaining = max_attempts - attempts
    return remaining if remaining > 0 else 0


def describe_course(title, student_count=None):
    """Given a course title and an optional student count, return a
    description string. If student_count is None, omit it from the string."""
    if student_count is None:
        return title
    return f"{title} ({student_count} students)"
