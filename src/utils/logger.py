import datetime

class Logger:
    log_levels = ["debug", "info", "warn", "error", "critical", "download"]

    log_strings = {
        "debug": "dbg",
        "info": "inf",
        "warn": "wrn",
        "error": "err",
        "critical": "crt",
        "download": "dwn"
    }
    

    def __init__(self, name, color, level):
        self.name = name
        self.color = color
        self.level = self.log_levels[level]
    
    
    def _time(self):
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        if now.hour > 18 and now.hour < 5:
            return f"{time} (☀️)"
        else:
            return f"{time} (🌙)"


    def _hextorgb(self, hex):
        hex = hex.lstrip("#")
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    
    
    def _colorize(self, color, message):
        if not type(color) == tuple:
            color = self._hextorgb(color)
        
        return f"\033[38;2;{color[0]};{color[1]};{color[2]}m{message}\033[0m"
            

    def log(self, level, message):
        if self.log_levels.index(level) < self.log_levels.index(self.level):
            return
        
        if not level in self.log_strings:
            level = "unk"
        else:
            level = self.log_strings[level]

        print(f"{self._time()} | [{level}] @ {self._colorize(self.color, self.name)}: {message}")
