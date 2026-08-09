from typing import TypedDict

from langgraph.graph import StateGraph, END

from tools.tools import (
    text_processor,
    calculator,
    calculator_simple,
    weather_mock,
)


class AgentState(TypedDict):
    task: str
    tool: str
    result: str
    steps: list


# ------------------------------------------------
# Router
# ------------------------------------------------

def router(state: AgentState):

    task = state["task"].lower()

    # Weather
    if any(word in task for word in [
        "weather",
        "temperature",
        "forecast"
    ]):
        return "weather"

    # Text
    if any(word in task for word in [
        "uppercase",
        "lowercase",
        "word count",
        "character count",
        "reverse"
    ]):
        return "text"

    # Calculator
    if any(word in task for word in [
        "calculate",
        "add",
        "subtract",
        "multiply",
        "divide",
        "+",
        "-",
        "*",
        "/"
    ]):
        return "calculator"

    raise ValueError(
        "Unable to determine the appropriate tool"
    )


# ------------------------------------------------
# Text node
# ------------------------------------------------

def text_node(state: AgentState):

    task = state["task"].lower()

    if "uppercase" in task:
        operation = "uppercase"

    elif "lowercase" in task:
        operation = "lowercase"

    elif "word count" in task:
        operation = "word_count"

    elif "character count" in task:
        operation = "character_count"

    elif "reverse" in task:
        operation = "reverse"

    else:
        operation = "uppercase"

    # Extract text after operation
    text = state["task"]

    for keyword in [
        "uppercase",
        "lowercase",
        "word count",
        "character count",
        "reverse"
    ]:
        text = text.lower().replace(keyword, "")

    text = text.replace("convert", "")
    text = text.replace("to", "")
    text = text.strip()

    result = text_processor.invoke({
        "text": text,
        "operation": operation
    })

    return {
        "tool": "TextProcessorTool",
        "result": result,
        "steps": state["steps"] + [
            {
                "step": "TextProcessorTool",
                "input": text,
                "output": result
            }
        ]
    }


# ------------------------------------------------
# Calculator node
# ------------------------------------------------

def calculator_node(state: AgentState):

    task = state["task"]

    # Extract expression from common wording
    expression = (
        task.lower()
        .replace("calculate", "")
        .replace("what is", "")
        .strip()
    )

    result = calculator_simple.invoke({
        "expression": expression
    })

    return {
        "tool": "CalculatorTool",
        "result": result,
        "steps": state["steps"] + [
            {
                "step": "CalculatorTool",
                "input": expression,
                "output": result
            }
        ]
    }


# ------------------------------------------------
# Weather node
# ------------------------------------------------

def weather_node(state: AgentState):

    task = state["task"]

    city = (
        task.lower()
        .replace("what is the weather in", "")
        .replace("weather in", "")
        .replace("weather", "")
        .replace("temperature in", "")
        .strip()
    )

    result = weather_mock.invoke({
        "city": city
    })

    return {
        "tool": "WeatherMockTool",
        "result": result,
        "steps": state["steps"] + [
            {
                "step": "WeatherMockTool",
                "input": city,
                "output": result
            }
        ]
    }


# ------------------------------------------------
# Build Graph
# ------------------------------------------------

workflow = StateGraph(AgentState)

workflow.add_node("text", text_node)
workflow.add_node("calculator", calculator_node)
workflow.add_node("weather", weather_node)


workflow.add_conditional_edges(
    "__start__",
    router,
    {
        "text": "text",
        "calculator": "calculator",
        "weather": "weather",
    }
)


workflow.add_edge("text", END)
workflow.add_edge("calculator", END)
workflow.add_edge("weather", END)


agent = workflow.compile()