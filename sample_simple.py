"""
sample_simple.py — Minimal test file for fm-agent.ai validation.
Contains a mix of correct and intentionally buggy functions.
Expected: 4 correct, 4 incorrect → ~50% pass rate.
"""


# ── Correct functions ─────────────────────────────────────


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def is_even(n):
    """Return True if n is even."""
    return n % 2 == 0


def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit."""
    return c * 9 / 5 + 32


def count_vowels(s):
    """Count the number of vowels in a string."""
    return sum(1 for ch in s.lower() if ch in "aeiou")


# ── Buggy functions (intentional errors) ─────────────────


def subtract(a, b):
    """Return a minus b."""
    return a + b  # BUG: should be a - b


def is_odd(n):
    """Return True if n is odd."""
    return n % 2 == 0  # BUG: logic inverted, returns True for even


def factorial(n):
    """Return n! recursively."""
    if n == 0:
        return 0  # BUG: base case should return 1
    return n * factorial(n - 1)


def celsius_to_kelvin(c):
    """Convert Celsius to Kelvin."""
    return c - 273.15  # BUG: should be c + 273.15


if __name__ == "__main__":
    print("add(2, 3)               =", add(2, 3))
    print("is_even(4)              =", is_even(4))
    print("celsius_to_fahrenheit(0)=", celsius_to_fahrenheit(0))
    print("count_vowels('hello')   =", count_vowels("hello"))
    print("subtract(5, 3)          =", subtract(5, 3))
    print("is_odd(3)               =", is_odd(3))
    print("factorial(5)            =", factorial(5))
    print("celsius_to_kelvin(0)    =", celsius_to_kelvin(0))
