
import argparse

def main():
    # Creating a new parser object
    parser = argparse.ArgumentParser(
        description="Mini calculator using argparse."
    )

    parser.add_argument("-a", "--num1", type=float, required=True, help="First number")
    parser.add_argument("-b", "--num2", type=float, required=True, help="Second number")
    parser.add_argument(
        "-o", "--operation",
        choices=["add", "sub", "mul", "div"],
        required=True,
        help="Operation: add, sub, mul, div",
    )
    # parser object : args
    args = parser.parse_args()

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
