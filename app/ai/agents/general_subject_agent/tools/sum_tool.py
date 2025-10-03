from langchain_core.tools import tool


@tool
def sum_tool(arg1: float, arg2: float) -> float:
    """
    Tool useful to sum two numbers

    Parameters:

    arg1: The first float to be summed
    arg2: The second float to be summed

    Return:
    This fuction return the total
    """
    print("===============SUM_TOOL=============")
    return float(arg1) + float(arg2)
