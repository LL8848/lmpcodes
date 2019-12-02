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

    t_a = 10 # average for last t_a (ns)
    timestep = 0.5e-6 # ns
    f_output = 100000 # output frequency, i.e., output every f_output timesteps
    l_a = int(t_a / timestep / f_output) # extract the data of the last l_a lines


    for dirt in dirlist:
        timestep_list,viscosity_list = [],[]
         # get data before restart
        path_0 = rootdir + subdir + '/' + dirt + '/'
        for filename in os.listdir(path_0):
            if 'srate' in filename:
                temperature = float(filename[:filename.index('K')])
                srate = float(filename[filename.index('=')+1:filename.rindex('.')])
                with open(path_0 + filename) as file:
                    mylines = file.readlines()
                    for s in mylines[2:]:
                        timestep_list.append(int(s.split()[0]))
                        viscosity_list.append(float(s.split()[1]))
        last_timestep = timestep_list[-1] # last time step before restart

        # get restart data
        path_r = rootdir + subdir + '/' + dirt + '_2/'
        for filename in os.listdir(path_r):
            if 'srate' in filename:
                temperature = float(filename[:filename.index('K')])
                srate = float(filename[filename.index('=')+1:filename.rindex('.')])
                with open(path_r + filename) as file:
                    mylines_r = file.readlines()
                    for s in mylines_r[2:]:
                        ts = int(s.split()[0])
                        eta = float(s.split()[1])
                        if ts > last_timestep:
                            timestep_list.append(ts)
                            viscosity_list.append(eta)

        with open(path_r+'catresult.txt','w') as file:
            file.write('# Time-averaged data for fix viscave\n')
            file.write('# TimeStep v_visc\n')
            for ts,eta in zip(timestep_list,viscosity_list):
                file.write("{} {}\r\n".format(ts,eta))


if __name__ == "__main__":
    main()
