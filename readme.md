# Reshaping and Cleaning Tableau Data Export

## Background
One significant hurdle in my particular part of this project was working with the data exported by Tableau.

In order to make comparisons between chambers, our project advisor recommended filtering the appropriate data in Tableau, exporting that data to CSV and analyzing with Excel. 

However, after filtering and exporting the data, I ended up with a fairly large file; >500 MB, for only one year's worth of data. The data also did **not** match the styling I had used in Tableau. 

In Tableau, I set up a worksheet with chambers on the x-axis, datetime minutes on the y-axis and temperature readings as the datapoints for any chamber at a given minute.

![Tableau Worksheert] (/assets/Tableau.png)

![Wide vs Long format](https://www.statology.org/wp-content/uploads/2021/12/wideLong1-1.png)

## How to use