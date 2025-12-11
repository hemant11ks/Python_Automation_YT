import sys  # Module to handle command line arguments

if len(sys.argv) != 4:
    print("Usage: python argv.py <num1> <num2> <operation>")
    sys.exit(1)

num1_str = sys.argv[1]
num2_str = sys.argv[2]
operation = sys.argv[3]

# Converting the values
num1 = int(num1_str)
num2 = int(num2_str)
# num1 = num1_str
# num2 = num2_str

if operation == "add":
    result = num1 + num2
elif operation == "sub":
    result = num1 - num2
elif operation == "mul":
    result = num1 * num2
elif operation == "div":
    result = num1 / num2
else:
    print("Invalid operation")
    sys.exit(1)

print(f"Result: {result}")

