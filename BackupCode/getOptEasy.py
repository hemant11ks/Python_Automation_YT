import sys  # Used to access command line arguments (sys.argv) and exit the program
import getopt  # Used to parse the flags/options


# Using Short flags: python script.py -f input.txt -o output.txt
# Using Long flags: python script.py --file input.txt --output output.txt

try: 
    # --- THE PARSING LINE ---
    # 1. sys.argv[1:]: We take the input list but skip the script name.
    # 2. "f:o:": These are SHORT options. 
    #    - 'f:' means -f requires a value.
    #    - 'o:' means -o requires a value.
    # 3. ["file=", "output="]: These are LONG options.
    #    - 'file=' means --file requires a value (indicated by the '=').
    #    - 'output=' means --output requires a value.
    
    opts, args = getopt.getopt(sys.argv[1:], "f:o:", ["file=", "output="])
    
    # 'opts' will be a list of pairs found, e.g., [('--file', 'data.txt'), ('-o', 'result.txt')]
    # 'args' will contain any leftover words that weren't flags.

except getopt.GetoptError as err: 
    # This block runs if the user makes a syntax mistake (e.g., forgets a filename)
    print(f"Error: {err}") 
    sys.exit(1)  # Stop the program with an error code

# Loop through the options that were found
for opt, arg in opts: 
    
    # Check if the option is either the short version (-f) OR the long version (--file)
    if opt in ("-f", "--file"): 
        print(f"Input file: {arg}") 
        
    # Check if the option is either the short version (-o) OR the long version (--output)
    elif opt in ("-o", "--output"): 
        print(f"Output file: {arg}")
