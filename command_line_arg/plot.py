#!/anaconda3/bin/python
__author__ = 'Lingnan Lin'

import sys,getopt

def usage():
    # print a guide on how to use this script
    print("Usage: python plot.py -i <filename>")


def plot_out(filename):
    import pandas as pd
    import matplotlib.pyplot as plt
    from linecache import getline
    line = getline(filename,2)   # read a specific line of a file
    colnames = line.strip('#').split()  # .strip() automatically strips whitespace
                                        # inluding ' ' and \n' etc

    df = pd.read_csv(filename,delimiter = ' ',
                     comment='#',
                     names = colnames,header = None)

    # make plots

    fignum = len(colnames)-1

    # set the first colomn as x
    x = colnames[0]

    # only 1 variant -> plot 1 fig
    if fignum == 1:
        plt.subplots()
        y = colnames[1]
        plt.plot(df[x],df[y])
        # ax.set_xlabel(x)
        # ax.set_ylabel(y)
        # title.set_text(y)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    # more than 1 variant -> plot multiple figs by subplots
    else:
        figw = 4
        figh = figw * fignum * 0.75
        fig, ax = plt.subplots(fignum,sharex=True,constrained_layout=True,figsize=(figw,figh))
        for axi,y in zip(ax.flat,colnames[1:]):
            axi.plot(df[x],df[y])
            axi.title.set_text(y)
    #         axi.set_xlabel(x)
            axi.set_ylabel(y)
        plt.xlabel(x)


def main():
    try:
        # read command line args
        # return two elements:
        # "opts" is a list of (option,value) pairs
        # "args" is a list of args left after the option list was stripped
        opts, args = getopt.getopt(sys.argv[1:], "i:h", ["help"])
    except getopt.GetoptError as err:
        # print error and help information and then exit Python:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    # variables to be operated
    # genneraly, the variable is a file name or a flag.
    input = None

    # o --> option
    # a --> argument passed to the o
    for o, a in opts:
        if o in ("-i", "--in"):
            input = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    if input is None:
        print("Error: not input file given.")
        sys.exit(2)

    plot_out(input)


if __name__ == "__main__":
    main()
