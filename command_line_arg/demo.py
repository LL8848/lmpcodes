#!/anaconda3/bin/python
import sys,getopt

def usage():
    # print a guide on how to use this code
    print('Usage: '+sys.argv[0]+' -i <file1> [option]')


def main():
    try:
        # read command line args
        # return two elements:
        # "opts" is a list of (option,value) pairs
        # "args" is a list of args left after the option list was stripped
        opts, args = getopt.getopt(sys.argv[1:], "i:ho:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print error and help information and then exit Python:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    # variables to be operated
    input = None
    output = None
    verbose = False

    # o --> option
    # a --> argument passed to the o
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--in"):
            input = a
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"

    if input is None:
        print("Error: not input file given.")
        sys.exit(2)
    if output is None:
        print("Error: not output file specified")
        sys.exit(2)

    print(f"input: {input}")
    print(f"output: {output}")
    # ...


if __name__ == "__main__":
    main()
