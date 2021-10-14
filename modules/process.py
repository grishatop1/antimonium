import threading
import subprocess as sub
import sys
import os
import time

class ProcessManager:
    def __init__(self) -> None:
        self.processes = []

    def runNewApp(self, filepath):
        p = AppProcess(self, filepath)
        self.processes.append(p)

class AppProcess:
    def __init__(self, manager, filepath) -> None:
        self.manager = manager
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        threading.Thread(
            target=self.runThread,
            daemon=True
        ).start()

    def runThread(self):
        p = sub.Popen([self.filepath], stdout=sub.PIPE, stderr=sub.PIPE)
        while True:
            poll = self.process.poll()
            if poll is None:
                break
            else:
                time.sleep(0.2)
        p.wait()