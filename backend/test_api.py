import urllib.request
import json

try:
    print("Testing /dashboard-stats...")
    with urllib.request.urlopen("http://localhost:8000/dashboard-stats") as response:
        if response.status == 200:
            data = json.loads(response.read().decode())
            print("Success!")
            print("Total Loans:", data.get("total_loans"))
            print("Approval Rate:", data.get("approval_rate"))
        else:
            print(f"Failed with status: {response.status}")
except Exception as e:
    print(f"Error: {e}")
