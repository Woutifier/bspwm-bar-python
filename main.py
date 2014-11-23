from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime
from barstatus import barstatus
from bspccontrol import bspccontrol
from threading import Thread
import subprocess
#subprocess.call(["free", "-m | grep Mem | awk '{printf \"%3.1f\", $3 / $2 * 100}'"])

bar = barstatus()

def getmemory():
    ps = subprocess.Popen(('free', '-m'), stdout=subprocess.PIPE)
    ps2 = subprocess.Popen(('grep', 'Mem'), stdin=ps.stdout, stdout=subprocess.PIPE)
    output = subprocess.check_output(('awk', '{printf \"%3.1f\", $3 / $2 * 100}'), stdin=ps2.stdout)
    ps2.wait()
    bar.setmemory(output.decode('ascii'))
    print(output)
    
#Configure scheduler
scheduler = BlockingScheduler()
scheduler.configure(timezone='Europe/Amsterdam')

#Schedule jobs
scheduler.add_job(getmemory, 'interval', seconds=2)

#Start continious jobs
bspccontrol = bspccontrol(bar)
Thread(target=bspccontrol.inputhandler).start()

#Start scheduler
scheduler.start()