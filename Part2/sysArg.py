# calc_sysargv_simple.py
# Mini calculator using sys.argv
# Usage:
#   python calc_sysargv_simple.py <num1> <num2> <operation>
# Example:
#   python calc_sysargv_simple.py 10 5 add

import sys

# We need exactly 3 extra arguments: num1, num2, operation
if len(sys.argv) != 4:
    print("Usage: python calc_sysargv_simple.py <num1> <num2> <operation>")
    print("operation: add, sub, mul, div")
    sys.exit(1)

# Get values from the list (all are strings)
num1_str = sys.argv[1]
num2_str = sys.argv[2]
op = sys.argv[3]

# Convert numbers
try:
    num1 = float(num1_str)
    num2 = float(num2_str)
except ValueError:
    print("Error: num1 and num2 must be numbers.")
    sys.exit(1)

# Do the operation
if op == "add":
    result = num1 + num2
elif op == "sub":
    result = num1 - num2
elif op == "mul":
    result = num1 * num2
elif op == "div":
    if num2 == 0:
        print("Error: Cannot divide by zero.")
        sys.exit(1)
    result = num1 / num2
else:
    print("Error: operation must be: add, sub, mul, div")
    sys.exit(1)

print(f"[sys.argv] Result = {result}")
