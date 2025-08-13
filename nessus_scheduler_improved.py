import os
import time
import logging
from datetime import datetime, timedelta
import requests
from concurrent.futures import ThreadPoolExecutor

# --- Yapılandırma ---
ACCESS_KEY = os.getenv("NESSUS_ACCESS_KEY", "null")
SECRET_KEY = os.getenv("NESSUS_SECRET_KEY", "null")

SCAN_IDS = ["70", "72", "74", "75", "76", "77", "78", "79", "80"]
NESSUS_URL = "https://127.0.0.1:8443"
MAX_WORKERS = 8

START_TIMES = ["00:00", "00:10", "00:15"]
PAUSE_TIMES = ["07:00", "07:10", "07:15"]

# --- Loglama Yapılandırması ---
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# --- Fonksiyonlar ---
def nessus_scan(action: str, scan_id: str):
    url = f"{NESSUS_URL}/scans/{scan_id}/{action}"
    headers = {"X-ApiKeys": f"accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}"}
    try:
        response = requests.post(url, headers=headers, verify=False, timeout=30)
        if response.status_code == 200:
            logging.info(f"Successfully executed '{action}' on scan {scan_id}.")
            return True
        else:
            logging.error(f"Failed to execute '{action}' on scan {scan_id}. Status: {response.status_code}, Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while trying to '{action}' scan {scan_id}: {e}")
        return False

def run_scans(action: str):
    logging.info(f"Starting to run '{action}' for {len(SCAN_IDS)} scans with {MAX_WORKERS} parallel workers...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(lambda sid: nessus_scan(action, sid), SCAN_IDS))
    success_count = sum(1 for r in results if r)
    logging.info(f"Action '{action}' finished. {success_count}/{len(SCAN_IDS)} scans were successful.")

def seconds_until(target_times: list[str]) -> int:
    """Sunucunun yerel saatine göre bir sonraki hedef zamana kalan saniyeyi hesaplar."""
    now = datetime.now()
    min_diff = float('inf')
    for t in target_times:
        hour, minute = map(int, t.split(":"))
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target < now:
            target += timedelta(days=1)
        diff = int((target - now).total_seconds())
        if diff < min_diff:
            min_diff = diff
    return min_diff

def format_time(seconds: int) -> str:
    h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

# --- Ana Döngü ---
def main():
    last_action_time = None
    logging.info("Scheduler started. Using server's local time.")
    while True:
        now = datetime.now()
        now_str = now.strftime("%H:%M")
        
        secs_to_start = seconds_until(START_TIMES)
        secs_to_pause = seconds_until(PAUSE_TIMES)
        
        print(f"Time until next action: Start in {format_time(secs_to_start)}, Pause in {format_time(secs_to_pause)}   ", end="\r")
        
        if now_str in START_TIMES and last_action_time != (now_str, "resume"):
            run_scans("resume")
            last_action_time = (now_str, "resume")
        elif now_str in PAUSE_TIMES and last_action_time != (now_str, "pause"):
            run_scans("pause")
            last_action_time = (now_str, "pause")
            
        time.sleep(1)

if __name__ == "__main__":
    # localhost için SSL sertifika uyarılarını bastır
    if NESSUS_URL.startswith('https://127.0.0.1'):
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    main()
