# 'sys' is the "System" module.
# We need it for two main reasons:
# 1. sys.argv: To access the list of arguments typed in the command line.
# 2. sys.exit(): To stop the program immediately (e.g., if an error occurs).
import sys

# 'getopt' is a module for "Get Options".
# It helps parse command-line flags (like -a, -b, -o).
# It separates the flags (options) from the actual values.
import getopt

def print_usage():
    """Helper function to show the user how to run the program properly."""
    print("Usage: python calc_getopt_simple.py -a <num1> -b <num2> -o <operation>")
    print("operation: add, sub, mul, div")

def main():
    # Initialize variables to None so we can check later if they were actually set.
    num1 = None
    num2 = None
    op = None

    try:
        # --- THE CORE PART: sys.argv and getopt ---
        
        # sys.argv is a list of everything typed in the command line.
        # sys.argv[0] is the script name itself ('calc_getopt_simple.py').
        # sys.argv[1:] is everything AFTER the script name (the actual flags and numbers).
        
        # "a:b:o:h" is the rule string:
        # - 'a:' means look for '-a' and it MUST be followed by a value (because of the colon).
        # - 'b:' means look for '-b' and it MUST be followed by a value.
        # - 'o:' means look for '-o' and it MUST be followed by a value.
        # - 'h'  means look for '-h', but it does NOT take a value (no colon).
        
        opts, _ = getopt.getopt(sys.argv[1:], "a:b:o:h")
        
        # 'opts' is now a list of pairs, e.g., [('-a', '10'), ('-b', '5'), ('-o', 'add')]
        
    except getopt.GetoptError as err:
        # This block runs if the user types a flag we didn't define (like -z)
        # or forgets a required value (like typing -a without a number).
        print("Error:", err)
        print_usage()
        sys.exit(1) # Exit with code 1 to indicate an error occurred.

    # Loop through the parsed options to assign values to variables
    for opt, val in opts:
        if opt == "-h":
            print_usage()
            sys.exit(0) # Exit with code 0 (Success) because the user just asked for help.
        elif opt == "-a":
            num1 = val # 'val' is the value found after -a
        elif opt == "-b":
            num2 = val # 'val' is the value found after -b
        elif opt == "-o":
            op = val   # 'val' is the value found after -o

    # Check that the user actually provided all three required flags
    if num1 is None or num2 is None or op is None:
        print("Error: -a, -b and -o are required.")
        print_usage()
        sys.exit(1)

    # Convert the input strings to numbers (floats)
    try:
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        # This catches errors if the user typed text instead of numbers (e.g., -a "hello")
        print("Error: num1 and num2 must be numbers.")
        sys.exit(1)

    # Perform the requested math operation
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
        # Handle the case where the user typed an unknown operation (e.g., -o "power")
        print("Error: operation must be: add, sub, mul, div")
        sys.exit(1)

    # Print the final result
    print(f"[getopt] Result = {result}")

if __name__ == "__main__":
    main()