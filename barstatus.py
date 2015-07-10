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
    COLOR_RED = '#FFFF0000'
    
    def __init__(self):
        self.bar = subprocess.Popen(('lemonbar', '-p', '-g', 'x20', '-f', '-*-terminus-medium-r-normal-*-*-*-*-*-*-*-*-*', '-F', BarStatus.COLOR_FOREGROUND, '-B', BarStatus.COLOR_BACKGROUND), stdin=subprocess.PIPE)
        self._memory = ''
        self.monitorline = ''
        self._time = ''
        self._battery = ''
        self._ip = 'None'
        print("Bar initialized")
    
    def refresh(self):
        output = '%{l}' + self.monitorline + '%{r}' + str(FormattedText('IP: ', fgcolor=BarStatus.COLOR_RED)) + self._ip + '  ' + str(FormattedText('Bat: ', fgcolor=BarStatus.COLOR_RED)) + self._battery + '%%  ' + str(FormattedText('Mem: ', fgcolor=BarStatus.COLOR_RED)) + self.memory + '%%  ' + self._time + '\n'
        self.bar.stdin.write(output.encode('ascii'))
        self.bar.stdin.flush()
    
    @property
    def memory(self):
        return self._memory
    
    @memory.setter
    def memory(self, usage):
        dorefresh = False
        if self._memory != usage:
            dorefresh = True
        self._memory = usage
        if dorefresh:
            self.refresh()
            
    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, time):
        self._time = time
        self.refresh()
        
    @property
    def battery(self):
        return self._battery
    
    @battery.setter
    def battery(self, battery):
        self._battery = battery
        self.refresh()
        
    @property
    def ip(self):
        return self._ip
    
    @ip.setter
    def ip(self, ip):
        self._ip = ip
        self.refresh()
            
    def setmonitors(self, monitors):
        self.monitors = monitors
        self.monitorline = ''
        index = 0
        for monitor in monitors:
            if True:
                self.monitorline += '%{S' + str(index) + '}' + str(FormattedText(' ' + monitor.name + ' ', fgcolor=BarStatus.COLOR_ACTIVE_MONITOR_FG, bgcolor=BarStatus.COLOR_ACTIVE_MONITOR_BG))
                index += 1
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
        self.monitorline += '%{S0}'
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
        
