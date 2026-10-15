import math

def get_non_negative_integer(prompt: str) -> int:
    """
    Validates User Input
    :param prompt: Prompt to Display to User
    :return: Integer Input
    """
    while True:
        user_input = input(prompt).strip()

        if user_input.isdigit():
            return int(user_input)

        print("Invalid Input - Enter a Whole Number 0 or Greater")

def calculate_wait_time(needed_resources: dict, production_rates: dict) -> float:
    """
    Calculates the Maximum Hours Needed to Accumulate Missing Resources
    :param needed_resources: The Missing Resources
    :param production_rates: The Production Rates
    :return: Maximum Hours Needed
    """
    max_hours = 0.0

    for resource, missing_amount in needed_resources.items():
        if missing_amount > 0:
            rate = production_rates.get(resource, 0)
            if rate > 0:
                hours = missing_amount / rate
                if hours > max_hours:
                    max_hours = hours
            else:
                return float('inf')

    return max_hours

def format_hours(total_hours: float) -> str:
    """
    Formats a Floating-Point Hour Duration into Hours and Minutes
    :param total_hours: Total Hours to Format
    :return: Formatted String of Hours and Minutes
    """
    if total_hours == float('inf'):
        return "Infinite Time (Production Rate is 0 for a Missing Resource)"

    hours = int(total_hours)
    minutes = math.ceil((total_hours - hours) * 60)

    if minutes == 60:
        hours += 1
        minutes = 0

    return f"{hours} Hours | {minutes} Minutes"