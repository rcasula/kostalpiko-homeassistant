from logging import lastResort
from kostalpiko.kostalpiko import Piko

import time

class PikoHolder(Piko):
    last_update = 0
    update_running = False
    def __init__(self, host=None, username="pvserver", password="pvwr") -> None:
        super().__init__(host, username, password)
    
    def update(self):
        if not self.update_running:
            if time.time() - self.last_update > 30.0:
                self.update_running=True
                self.last_update=time.time()
                super().update()
                self.update_running=False
