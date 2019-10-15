import sys
import pandas as pd
import matplotlib.pyplot as plt
from linecache import getline

def main():
    filename = sys.argv[1]

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
        y = colnames[1]
        plt.plot(df[x],df[y])
        plt.xlabel(x)
        plt.ylabel(y)    
        plt.title(y)
    # more than 1 variant -> plot multiple figs by subplots
    else:
        figw = 4
        figh = figw * fignum * 0.75
        fig, ax = plt.subplots(fignum,sharex=True,figsize=(figw,figh))
        for axi,y in zip(ax.flat,colnames[1:]):
            axi.plot(df[x],df[y])
            axi.title.set_text(y)
    #         axi.set_xlabel(x)
            axi.set_ylabel(y)
        plt.xlabel(x)

    plt.show()


if __name__ == "__main__":
    main()