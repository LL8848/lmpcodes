#!/share/sw/anaconda3/bin/python
__author__ = 'Lingnan Lin'

import sys,getopt

def usage():
    # print a guide on how to use this script
    print("Usage: plot_out [option] <argument>\n")
    print("Options:")
    print("-h              : print this help message and exit (also --help)")
    print("-i   <filename> : specify the input file name to the program")
    print("-s              : calculate block average and error (also --stat)")
    print("-a              : perform average calculation for each variant (also avg)")

def get_mean_std(data,n_b):

    import statistics

    # n_b: number of chunks(or blocks) to divide
    n_e = int(len(data)/n_b)
#     print("n_e = {}".format(n_e))
    # list of chunks
    final = [data[i * n_e:(i + 1) * n_e] for i in range((len(data) + n_e - 1) // n_e )]

    # get a list of mean of each chunk
    stat = [statistics.mean(chunk) for chunk in final]

    # calculate the mean and standard deviation of the chunks
    return statistics.mean(stat), statistics.stdev(stat)


def rave(mylist):

    # calculate running average
    sum = 0
    rave = []
    for i, x in enumerate(mylist,1):

        sum += x
        rave.append(sum / i)

    return rave


def linearfit(x,y):

    from scipy.stats import linregress
    slope, intercept, r_value, p_value, std_err = linregress(x,y)

    return slope, intercept


def plot_out(filename,dt,if_stat,if_ave,if_fit):

    import pandas as pd
    import matplotlib.pyplot as plt
    from linecache import getline
    from statistics import mean

    line = getline(filename,2)   # read a specific line of a file
    colnames = line.strip('#').split()  # .strip() automatically strips whitespace
                                        # inluding ' ' and \n' etc

    df = pd.read_csv(filename,delimiter = ' ',
                     comment='#',
                     names = colnames,header = None)

    # if the flag "if_stat" is True, then calculate the block average and confidence interval for each column
    if if_stat:
        Nblocks = 10
        print("statistics:")
        print("number of blocks: {}".format(Nblocks))
        print("                    average, 95% confidence interval")
        for y in colnames[1:]:
            ave, std = get_mean_std(df[y],Nblocks)
            err = std * 1.96 # 95% confidence interval
            print("{0:10s}:{1:16.5f}, {2:16.5f}".format(y,ave,err))

    # if the flag "if_ave" is True, then calculate the average for each column
    if if_ave:
        print("simple averages:")
        for y in colnames[1:]:
            ave = mean(df[y])
            print("{0:15s} | {1:16.5f}".format(y,ave))


    # make plots

    fignum = len(colnames)-1

    # set the first colomn as x
    x = colnames[0]

    # change "Timestep" to "Time [ns]"
    if colnames[0] == "TimeStep":
        x = 'Time'
        unitx = "ns"
        df.rename(columns={"TimeStep":"Time"},inplace=True)
        df[x] = df[x] * dt / 1000000 # convert to ns

    # only 1 variant -> plot 1 fig
    if fignum == 1:
        plt.subplots()
        y = colnames[1]
        plt.plot(df[x],df[y],color='blue',linewidth=0.5,label="average for one window")
        plt.plot(df[x],rave(df[y]),color='red',linewidth=2,label="running average")
        if if_fit:
            slope, intercept = linearfit(df[x],df[y])
            plt.plot(df[x],slope*df[x]+intercept,color='black',linewidth=2,label="linear fit")
            drift = slope * (df[x].iloc[-1] - df[x].iloc[0])
            meany = slope * (df[x].iloc[-1] + df[x].iloc[0]) / 2 + intercept
            print("Estimated Drift: {0:4.2f} %".format(drift/meany*100))
        # ax.set_xlabel(x)
        # ax.set_ylabel(y)
        # title.set_text(y)
        plt.xlabel(x + " [" + unitx + "]")
        plt.ylabel(y)
        plt.legend()
        plt.show()

    # more than 1 variant -> plot multiple figs by subplots
    else:
        figw = 4
        figh = figw * fignum * 0.75
        fig, ax = plt.subplots(fignum,sharex=True,figsize=(figw,figh))
        for axi,y in zip(ax.flat,colnames[1:]):
            axi.plot(df[x],df[y],color='blue',linewidth=1)
            axi.plot(df[x],rave(df[y]),color='red',linewidth=2)
            if if_fit:
                slope, intercept = linearfit(df[x],df[y])
                axi.plot(df[x],slope*df[x]+intercept,color='black',linewidth=2)
                drift = slope * (df[x].iloc[-1] - df[x].iloc[0])
                meany = slope * (df[x].iloc[-1] + df[x].iloc[0]) / 2 + intercept
                print("Estimated Drift of {0:10s}: {1:4.2f} %".format(y,drift/meany*100))
            axi.title.set_text(y)
    #         axi.set_xlabel(x)
            axi.set_ylabel(y)
        plt.xlabel(x + " [" + unitx + "]")
        plt.show()





def main():
    try:
        # read command line args
        # return two elements:
        # "opts" is a list of (option,value) pairs
        # "args" is a list of args left after the option list was stripped
        opts, args = getopt.getopt(sys.argv[1:], "i:d:hsaf",
            ["help","dt","stat","avg","fit"])
    except getopt.GetoptError as err:
        # print error and help information and then exit Python:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    # variables to be operated
    # genneraly, the variable is a file name or a flag.
    input = None
    dt = 0.5 # timestep [fs]
    if_stat = False # flag for statistics
    if_ave = False # flag for simple average
    if_fit = False

    # o --> option
    # a --> argument passed to the o
    for o, a in opts:
        if o in ("-i", "--in"):
            input = a
        elif o in ("-d","--dt"):
            dt = float(a)
        elif o in ("-f","--fit"):
            if_fit = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--stat"):
            if_stat = True
        elif o in ("-a", "--avg"):
            if_ave = True
        else:
            assert False, "unhandled option"

    if input is None:
        print("Error: not input file given.")
        sys.exit(2)

    plot_out(input,dt,if_stat,if_ave,if_fit)


if __name__ == "__main__":
    main()
