import subprocess

class BspcControl:
    def __init__(self, bar):
        self.bar = bar
        self.bspc = subprocess.Popen(('bspc', 'control', '--subscribe'), stdout=subprocess.PIPE)
        self.monitors = []

    def inputhandler(self):
        while True:
            input = self.bspc.stdout.readline().decode('ascii').strip()[1:]
            self.monitors = []
            self.parseline(input)

    def parseline(self,line):
        split = line.split(':')
        ismonitor = True
        for item in split:
            if ismonitor:
                self.monitors.append(Monitor(item[1:], item[0:1]))
                ismonitor = False
            elif item.startswith('L'):
                ismonitor = True
            else:
                self.monitors[-1].add_desktop(Desktop(item[1:], item[:1]))
        self.outputbar()

    def outputbar(self):
        self.bar.setmonitors(self.monitors)

    def __str__(self):
        return 'Test'

class Monitor:
    def __init__(self, name, status):
        self.name = name
        self.desktops = []
        print(status)

    def add_desktop(self, desktop):
        self.desktops.append(desktop)

    def __str__(self):
        returnstring = 'Monitor: ' + self.name + '\n'
        for desktop in self.desktops:
            returnstring += str(desktop) + '\n'
        return returnstring

class Desktop:
    def __init__(self, name, status):
        self.name = name
        if status == 'F':
            self.active = True
            self.used = False
        elif status == 'f':
            self.active = False
            self.used = False
        elif status == 'o':
            self.active = False
            self.used = True
        else:
            self.active = True
            self.used = True

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def __str__(self):
        return self.name + ': ' + str(self.active) + ' ' + str(self.used)
