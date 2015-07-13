from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime
from barstatus import BarStatus
from bspccontrol import BspcControl
from threading import Thread
import re
import subprocess
from time import strftime

bar = BarStatus()

def getmemory():
    ps = subprocess.Popen(('free', '-m'), stdout=subprocess.PIPE)
    ps2 = subprocess.Popen(('grep', 'Mem'), stdin=ps.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(('awk', '{printf \"%3.1f\", $3 / $2 * 100}'), stdin=ps2.stdout)
    ps2.wait()
    bar.memory = output.decode('ascii')
    
def getwindowtitle():
    title = subprocess.check_output(('xdotool', 'getactivewindow', 'getwindowname')).decode('ascii').strip()
    bar.title = title
    
def getcurrenttime():
    current_time = strftime("%a %d %b %H:%M")
    bar.time = current_time
    
def getbattery():
    output = subprocess.check_output(('acpi')).decode('ascii')
    if 'Battery' in output:
        percentage = output.split(' ')[3].replace("%", "").replace(",", "").strip()
        bar.battery = percentage
        
def getip():
    cmd = subprocess.check_output(('ip', 'route')).decode('ascii')
    match = re.search("src ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", cmd)
    if match:
        bar.ip = match.group(1)
    else:
        bar.ip = "None"
    
#Configure scheduler
scheduler = BlockingScheduler()
scheduler.configure(timezone='Europe/Amsterdam')

#Schedule jobs
scheduler.add_job(getmemory, 'interval', seconds=2, next_run_time=datetime.now())
scheduler.add_job(getcurrenttime, 'interval', seconds=1, next_run_time=datetime.now())
scheduler.add_job(getbattery, 'interval', seconds=10, next_run_time=datetime.now())
scheduler.add_job(getip, 'interval', seconds=10, next_run_time=datetime.now())
scheduler.add_job(getwindowtitle, 'interval', seconds=.5, next_run_time=datetime.now())

#Start continious jobs
bspccontrol = BspcControl(bar)
Thread(target=bspccontrol.inputhandler).start()

#Start scheduler
scheduler.start()