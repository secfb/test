import os
import time
import threading
import subprocess
import logging
from datetime import datetime

access_key = os.getenv("NESSUS_ACCESS_KEY", "")
secret_key = os.getenv("NESSUS_SECRET_KEY", "")
scan_ids = ["43", "46", "51"]  #scan
nessus_url = "https://127.0.0.1:8443"
start_times = {"00:10", "00:15"}
pause_times = {"07:20", "07:30"}
daily_pause_time = "07:30"  # All scans should be paused at 07:30

# Setting up logging
logging.basicConfig(
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler("log.txt"),  # Log to a file named log.txt
        logging.StreamHandler()  # Log to the console as well
    ]
)

def nessus_scan(action, scan_id):
    cmd = [
        'curl', '-X', 'POST', '-sk',
        '-H', f'X-ApiKeys: accessKey={access_key}; secretKey={secret_key}',
        f'{nessus_url}/scans/{scan_id}/{action}'
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f'Successfully executed {action} on scan {scan_id}')
        else:
            logging.error(f'Failed to execute {action} on scan {scan_id}. Error: {result.stderr}')
        # Debugging output for testing
        logging.debug(f'Stdout: {result.stdout}\nStderr: {result.stderr}')
    except Exception as e:
        logging.exception(f'Exception occurred while executing {action} on scan {scan_id}')

def run_scans(action):
    threads = [threading.Thread(target=nessus_scan, args=(action, scan_id)) for scan_id in scan_ids]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

while True:
    now = datetime.now().strftime("%H:%M")
    
    # Start or pause scans based on predefined times
    if now in start_times:
        run_scans("resume")
    elif now in pause_times:
        run_scans("pause")
    # Pause all scans at 07:30
    elif now == daily_pause_time:
        logging.info(f'Pausing all scans at {daily_pause_time}')
        run_scans("pause")
    
    time.sleep(60)  # Sleep until the next minute
