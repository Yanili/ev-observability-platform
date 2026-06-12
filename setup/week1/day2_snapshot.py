# `snapshot = {
#    "date": "2026-06-11",
#    "sessions": 1200,
#    "revenue_gbp": 4500.00,
#    "kwh_delivered": 21000,
#    "active_chargers": 438,
#    "offline_chargers": 12,
# }
# # Derived metrics - computed, never typed in by hand
# snapshot["availability_pct"] = round(
#    snapshot["active_chargers"] /
#    (snapshot["active_chargers"] + snapshot["offline_chargers"]) * 100, 1
# )
# snapshot["revenue_per_session"] = round(snapshot["revenue_gbp"] / snapshot["sessions"], 2)
# for key, value in snapshot.items():
#    print(f"{key:>22}:{value}")


# Task 1 : build today snapshot with what I want to report
snapshot_1 = {
    "Date" : "12-06-2026",
    "Sessions" : 1899,
    "Energy"  : 38200,
    "Revenue" : 18900,
    "Users"   : 1422,
    "Sockets"  : 7000,
    "Uptime"  : 0.98,
    "Utilisation" : 0.25
}

snapshot_2 = {
    "Date" : "11-06-2026",
    "Sessions" : 2000,
    "Energy"  : 60000,
    "Revenue" : 30000,
    "Users"   : 1622,
    "Sockets"  : 7000,
    "Uptime"  : 0.98,
    "Utilisation" : 0.30
}

snapshot_3 = {
    "Date" : "10-06-2026",
    "Sessions" : 5000,
    "Energy"  : 35000,
    "Revenue" : 10000,
    "Users"   : 1000,
    "Sockets"  : 7000,
    "Uptime"  : 0.98,
    "Utilisation" : 0.15
}

# Task 2 : add failed session and pct

# snapshot_1["Failed sessions"] = 20
# snapshot_1["failed sessions pct"] = round(snapshot_1["Failed sessions"]/snapshot_1["Sessions"],2)

# Task 3 : mark a list of dict for 3 days
history = [snapshot_1,snapshot_2,snapshot_3]
#print(history)

import json 
print(json.dumps(history,indent=3))


