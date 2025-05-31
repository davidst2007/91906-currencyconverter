"""Simple converting and rounding function."""

# This is intended to be imported into main file.

def convert_round_4dp(value, multiplier):
    """Simple converting and rounding function."""
    answer = round((value * multiplier), 4)
    if answer <= 0:
        return "Less than 0.0001"
    else:
        return answer