from datetime import datetime, date

def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(f"Please enter an integer.")

def input_str(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"Please enter not null string.")

def input_date(prompt: str) -> date:
    while True:
        try:
            return datetime.strptime(prompt, "%Y-%m-%d").date()
        except ValueError:
            print(f"Please enter a valid date.")

def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(f"Please enter a valid float.")