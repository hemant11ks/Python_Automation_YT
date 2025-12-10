"""
==============================================================
Python Scripting & Automation Basics
Using:
    ✔ sys.argv       (Beginner level command-line arguments)
    ✔ argparse       (Professional CLI argument parsing)
    ✔ main() method  (Industry best practice to structure code)
==============================================================
Run Examples:

# --- sys.argv Usage ---
python automation_demo.py Hemant

# --- argparse Usage ---
python automation_demo.py -a 10 -b 5 -o add
python automation_demo.py -a 6 -b 4 -o mul
python automation_demo.py --help    <-- Shows help menu

==============================================================
"""

# --------------------------
# Importing Required Modules
# --------------------------
import sys          # For basic command-line arguments
import argparse     # For advanced professional CLI arguments
import os           # Optional (commonly used in automation scripts)


# -----------------------------------------------------------
# 1. Function using sys.argv (Simple Beginner Level)
# -----------------------------------------------------------
def greet_using_sysargv():
    """
    This function demonstrates how sys.argv works.
    sys.argv is a LIST where:
        sys.argv[0] = script file name
        sys.argv[1] = first argument provided by user
    """

    # Check if user passed at least 1 argument after script name
    if len(sys.argv) < 2:
        print("Usage (sys.argv): python automation_demo.py <your_name>")
        return

    # Accessing argument (always string type)
    name = sys.argv[1]
    print(f"[Using sys.argv] Hello {name}! Welcome to Python Automation.")


# -----------------------------------------------------------
# 2. Function using argparse (Professional CLI Handling)
# -----------------------------------------------------------
def calculate_using_argparse():
    """
    argparse allows building advanced CLI programs with:
        - Short flags (-a) and long flags (--num1)
        - Data type support, validation, help text
        - Default values and restricted choices
    """

    # Create argument parser with description
    parser = argparse.ArgumentParser(
        description="This script performs addition or multiplication using argparse."
    )

    # Adding command-line options
    parser.add_argument("-a", "--num1", type=int, required=True, help="First number")
    parser.add_argument("-b", "--num2", type=int, required=True, help="Second number")

    # choices restricts accepted values, default runs if not passed
    parser.add_argument("-o", "--operation",
                        choices=["add", "mul"], default="add",
                        help="Operation to perform: add/mul (default: add)")

    # Parse arguments
    args = parser.parse_args()

    # Perform desired operation
    if args.operation == "add":
        print(f"[argparse] Addition = {args.num1 + args.num2}")
    else:
        print(f"[argparse] Multiplication = {args.num1 * args.num2}")


# -----------------------------------------------------------
# 3. main() Method — BEST PRACTICE
# -----------------------------------------------------------
def main():
    print("\n================ Automation Demo Script ================\n")

    # --- SYS.ARGV SECTION ---
    # print(">>> Running sys.argv Example:")
    # greet_using_sysargv()


    # If flags (-a/-b) exist → run argparse
    if any(arg in sys.argv for arg in ["-a", "--num1", "-b", "--num2", "-o", "--operation"]):
        calculate_using_argparse()
    else:
        greet_using_sysargv()

    print("\n>>> Run below for argparse examples:")
    print("python automation_demo.py -a 10 -b 5 -o mul")
    print("python automation_demo.py --help")


# -----------------------------------------------------------
# MAIN EXECUTION GUARD
# -----------------------------------------------------------
# Ensures main() runs only when file executed directly,
# not when imported in another script.
if __name__ == "__main__":
    main()
