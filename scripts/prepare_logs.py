import json
import os

input_file = "data/logs/repair_logs.json"
output_file = "data/logs/repair_logs.txt"

with open(input_file, "r") as f:
    logs = json.load(f)

with open(output_file, "w") as f:
    for log in logs:
        text = f"""
Vehicle: {log['vehicle']}
Issue: {log['issue']}
Symptoms: {log['symptoms']}
Fix: {log['fix']}
Date: {log['date']}
-------------------------
"""
        f.write(text)

print("✅ Logs converted to text")