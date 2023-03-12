# Reshaping and Cleaning Tableau Data Export

## What this program does
This is a fairly simple program that performs the following:
- ingests two CSV files exported by Tablueau
    - One containing the temperature data
    - One containing the set-point data
- reshapes each from long to wide format with chambers on the x-axis
- converts string dates/times to datetime format
- joints the two tables so the temperature table also contains the asymmetric setpoint data
- drops rows in which Tr_02 contains a Null value
    - Can't make comparisons with them, anyway
- writes the new dataframe to a CSV

## How to use

Simply place this program in the same directory as your Tableau export and run: 

```
python clean.py [filename1].csv [filename2].csv [output].csv
```

replacing bracketed items with your file names. The filenames must end in `.csv`

If you are missing dependencies, simply run 

```
pip install -r requirements.txt
```

## Caveats
This program is intended for use with time series datasets in which the user would like the datetime to be on the y-axis. Additionally, in my case the program was written to handle minute-by-minute data. You may need to modify, or eliminate, lines 49-54 to suit your particular needs:

```py
# Load CSV file (except tableau outputs tab-separated files, so set sep="\t")
print("Importing {}...".format(fname))
df = pd.read_csv(fname, index_col = 'Minute of Date And Time', encoding=enc, sep=sep)

# Convert the date/time column (string) to datetime format
print("Converting string date and time to datetime...")
df.index = pd.to_datetime(df.index, format='%B %d, %Y at %I:%M %p')
```

## Background (in case you're curious)
One significant hurdle in my particular part of this project was working with the data exported by Tableau.

In order to make comparisons between chambers, our project advisor recommended filtering the appropriate data in Tableau, exporting that data to CSV and analyzing with Excel. 

In Tableau, I set up a worksheet with chambers on the x-axis, datetime minutes on the y-axis and temperature readings as the datapoints for any chamber at a given minute.

![Tableau worksheet](/assets/Tableau.png)

When I went to export the data, that formatting was lost. Every single reading had its own row with a chamber and time. In other words, instead of the output looking like this:

![Expected output](/assets/wide_ouput.png)

It looked more like this:

![Long output](/assets/Tableau%20Export.png)

As you can imagine, this created **many** redundancies in the number of chambers (same chamber listed in numerous rows) and date/times (same time listed in numerous rows). This made the file very large (>500 MB for a single year) and very long. When I tried to open it in LibreOffice Calc, I recieved this error:

![Too many rows](/assets/Too%20many%20rows.png)

After doing some asking around in the Tableau community, I was guided to a [great article](https://www.statology.org/long-vs-wide-data/) on "Long" vs. "Wide" formats. 

To briefly summarize: 
- A wide format contains values that do not repeat in the first column.
- A long format contains values that do repeat in the first column.

Take the two datasets below, both featuring the same data but in different formats (pulled form article linked above):
![Wide vs Long format](/assets/wideLong1-1.png)

Wide formats tend to be best for analysis, since a user can easily make calculations across rows, or down columns.

Long formats tend to be best for visualizations. Therefore, Tableau converts wide data to long data which is what I was getting when I exported the data set. Luckily, reshaping the data back to wide was primarily a matter of creating a pivot table.

Typically, I would do this in Excel/Calc, but since the file was too big, I had to rely on Python and and Pandas library to handle such a large file.