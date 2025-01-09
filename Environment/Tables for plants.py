# import libraries

import pandas as pd 
import xarray as xr
import os as os

import hvplot.pandas # noqa: adds hvplot method to pandas objects
import hvplot.xarray # noqa: adds hvplot method to xarray objects

# read in the data

# location of data
fileLoc = 'C:\Data'
fileNames = os.listdir(fileLoc)
fileNames.sort()
#fileNames = [f for f in fileNames if 'md' not in f]
print(fileNames)
# colNames = [c[:-4] for f in fileNames]
os.chdir(fileLoc)

# read the file
df1 = pd.read_csv(fileNames[0],header= 13)
df2 = pd.read_csv(fileNames[1],header= 13)
df3 = pd.read_csv(fileNames[2],header= 13)
df4 = pd.read_csv(fileNames[3],header= 13)
df5 = pd.read_csv(fileNames[4],header= 13)

dflist = (df1, df2, df3, df4, df5)
x=1
threshold = 32
total_reached = []
total_hours = []
years = ["2018","2019","2020","2021","2022"]

for df in dflist:
    df['datetime'] = pd.to_datetime(df['Date/Time'])
    df = df.set_index('datetime')
    df.rename(columns = {'Value':'temperature'},inplace = True)
    df = df.drop(['Unit','Date/Time'],axis = 'columns')

    temp = df['temperature']
    reached = 0.0

    for x in temp:
        if x >= threshold:
            reached += 1
    total_reached.append(reached)
    if x == 1:
        df1 = df
    elif x == 2:
        df2 = df
    elif x == 3:
        df3 = df
    elif x == 4:
        df4 = df
    else:
        df5 = df
    x +=1

for x in total_reached:
    total_hours.append(x*4.5)
    
time = {'Year': years, 'Events reached': total_reached, 'Hours Above or At Threshold': total_hours}
df = pd.DataFrame(time)

print(df)
table = df.hvplot.table(columns=['Year', 'Events reached', 'Hours Above or At Threshold'], sortable=True, selectable=True)
hvplot.save(table, 'table.html')
table