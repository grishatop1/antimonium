import os
import time
import threading
import datetime
import subprocess as sub

class AppManager:
    def __init__(self, app) -> None:
        self.app = app
        self.list = self.app.gui.left_frame
        self.programs = {}
        self.loadFromCache()

    def updateList(self):
        app_items = list(self.programs.values())
        app_list = []
        for app_item in app_items:
            app_list.append(app_item.labelname + app_item.suffix)

        self.list.updateList(
            app_list
        )

    def saveToCache(self):
        output = {}
        for label_name, obj in self.programs.items():
            output[label_name] = obj.filepath

        self.app.cache.write("apps", output)

    def loadFromCache(self):
        data = self.app.cache.read("apps")
        for label_name, filepath in data.items():
            self.addProgram(filepath)

    def addProgram(self, filepath):
        filename = os.path.basename(filepath)
        labelname = os.path.splitext(filename)[0].capitalize()
        item = AppItem(self, filepath, filename, labelname)
        self.programs[labelname] = item
        self.updateList()
        self.saveToCache()

    def removeProgram(self, labelname):
        label = self.removeSuffix(labelname)
        del self.programs[label]
        self.updateList()
        self.saveToCache()

    def runProgram(self, labelname):
        label = self.removeSuffix(labelname)
        self.programs[label].suffix = " (running)"
        self.programs[label].run()
        self.updateList()

    def stopProgram(self, labelname):
        label = self.removeSuffix(labelname)
        self.programs[label].stop()

    def updateFileInfo(self, labelname):
        label = self.removeSuffix(labelname)
        item = self.programs[label]
        filepath, size, creation = item.getInfo()
        self.app.updateInfo(filepath, size, creation)
        self.app.updateStartBtn(item.running)

    def removeSuffix(self, labelname):
        if " (running)" in labelname:
            label, suffix = labelname.rsplit(" ", 1)
            return label
        else:
            return labelname

class AppItem:
    def __init__(self, manager, filepath, filename, labelname) -> None:
        self.manager = manager
        self.filepath = filepath
        self.filename = filename
        self.labelname = labelname
        self.suffix = ""
        self.running = False
        self.p = None

    def run(self):
        threading.Thread(
            target=self.runThread,
            daemon=True
        ).start()

    def stop(self):
        if self.running:
            self.running = False
            self.p.terminate()
    
    def runThread(self):
        self.p = sub.Popen([self.filepath], stdout=sub.PIPE, stderr=sub.PIPE)
        while True:
            poll = self.p.poll()
            if poll is None:
                break
            else:
                time.sleep(0.2)
        self.running = True
        self.p.wait()
        self.suffix = ""
        self.manager.updateList()

    def getInfo(self):
        size = f"{round(os.path.getsize(self.filepath)/1024/1024, 1)}MB" #in MB

        unix_timestamp = os.path.getctime(self.filepath)
        timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
        creation = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        return (self.filepath, size, creation)
        