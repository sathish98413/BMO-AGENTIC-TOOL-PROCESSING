from langchain_core.tools import tool
import ast
import operator
from simpleeval import simple_eval


@tool
def text_processor(text: str, operation: str) -> str:
    """Process text."""

    operation = operation.lower().strip()

    if operation == "uppercase":
        return text.upper()

    if operation == "lowercase":
        return text.lower()

    if operation == "word_count":
        return str(len(text.split()))

    if operation == "character_count":
        return str(len(text))

    if operation == "reverse":
        return text[::-1]

    return f"Unsupported text operation: {operation}"


    

@tool
def calculator_simple(expression: str) -> str:
    """Perform basic arithmetic."""
    try:
        return str(simple_eval(expression))
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception:
        return "Error: Invalid expression"   


@tool
def weather_mock(city: str) -> str:
    """Return mock weather."""

    weather = {
        "toronto": "22°C, Partly Cloudy, Humidity 65%",
        "mississauga": "21°C, Sunny, Humidity 60%",
        "new york": "25°C, Clear, Humidity 55%",
        "chicago": "20°C, Rainy, Humidity 75%",
        "london": "18°C, Cloudy, Humidity 70%",
    }

    city_key = city.lower().strip()

    result = weather.get(
        city_key,
        "20°C, Partly Cloudy, Humidity 60%"
    )

    return f"Weather in {city.title()}: {result}"