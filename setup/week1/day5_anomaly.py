import pandas as pd

df = pd.read_csv("ev_sessions_raw.csv")
daily = (df.groupby("session_date")
            .agg(sessions=("session_id","nunique"),
                 revenue = ("revenue_gbp","sum"),
                 kwh = ("kwh_delivered","sum"))
            .reset_index())

#add jor below columns into daily
#7-day moving average - each day's "expected" value 
# daily["sessions_ma7"] = round(daily["sessions"].rolling(7).mean(),2) # sum 7day's session / 7
# daily["var_pct"] = ((daily["sessions"]-daily["sessions_ma7"])/daily["sessions_ma7"] *100).round(2)
# daily["anomaly"] = daily["var_pct"].abs() > 20 #abs() no matter +/- , variance more than X count yes

daily["revenue_ma7"] = round(daily["revenue"].rolling(7).mean(),2) # sum 7day's session / 7
daily["var_pct"] = ((daily["revenue"]-daily["revenue_ma7"])/daily["revenue_ma7"] *100).round(2)
daily["anomaly_20"] = daily["var_pct"].abs() > 20 
daily["anomaly_30"] = daily["var_pct"].abs() > 30
daily["anomaly_50"] = daily["var_pct"].abs() > 50 #abs() no matter +/- , variance more than X count yes
#print(daily[daily["anomaly_20"]]) #only show anomaly = true ga WHERE
print(f" over 20 {len(daily[daily["anomaly_20"]])}days")
print(len(daily[daily["anomaly_30"]]))
print(len(daily[daily["anomaly_50"]]))




#just variable, will not add into daily
ma7 =  round(daily["sessions"].rolling(7).mean(),2) 
#print(ma7)