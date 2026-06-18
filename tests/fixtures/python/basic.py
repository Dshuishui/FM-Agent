def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


async def fetch(url):
    pass


@staticmethod
def greet(name):
    return f"Hello, {name}"


@decorator_a
@decorator_b
def multi_decorated():
    pass


def outer():
    def inner():
        pass
    return inner


def long_signature(
    param_a: int,
    param_b: str,
    param_c: float = 0.0,
) -> bool:
    return True


SQL = """
def fake_in_string():
    pass
"""
