import sys 
import getopt 

# sys.argv[1:] : skip the script name
# "f:o:" : short options string 
# ["file=", "output="] : long options   
try:

    opts, args = getopt.getopt(sys.argv[1:], "f:o:", ["file=", "output="])
    # file= : there is a option --file it required an argument
    # output= : there is a option --output it required an argument

except getopt.GetoptError:
    print("Usage: python get_opt.py -f <file> -o <output>")
    sys.exit(1)


# iterate over loop
for opt, arg in opts:
    if opt in ("-f", "--file"):
        file = arg
        print(f"File: {file}")
    elif opt in ("-o", "--output"):
        output = arg
        print(f"Output: {output}")

