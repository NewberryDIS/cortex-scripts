import pandas as pd
import os

directory = r'../csv_batches/'
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        basename = filename.strip('.csv')
        for i,chunk in enumerate(pd.read_csv(filename, chunksize=2500)):
            chunk.to_csv('./splits/' + basename + '_chunk_{}.csv'.format(i), index=False)
