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
def calculator(expression: str) -> str:
    """Perform basic arithmetic."""

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid number")

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)

            op = operators.get(type(node.op))

            if not op:
                raise ValueError("Unsupported operator")

            return op(left, right)

        if isinstance(node, ast.UnaryOp):

            value = evaluate(node.operand)

            if isinstance(node.op, ast.USub):
                return -value

            if isinstance(node.op, ast.UAdd):
                return value

        raise ValueError("Invalid expression")

    try:
        tree = ast.parse(expression, mode="eval")
        return str(evaluate(tree.body))

    except ZeroDivisionError:
        return "Error: Division by zero"

    except Exception:
        return "Error: Invalid expression"
    

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