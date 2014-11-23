import subprocess

class BarStatus:
    COLOR_FOREGROUND = '#FFA3A6AB'
    COLOR_BACKGROUND = '#FF34322E'
    COLOR_ACTIVE_MONITOR_FG = '#FF34322E'
    COLOR_ACTIVE_MONITOR_BG = '#FF58C5F1'
    COLOR_INACTIVE_MONITOR_FG = '#FF58C5F1'
    COLOR_INACTIVE_MONITOR_BG = '#FF34322E'
    COLOR_FOCUSED_OCCUPIED_FG = '#FFF6F9FF'
    COLOR_FOCUSED_OCCUPIED_BG = '#FF5C5955'
    COLOR_FOCUSED_FREE_FG = '#FFF6F9FF'
    COLOR_FOCUSED_FREE_BG = '#FF6D561C'
    COLOR_FOCUSED_URGENT_FG = '#FF34322E'
    COLOR_FOCUSED_URGENT_BG = '#FFF9A299'
    COLOR_OCCUPIED_FG = '#FFA3A6AB'
    COLOR_OCCUPIED_BG = '#FF34322E'
    COLOR_FREE_FG = '#FF6F7277'
    COLOR_FREE_BG = '#FF34322E'
    COLOR_URGENT_FG = '#FFF9A299'
    COLOR_URGENT_BG = '#FF34322E'
    COLOR_LAYOUT_FG = '#FFA3A6AB'
    COLOR_LAYOUT_BG = '#FF34322E'
    COLOR_TITLE_FG = '#FFA3A6AB'
    COLOR_TITLE_BG = '#FF34322E'
    COLOR_STATUS_FG = '#FFA3A6AB'
    COLOR_STATUS_BG = '#FF34322E'
    
    def __init__(self):
        self.bar = subprocess.Popen(('bar', '-p', '-g', 'x20', '-f', '-*-terminus-medium-r-normal-*-*-*-*-*-*-*-*-*', '-F', BarStatus.COLOR_FOREGROUND, '-B', BarStatus.COLOR_BACKGROUND), stdin=subprocess.PIPE)
        self.memory = ''
        self.monitorline = ''
        self.time = ''
        self.battery = ''
        self.ip = 'None'
        print("Bar initialized")
    
    def refresh(self):
        output = '%{l}' + self.monitorline + '%{r}IP: ' + self.ip + '  Bat: ' + self.battery + '%%  Mem: ' + self.memory + '%%  ' + self.time + '\n'
        self.bar.stdin.write(output.encode('ascii'))
        self.bar.stdin.flush()
        
    def setmemory(self, usage):
        dorefresh = False
        if self.memory != usage:
            dorefresh = True
        self.memory = usage
        if dorefresh:
            self.refresh()
            
    def settime(self, time):
        self.time = time
        self.refresh()
    
    def setbattery(self, battery):
        self.battery = battery
        self.refresh()
            
    def setmonitors(self, monitors):
        self.monitors = monitors
        self.monitorline = ''
        for monitor in monitors:
            if True:
                self.monitorline += str(FormattedText(' ' + monitor.name + ' ', fgcolor=BarStatus.COLOR_ACTIVE_MONITOR_FG, bgcolor=BarStatus.COLOR_ACTIVE_MONITOR_BG))
            for desktop in monitor.desktops:
                text = FormattedText(' ' + desktop.name + ' ')
                if desktop.active and desktop.used:
                    text.fgcolor = BarStatus.COLOR_FOCUSED_OCCUPIED_FG
                    text.bgcolor = BarStatus.COLOR_FOCUSED_OCCUPIED_BG
                    text.ucolor = BarStatus.COLOR_FOCUSED_OCCUPIED_FG
                elif desktop.active:
                    text.fgcolor = BarStatus.COLOR_FOCUSED_FREE_FG
                    text.bgcolor = BarStatus.COLOR_FOCUSED_FREE_BG
                    text.ucolor = BarStatus.COLOR_FOCUSED_FREE_FG
                elif desktop.used:
                    text.fgcolor = BarStatus.COLOR_OCCUPIED_FG
                self.monitorline += str(text)
        self.refresh()
        
class FormattedText:
    def __init__(self, text, fgcolor=None, bgcolor=None, ucolor=None):
        self.text = text
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.ucolor = ucolor
    
    def __str__(self):
        returnstring = self.text
        if self.ucolor != None:
            returnstring = '%{U' + self.ucolor + '}%{+u}' + returnstring
            returnstring += '%{-u}'
        if self.fgcolor != None:
            returnstring = '%{F' + self.fgcolor + '}' + returnstring
            returnstring += '%{F-}'
        if self.bgcolor != None:
            returnstring = '%{B' + self.bgcolor + '}' + returnstring
            returnstring += '%{B-}'
        return returnstring
        
