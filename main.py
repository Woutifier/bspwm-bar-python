from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime
from barstatus import BarStatus
from bspccontrol import BspcControl
from threading import Thread
import subprocess
from time import strftime

bar = BarStatus()

def getmemory():
    ps = subprocess.Popen(('free', '-m'), stdout=subprocess.PIPE)
    ps2 = subprocess.Popen(('grep', 'Mem'), stdin=ps.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(('awk', '{printf \"%3.1f\", $3 / $2 * 100}'), stdin=ps2.stdout)
    ps2.wait()
    bar.setmemory(output.decode('ascii'))
    
def getcurrenttime():
    current_time = strftime("%a %m %b %H:%M")
    bar.settime(current_time)
    
def getbattery():
    output = subprocess.check_output(('acpi')).decode('ascii')
    if 'Battery' in output:
        percentage = output.split(' ')[3].replace("%", "").replace(",", "")
        bar.setbattery(percentage)
    
    
#Configure scheduler
scheduler = BlockingScheduler()
scheduler.configure(timezone='Europe/Amsterdam')

#Schedule jobs
scheduler.add_job(getmemory, 'interval', seconds=2, next_run_time=datetime.now())
scheduler.add_job(getcurrenttime, 'interval', seconds=1, next_run_time=datetime.now())
scheduler.add_job(getbattery, 'interval', seconds=10, next_run_time=datetime.now())

#Start continious jobs
bspccontrol = BspcControl(bar)
Thread(target=bspccontrol.inputhandler).start()

#Start scheduler
scheduler.start()