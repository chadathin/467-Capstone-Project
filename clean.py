import pandas as pd
import numpy as np


ambient_chambers = ["tr_02", "tr_06", "tr_10", "tr_14"]
symmetric_chambers = ["tr_03", "tr_05", "tr_11", "tr_13"]
asymmetric_chambers = ["tr_04", "tr_07", "tr_09", "tr_12"]

symmetric_warming = 3.5


def main(filename: str):
    '''
    Takes in a CSV file produced by Tableau
    Pivots from long form to wide form
    Drops columns we don't care about
    Drops rows with incomplete data
    Outputs pivoted data to new CSV file
    '''
    
    # Load CSV file (except tableau outputs tab-separated files, so set sep="\t")
    df = pd.read_csv(filename, index_col = 'Minute of Date And Time', encoding='utf-16', sep="\t")
    
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
    
    print("{:.2f}% incomplete data".format(loss*100))

    # Display the pivoted DataFrame
    print(df_wide)
    
    # Write out
    df_wide.to_csv('out.csv')

    
    return 0

if __name__ == "__main__":
    main('test.csv')