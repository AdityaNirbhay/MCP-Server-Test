import math
import statistics
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Demo")


# ---------- Math tools ----------

@mcp.tool()
def add(a: float, b: float) -> float:
    """Adds two numbers"""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtracts b from a"""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers"""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divides a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Raises base to the given exponent"""
    return math.pow(base, exponent)


@mcp.tool()
def sqrt(x: float) -> float:
    """Square root of a non-negative number"""
    if x < 0:
        raise ValueError("Cannot take the square root of a negative number")
    return math.sqrt(x)


@mcp.tool()
def stats(numbers: list[float]) -> dict:
    """Returns count, sum, mean, median, min and max for a list of numbers"""
    if not numbers:
        raise ValueError("Provide at least one number")
    return {
        "count": len(numbers),
        "sum": sum(numbers),
        "mean": statistics.mean(numbers),
        "median": statistics.median(numbers),
        "min": min(numbers),
        "max": max(numbers),
    }


# ---------- Text tools ----------

@mcp.tool()
def word_count(text: str) -> dict:
    """Counts words, characters and lines in a piece of text"""
    return {
        "words": len(text.split()),
        "characters": len(text),
        "lines": len(text.splitlines()) or (1 if text else 0),
    }


@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverses a string"""
    return text[::-1]


@mcp.tool()
def change_case(text: str, mode: str = "upper") -> str:
    """Changes text case. mode: upper, lower, title, or snake"""
    if mode == "upper":
        return text.upper()
    if mode == "lower":
        return text.lower()
    if mode == "title":
        return text.title()
    if mode == "snake":
        return "_".join(text.lower().split())
    raise ValueError("mode must be one of: upper, lower, title, snake")


@mcp.tool()
def is_palindrome(text: str) -> bool:
    """Checks whether text reads the same forwards and backwards (ignores case and non-alphanumerics)"""
    cleaned = "".join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]


# ---------- Date/time tools ----------

@mcp.tool()
def current_time(timezone_name: str = "UTC") -> str:
    """Current date and time in an IANA timezone, e.g. 'Asia/Kolkata' or 'America/New_York'"""
    try:
        tz = ZoneInfo(timezone_name)
    except Exception:
        raise ValueError(f"Unknown timezone: {timezone_name}")
    return datetime.now(tz).isoformat(timespec="seconds")


@mcp.tool()
def days_between(start: str, end: str) -> int:
    """Number of days from start to end. Dates in YYYY-MM-DD format"""
    d1 = datetime.strptime(start, "%Y-%m-%d")
    d2 = datetime.strptime(end, "%Y-%m-%d")
    return (d2 - d1).days


# ---------- Unit conversion ----------

@mcp.tool()
def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Converts temperature between 'C', 'F' and 'K'"""
    f, t = from_unit.upper(), to_unit.upper()
    if f not in "CFK" or t not in "CFK" or len(f) != 1 or len(t) != 1:
        raise ValueError("Units must be C, F or K")
    celsius = {"C": value, "F": (value - 32) * 5 / 9, "K": value - 273.15}[f]
    return {"C": celsius, "F": celsius * 9 / 5 + 32, "K": celsius + 273.15}[t]


# ---------- Resources ----------

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}"


@mcp.resource("info://server")
def server_info() -> str:
    """Basic information about this server"""
    return f"Demo MCP server. Started check at {datetime.now(timezone.utc).isoformat(timespec='seconds')}"


# ---------- Prompts ----------

@mcp.prompt()
def explain_code(code: str, language: str = "Python") -> str:
    """Prompt template that asks for a clear explanation of a code snippet"""
    return f"Explain the following {language} code step by step:\n\n{code}"


if __name__ == "__main__":
    mcp.run()