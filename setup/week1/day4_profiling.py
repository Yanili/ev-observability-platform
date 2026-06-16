import pandas as pd

df = pd.read_csv("ev_sessions_raw.csv")

#print(df.shape) # (rows, columns)
#print(df.head(10)) #select top 10*
#print(df.describe()) #instant statistical profile
#print(df.dtypes) #schema check - are dates really dates?

#The SQL you already know, translated:
df[df["city"] == "London"] # where
df.groupby("city")["revenue_gbp"].sum() #groupby
df.sort_values("kwh_delivered",ascending=False) #order by ...desc
df["session_id"].nunique() #count(distinct)

print(len(df)) #count
print(df["session_id"].nunique()) #distin count
print(df.isna().sum()) # to see which columns has NULL 
print(df[df["revenue_gbp"]<0]) # to see how many rows/record had negative £
print(df[df["session_date"]>"2026-06-13"]) 
print(df["charger_status"].value_counts()) #count by status
print(df.groupby("session_date").size().plot())

