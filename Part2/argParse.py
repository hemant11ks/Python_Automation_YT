# calc_argparse_simple.py
# Mini calculator using argparse (best for real projects)
# Usage:
#   python calc_argparse_simple.py -a 10 -b 5 -o add
#   python calc_argparse_simple.py --num1 10 --num2 5 --operation mul

import argparse

def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Mini calculator using argparse."
    )

    # Add arguments
    parser.add_argument("-a", "--num1", type=float, required=True, help="First number")
    parser.add_argument("-b", "--num2", type=float, required=True, help="Second number")
    parser.add_argument(
        "-o", "--operation",
        choices=["add", "sub", "mul", "div"],
        required=True,
        help="Operation: add, sub, mul, div",
    )

    # Parse them
    args = parser.parse_args()

    # Do the operation
    if args.operation == "add":
        result = args.num1 + args.num2
    elif args.operation == "sub":
        result = args.num1 - args.num2
    elif args.operation == "mul":
        result = args.num1 * args.num2
    elif args.operation == "div":
        if args.num2 == 0:
            print("Error: Cannot divide by zero.")
            return
        result = args.num1 / args.num2

    print(f"[argparse] Result = {result}")

if __name__ == "__main__":
    main()
