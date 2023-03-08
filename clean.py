import pandas as pd
import os
import sys
import math
import numpy as np

ambient_chambers = ["tr_02", "tr_06", "tr_10", "tr_14"]
symmetric_chambers = ["tr_03", "tr_05", "tr_11", "tr_13"]
asymmetric_chambers = ["tr_04", "tr_07", "tr_09", "tr_12"]

symmetric_warming = 3.5

# Found this conversion function on StackOverflow
# https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def main():
    '''
    Takes in a CSV file produced by Tableau
    Pivots from long form to wide form
    Drops columns (chambers) we don't care about
    Drops rows with incomplete data
    Outputs pivoted data to new CSV file
    '''
    args = sys.argv[1:]
    if len(args) == 0:
        print("No filename given")
        return 1

    if (args[0][-4:]) != '.csv':
        print("Invalid file type")
        return 2
    
    try:
        long_file_stats = os.stat(args[0])
        long_file_size = long_file_stats.st_size
    except:
        print("File does not exist")
        return 3
    
    # Load CSV file (except tableau outputs tab-separated files, so set sep="\t")
    df = pd.read_csv(args[0], index_col = 'Minute of Date And Time', encoding='utf-16', sep="\t")
    
    # Sanity check
    print(df)
    
    # Convert the date/time column (string) to datetime format
    df.index = pd.to_datetime(df.index, format='%B %d, %Y at %I:%M %p')
    
    # PIVOT TO WIDE FORM
    df_wide = df.pivot_table(index='Minute of Date And Time', columns='Chamber', values='Filtered Values')
    
    # free up some memory, no longer need df
    del df
    
    # Drop columns we don't care about (in this case, the asymmetric cols 4, 7, 9, 12)
    df_wide = df_wide.drop(asymmetric_chambers, axis=1)
    
    # How many rows before dropping incomplete data
    before = len(df_wide)
    
    # Drop incomplete rows
    df_wide = df_wide.dropna()
    
    # Rows left after dropping incomplete data
    after = len(df_wide)

    # Per cent loss of data
    loss = abs((after - before))/before
    
    # Display the pivoted DataFrame
    print(df_wide)
    
    # Write out
    df_wide.to_csv('out.csv')
    
    # Get wide file size
    wide_file_stats = os.stat('out.csv')
    wide_file_size = wide_file_stats.st_size
    
    # Print summary
    print("\nWrite complete")
    print("Long file size: {}".format(convert_size(long_file_size)))
    print("Wide file size: {}".format(convert_size(wide_file_size)))
    print("Percent rows dropped (incomplete data): {:.2f}%".format(loss*100))

    
    return 0

if __name__ == "__main__":
    main()