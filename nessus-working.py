import os, time, threading
from datetime import datetime, timedelta


#https://127.0.0.1:8443/#/settings/my-account/api-keys

access_key = "null"
secret_key = "null"

scan_ids = ["70", "72", "74"]
nessus_url = "https://127.0.0.1:8443"

start_times = ["00:00", "00:10"]
pause_times = ["07:00", "07:00"]

def nessus_scan(action, scan_id):
    cmd = f'curl -X POST -sk -H "X-ApiKeys: accessKey={access_key}; secretKey={secret_key}" {nessus_url}/scans/{scan_id}/{action}'
    result = "Successfully" if os.system(cmd) == 0 else "Failed"
    print(f'[{datetime.now()}] {result} executed {action} on scan {scan_id}')

def run_scans(action):
    for scan_id in scan_ids:
        threading.Thread(target=nessus_scan, args=(action, scan_id)).start()

def seconds_until(target_times):
    now = datetime.now()
    min_diff = None
    for t in target_times:
        hour, minute = map(int, t.split(":"))
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target < now:
            target += timedelta(days=1)
        diff = int((target - now).total_seconds())
        if min_diff is None or diff < min_diff:
            min_diff = diff
    return min_diff

def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

last_action_time = None

while True:
    now_str = datetime.now().strftime("%H:%M")
    secs_to_start = seconds_until(start_times)
    secs_to_pause = seconds_until(pause_times)
    print(f"Kalan süre: Başlatmaya {format_time(secs_to_start)}, Durdurmaya {format_time(secs_to_pause)}", end="\r")
    if now_str in start_times and last_action_time != (now_str, "resume"):
        run_scans("resume")
        last_action_time = (now_str, "resume")
    elif now_str in pause_times and last_action_time != (now_str, "pause"):
        run_scans("pause")
        last_action_time = (now_str, "pause")
    time.sleep(1)
