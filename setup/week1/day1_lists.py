# 7 days of charging sessions - like the values behind a line chart

daily_sessions = [1050, 1100, 980, 1200, 1180, 870, 910]
daily_revenue = [50,55,40,70,60,30,39]
total_revenue = sum(daily_revenue)
total = sum(daily_sessions)
average = total / len(daily_sessions)
highest = max(daily_sessions)
lowest = min(daily_sessions)

for sessions, rev in zip(daily_sessions,daily_revenue):
    print(f"GBP{rev/sessions:.2f} per session")
print(f"Total:{total} | Total Revenue:{total_revenue} | Revenue per session: {total_revenue/total:.2f} |Avg:{average:.0f} | High:{highest} | Low:{lowest}")

# Slicing = filtering by position
weekdays = daily_sessions[:5]     
# first five
weekend = daily_sessions[5:]      
# last two
print(f"Weekday avg:{sum(weekdays)/len(weekdays):.0f}")
print(f"Weekend avg:{sum(weekend)/len(weekend):.0f}")

#3- day moving average
random = daily_sessions[:3]
print(sum(random))
print(f"3-day moving average {sum(random)/len(random):.2f}")