#!/share/sw/anaconda3/bin/python

# usage in bash:
# nemd_tplot <ff_folder> <T_folder>

def main():

    import sys
    import os
    import matplotlib.pyplot as plt

    ff_folder = sys.argv[1]
    T_folder = sys.argv[2]

    rootdir = '/wrk/lnl5/vis_nemd/'
    subdir = ff_folder + '/' + T_folder
    # '0.5e-7','0.6e-7','0.7e-7','0.8e-7','0.9e-7','1.0e-7',
    # dirlist = ['2.0e-7','3.0e-7','4.0e-7','5.0e-7','6.0e-7','7.0e-7','8.0e-7','9.0e-7','10.0e-7']
    dirlist = ['2e-7','3e-7','4e-7','5e-7','6e-7','7e-7','8e-7','9e-7','10e-7']
    # dirlist = ['2e-6','3e-6','4e-6','5e-6','6e-6','7e-6','8e-6','9e-6','10e-6']
    # dirlist = ['2.0e-7_2','3.0e-7_2','4.0e-7_2','5.0e-7','6.0e-7','7.0e-7','8.0e-7','9.0e-7','1.0e-6']

    mylist = []
    timestep = 0.5e-6 # unit: ns
    fig, ax = plt.subplots()
    for dirt in dirlist:
        path = rootdir + subdir + '/' + dirt + '/'
        for filename in os.listdir(path):
            if 'srate' in filename:
                with open(path + filename) as file:
                    data = file.readlines()
                    ts = []
                    vis = []
                    for line in data[2:]:
                        ts.append(float(line.split()[0])*timestep)
                        vis.append(float(line.split()[1]))
                    labels = "%.1E" % (float(dirt)*1e15)
                    plt.plot(ts, vis, label = labels)

    #  Location String	Location Code
    # 'best'	0
    # 'upper right'	1
    # 'upper left'	2
    # 'lower left'	3
    # 'lower right'	4
    # 'right'	5
    # 'center left'	6
    # 'center right'	7
    # 'lower center'	8
    # 'upper center'	9
    # 'center'	10

    plt.legend(loc=3, bbox_to_anchor=(0,0),ncol=3, title='shear rates ($\mathregular{s^{-1}}$):',fontsize='x-small',bbox_transform=ax.transAxes)
    plt.xlabel('Time (ns)')
    plt.ylabel('Viscosity (mPa s)')
    plt.text(0.8, 0.2, subdir, horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)

    plt.show()
    #
    # savefig('/wrk/lnl5/vis_nemd/Gromos' + '/timeevolution.jpg')

if __name__ == "__main__":
    main()
