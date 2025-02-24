# calculate the converged values of the viscosities of NEMD results



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


def main():

    import os
    import sys
    import matplotlib.pyplot as plt

    ff_folder = sys.argv[1]
    T_folder = sys.argv[2]

    rootdir = '/wrk/lnl5/vis_nemd/'
    subdir = ff_folder + '/' + T_folder
    dirlist = ['2e-7','3e-7','4e-7','5e-7','6e-7','7e-7','8e-7','9e-7','10e-7']

    t_a = 15 # average for last t_a (ns)
    timestep = 0.5e-6 # ns
    f_output = 10000 # output frequency, i.e., output every f_output timesteps
    l_a = int(t_a / timestep / f_output) # extrat the data of the last l_a lines

    mylist = []
    templist,sratelist,meanlist,stdevlist = [],[],[],[]
    for dirt in dirlist:
        path = rootdir + subdir + '/' + dirt + '/'
        for filename in os.listdir(path):
            if 'srate' in filename:
                temperature = float(filename[:filename.index('K')])
                srate = float(filename[filename.index('=')+1:filename.rindex('.')])
                with open(path + filename) as file:
                    mylines = file.readlines()[-l_a:]
                    viscosity_list = [float(s.split()[-1]) for s in mylines]
                    mean, stdev = get_mean_std(viscosity_list,5)
                templist.append(temperature)
                sratelist.append(srate*1e15)
                meanlist.append(mean)
                stdevlist.append(stdev)
                mylist.append([temperature,srate*1e15,mean,stdev])
    mylist.sort()

    # plt.plot(sratelist,meanlist,'ro')
    # plt.show()

    # write to file
    fname = rootdir + ff_folder + "/" + str(temperature) + "K.txt"
    with open(fname,'w') as file:
        file.write("Shear rate, Shear viscosity, stdev\r\n") # write long names
        file.write("s^-1, mPa s, mPa s\r\n") # wrtie units
        for lines in mylist:
            file.write("{}\r\n".format(str(lines[1:]).strip('[]')))


if __name__ == "__main__":
    main()
