import pandas as pd
df=pd.read_csv("islamabad_pm25.csv.csv",skiprows=2) #Starts from rows after longitude and latitude
print(df.head())
NoRow,NoCol=df.shape
print("Total Rows: ",NoRow)
print("Total Columns: ",NoCol)
print(df.isnull().sum()) #Counts any missing values
df["time"]=pd.to_datetime(df["time"])
df=df.rename(columns={"pm2_5 (μg/m³)": "pm25"}) #Renamed PM2.5 Column
df["date"]=df["time"].dt.date
daily=df.groupby("date",as_index=False)["pm25"].mean()
print(daily.head())
print("Total days: ",len(daily))
daily.to_csv("daily_pollution.csv",index=False) #saving daily dataset without adding additional rows


