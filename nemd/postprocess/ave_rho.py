#!/share/sw/anaconda3/bin/python

__author__ = 'Lingnan Lin'

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
    import sys
    import pandas as pd
    filename = sys.argv[1]
    df = pd.read_csv(filename,
                     delimiter = ' ',
                     comment='#',
                     names = ['step','v_rho'],
                     header = None)
    ave, std = get_mean_std(df['v_rho'],10)
    err = std * 1.96 # 95% confidence interval
    
    print(f"average density: {ave}"