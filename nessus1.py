import os
import time
import threading
import subprocess
from datetime import datetime

# Access keys and URLs should be read from environment variables for security.
access_key = os.getenv("NESSUS_ACCESS_KEY", "")
secret_key = os.getenv("NESSUS_SECRET_KEY", "")
scan_ids = ["43", "46", "51"]
nessus_url = "https://127.0.0.1:8443"
start_times = {"00:10", "00:15"}
pause_times = {"07:20", "07:30"}

def nessus_scan(action, scan_id):
    cmd = [
        'curl', '-X', 'POST', '-sk',
        '-H', f'X-ApiKeys: accessKey={access_key}; secretKey={secret_key}',
        f'{nessus_url}/scans/{scan_id}/{action}'
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f'[{datetime.now()}] Successfully executed {action} on scan {scan_id}')
        else:
            print(f'[{datetime.now()}] Failed to execute {action} on scan {scan_id}. Error: {result.stderr}')
    except Exception as e:
        print(f'[{datetime.now()}] Exception occurred: {str(e)}')

def run_scans(action):
    threads = [threading.Thread(target=nessus_scan, args=(action, scan_id)) for scan_id in scan_ids]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

while True:
    now = datetime.now().strftime("%H:%M")
    if now in start_times:
        run_scans("resume")
    elif now in pause_times:
        run_scans("pause")
    time.sleep(60)  # Sleep until the next minute
