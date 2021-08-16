import pandas as pd
import datetime as dt
from dateutil.parser import parse
import numpy as np

to_drop = '''Favorite
Calories
Training Stress Score®
Avg HR
Max HR
Aerobic TE
Avg Run Cadence
Max Run Cadence
Avg Pace
Best Pace
Elev Loss
Avg Stride Length
Avg Vertical Ratio
Avg Vertical Oscillation
Avg Ground Contact Time
Avg GCT Balance
Grit
Flow
Dive Time
Min Temp
Surface Interval
Decompression
Best Lap Time
Number of Laps
Max Temp
Avg Resp
Min Resp
Max Resp
Moving Time
Elapsed Time
Min Elevation
Max Elevation'''.split("\n")



df = pd.read_csv("~/Downloads/Activities (3).csv").drop(to_drop, axis=1)
df = df[df["Date"] > "2021-07-01"]
df["Date"] = df["Date"].apply(parse)
df["Track Adjusted"] = df.loc[df['Activity Type'] == "Track Running", 'Distance'].apply(lambda x: float(float(x.replace(",","")) / 1609))
df["Distance"] = df["Distance"].apply(lambda x: float(float(x.replace(",",""))))
df.loc[df['Track Adjusted'].isna(), 'Track Adjusted'] = 99999
df["Distance"] = df[["Distance", "Track Adjusted"]].agg("min", axis="columns")
df = df.drop(["Track Adjusted"], axis = 1)

oneDays = df.groupby(pd.Grouper(key='Date', freq='1D')).sum()[['Distance']].sort_index()
twoDays = df.groupby(pd.Grouper(key='Date', freq='2D')).sum()[['Distance']].sort_index()
threeDays = df.groupby(pd.Grouper(key='Date', freq='3D')).sum()[['Distance']].sort_index()
sevenDays = df.groupby(pd.Grouper(key='Date', freq='7D')).sum()[['Distance']].sort_index()
eightDays = df.groupby(pd.Grouper(key='Date', freq='8D')).sum()[['Distance']].sort_index()
nineDays = df.groupby(pd.Grouper(key='Date', freq='9D')).sum()[['Distance']].sort_index()
tenDays = df.groupby(pd.Grouper(key='Date', freq='10D')).sum()[['Distance']].sort_index()
elevenDays = df.groupby(pd.Grouper(key='Date', freq='11D')).sum()[['Distance']].sort_index()

import matplotlib.pyplot as plt
plt.close("all")
plt.figure();


ax = pd.DataFrame(twoDays).plot()
pd.DataFrame(threeDays).plot(ax=ax)
pd.DataFrame(sevenDays).plot(ax=ax)
pd.DataFrame(eightDays).plot(ax=ax)
pd.DataFrame(nineDays).plot(ax=ax)
pd.DataFrame(tenDays).plot(ax=ax)
pd.DataFrame(elevenDays).plot(ax=ax)
ax.set_title("Distance over Different Cycle Lengths")
ax.set_xlabel("Date")
ax.set_ylabel("Distance (miles)")
ax.legend(["two day cycle", "three day cycle", "seven day cycle", "eight day cycle", "nine day cycle","ten day cycle", "elevent day cycle"])
plt.savefig("Running_Cycles.png")
# easy, workout, rest template
# x x x x x x x x x
# 1 2 0 1 2 0 1 2 0

# workout easy workout rest template
# x x x x x x x x x
# 1 2 0 1 2 0 1 1 1

# max_two = # average of the maximum two from the previous cycle

#max_two = nineDays["Distance"][-2] / 3
#max_three = nineDays["Distance"][-2] / 2

# the trick is that I want the combination that create the largest load for two/three day counts to see what I should probably be doing.
# I can use this with the normal mileage recommendations to decide on what to do.
