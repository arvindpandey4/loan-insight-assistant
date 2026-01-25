import sys
import os
from pathlib import Path

# Add project root
sys.path.append(os.getcwd())

try:
    print("Importing backend.api...")
    from backend.api import loan_api
    print("Import successful!")
    
    print("Testing get_dashboard_stats...")
    stats = loan_api.get_dashboard_stats()
    print("Stats keys:", list(stats.keys()))
    print("Total loans:", stats.get("total_loans"))
    
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
