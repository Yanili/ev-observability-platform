def calculative_variance_pct (current:float, previous:float):
    if previous == 0:
        return 0.0 #guard clause:never divide by zero
    return round((current-previous)/previous*100, 2)

current_session = 200
previous_session = 300
current_kwh = 25000
previous_kwh = 45000
current_revenue = 90000
previous_revenue = 800

def is_anomaly(variance_pct,threshold=30):
    if variance_pct > threshold :
        return True
    return False

print(is_anomaly(20))

session_var = calculative_variance_pct(current_session,previous_session)
if is_anomaly(session_var):
    print(f"Alert: variance {session_var} pct breaches threshold")

revenue_var = calculative_variance_pct(current_revenue,previous_revenue)
if is_anomaly(revenue_var):
    print(f"Alert: variance {revenue_var} pct breaches threshold")

# print(f"session {calculative_variance_pct(current_session,previous_session)}")
# print(calculative_variance_pct(current_kwh,previous_kwh))
#print(calculative_variance_pct(current_revenue,previous_revenue))

# print(calculative_variance_pct(1200,1100))
# print(calculative_variance_pct(870,1180))
# print(calculative_variance_pct(500,0))

