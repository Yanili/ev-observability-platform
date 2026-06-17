import pandas as pd

df = pd.read_csv("ev_sessions_raw.csv")
#print(df.head(10))
#print((df["charger_status"] == "failed").sum()) 

daily_metrics = (df.groupby("session_date")
                   .agg(session = ("session_id","nunique"),
                        revenue = ("revenue_gbp","sum"),
                        kwh    = ("kwh_delivered","sum"))
                        .reset_index())

daily_metrics["failure_rate"] = ((df["charger_status"] == "failed").sum() /daily_metrics["session"] * 100).round(2)
daily_metrics["ma7_session"] = round(daily_metrics["session"].rolling(7).mean(),2)
daily_metrics["ma7_revenue"] = round(daily_metrics["revenue"].rolling(7).mean(),2)
daily_metrics["ma7_kwh"] = round(daily_metrics["kwh"].rolling(7).mean(),2)


def variance(current_col,ma7_col):
    pct = (current_col -ma7_col)/ma7_col *100
    return pct.round(2)
        

def is_anomaily (variance_pct,thershold=30):
    return variance_pct.abs() > thershold

daily_metrics["session_var_pct"] = variance(daily_metrics["session"],daily_metrics["ma7_session"])
daily_metrics["revenue_var_pct"] = variance(daily_metrics["revenue"],daily_metrics["ma7_revenue"])
daily_metrics["kwh_var_pct"] = variance(daily_metrics["kwh"],daily_metrics["ma7_kwh"])
daily_metrics["session_anomaily"] = is_anomaily(daily_metrics["session_var_pct"],30)
daily_metrics["revenue_anomaily"] = is_anomaily(daily_metrics["revenue_var_pct"],30)
daily_metrics["kwh_anomaily"] = is_anomaily(daily_metrics["kwh_var_pct"],30)

print(daily_metrics)

