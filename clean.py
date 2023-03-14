import pandas as pd
import os
import sys
import math
import chardet
import numpy as np

ambient_chambers = ["tr_02", "tr_06", "tr_10", "tr_14"]
symmetric_chambers = ["tr_03", "tr_05", "tr_11", "tr_13"]
asymmetric_chambers = ["tr_04", "tr_07", "tr_09", "tr_12"]

symmetric_warming = 3.5
# Using all_temps.csv, Tr_2_4_sp.csv and day_night.csv => all_data_cleaned.py


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

def pivot(fname: str) -> pd.DataFrame:
    """pivots a tab-separated file from long form to wide form
    Args:
        fname (str): Filename of .csv file to be pivoted
    Returns:
        pd.DataFrame: pandas DataFrame
    """
    
    with open(fname, 'rb') as f:
        raw_data = f.read(10000)
        
    
    result = chardet.detect(raw_data)
    enc = result["encoding"]
    
    with open(fname, 'r', encoding=enc) as f:
        first_line = f.readline()
        if ',' in first_line:
            sep = ','
        else:
            sep = '\t'
    
    # Load CSV file (except tableau outputs tab-separated files, so set sep="\t")
    print("Importing {}...".format(fname))
    df = pd.read_csv(fname, index_col = 'Minute of Date And Time', encoding=enc, sep=sep)
    

    # Convert the date/time column (string) to datetime format
    print("Converting string date and time to datetime...")
    df.index = pd.to_datetime(df.index, format='%B %d, %Y at %I:%M %p')
    
    # PIVOT TO WIDE FORM
    print("Creating pivot table...")
    df_wide = df.pivot_table(index='Minute of Date And Time', columns='Chamber', values='Filtered Values')

    # free up some memory, no longer need df
    del df
    
    return df_wide
    

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
        print("No infile1 given")
        return 1

    if len(args) < 2:
        print("No infile2 given")
        return 1

    if (args[0][-4:]) != '.csv' or args[1][-4:] != '.csv':
        print("Invalid file type")
        return 2

    if len(args) < 3:
        outfile = "out.csv"
        
    if len(args) == 3:
        # [0] = infile1
        # [1] = infile2
        # [2] = outfile
        infile1 = args[0]
        infile2 = args[1]
        outfile = args[2]    
    
    try:
        long_file1_stats = os.stat(infile1)
        long_file1_size = long_file1_stats.st_size
    except:
        print("File does not exist")
        return 3
    
    try:
        long_file2_stats = os.stat(infile2)
        long_file2_size = long_file2_stats.st_size
    except:
        print("File does not exist")
        return 3
    
    # pivot the temps
    print("Pivoting {}...".format(infile1))
    all_temps_df = pivot(infile1)
    
    
    # pivot the set-points
    print("Pivoting {}...".format(infile2))
    set_points_df = pivot(infile2)

    # Read in day/night data
    dn_df = pd.read_csv("day_night.csv", index_col='Minute of Date And Time',encoding="utf-16", sep="\t")
    
    # convert day/night string dates to datetimes
    dn_df.index = pd.to_datetime(dn_df.index, format='%B %d, %Y at %I:%M %p')

    # calc the asym set-points
    print("Calculating asymmetric set points...")
    set_points_df['asym_sp'] = round(set_points_df['tr_04'] - set_points_df['tr_02'],2)
    
    # merge asym_sp's to the temps df
    print("Merging set points into temp data...")
    # all_temps_df = pd.merge(all_temps_df, set_points_df[['Minute of Date And Time', 'asym_sp']], on='Minute of Date And Time', how='left')
    all_temps_df = all_temps_df.join(set_points_df['asym_sp'])
    
    # merge day/night data
    all_temps_df = all_temps_df.join(dn_df['Day/Night'])
    
    # Drop rows in which tr_02 is null (since we can't make any comparisons with them)
    all_temps_df = all_temps_df.dropna(subset=['tr_02'])

    # Write out
    print("Writing to '{}'...".format(outfile))
    all_temps_df.to_csv(outfile)
    
    # Get wide file size
    wide_file_stats = os.stat(outfile)
    wide_file_size = wide_file_stats.st_size
        
    print("\nWrite complete")

    return 0

if __name__ == "__main__":
    main()