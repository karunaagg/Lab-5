import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
# from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.tools import google_search




def get_add(a: int, b:int) -> int:
    """Returns the addition of two numbers.

    Args:
        a (int) : The first number of the addition.
        b (int) : The second number of the addition.

    Returns:
        int: return the result of addition.
    """
    return a+b

def get_mul(a: int, b:int) -> int:
    """Returns the multiplication of two numbers.

    Args:
       
        a (int) : The first number of the multiplication.
        b (int) : The second number of the multiplication.

    Returns:
        int: return the result of multiplication.
    """
    return a*b

def get_sub(a: int, b:int) -> int:
    """Returns the substraction of two numbers.

    Args:
       
        a (int) : The first number of the substraction.
        b (int) : The second number of the substraction.

    Returns:
        int: return the result of substraction.
    """
    return a-b


def get_div(a: int, b:int) -> int:
    """Returns the division of two numbers.

    Args:
       
        a (int) : The first number of the division.
        b (int) : The second number of the division.

    Returns:
        int: return the result of division.
    """
    if b == 0:
        return "error"
    else: 
        return a/b



root_agent = Agent(
    name="calculator_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to perform the calculation like a calculator"
    ),
    instruction=(
         "You are a calculator. When the user asks to compute something, "
        "call the 'calculate_or_reject' tool with the expression string, "
        "and return the 'result'. If the tool returns status='error', "
        "say: 'Sorry, I can only help with math problems.'"),
    tools=[get_mul, get_add, get_sub, get_div],
    
)


