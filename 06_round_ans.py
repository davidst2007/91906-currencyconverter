def convert_round_4dp(value, multiplier):
    answer = round((value * multiplier), 4)
    if answer <= 0:
        return "Less than 0.0001"
    else:
        return answer

print(convert_round_4dp(10, 0.000029))