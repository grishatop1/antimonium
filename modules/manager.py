import os
import sys
import time
import threading
import datetime
import subprocess as sub

class AppManager:
    def __init__(self, app) -> None:
        self.app = app
        self.list = self.app.gui.left_frame
        self.programs = {}
        self.currentSort = "a-z"
        
        self.loadFromCache()
       

    def updateList(self):
        app_items = list(self.programs.values())
        app_list = []
        for app_item in app_items:
            app_list.append(app_item.labelname + app_item.suffix)

        app_sort = self.sortList(app_list)

        self.list.updateList(
            app_sort
        )

    def changeSort(self, _sort):
        self.currentSort = _sort
        self.updateList()

    def sortList(self, app_list):
        if self.currentSort == "a-z":
            return sorted(app_list)
        elif self.currentSort == "z-a":
            return sorted(app_list, reverse=True)

    def saveToCache(self):
        output = {}
        for label_name, obj in self.programs.items():
            output[label_name] = obj.filepath

        self.app.cache.write("apps", output)

    def loadFromCache(self):
        data = self.app.cache.read("apps")
        for label_name, filepath in data.items():
            self.addProgram(filepath, update=False, label_name=label_name)

        self.updateList()

    def addProgram(self, filepath, update=True, label_name=None):
        filename = os.path.basename(filepath)
        if not label_name:
            labelname = os.path.splitext(filename)[0].capitalize()
        else:
            labelname = label_name
        item = AppItem(self, filepath, filename, labelname)
        self.programs[labelname] = item
        if update:
            self.updateList()
            self.saveToCache()

    def renameProgram(self, new, old):
        try:
            if new in self.programs:
                return
            self.programs[new] = self.programs.pop(old)
            self.programs[new].labelname = new
            self.updateList()
            self.saveToCache()
        except: pass

    def removeProgram(self, labelname):
        label = self.removeSuffix(labelname)
        del self.programs[label]
        self.updateList()
        self.saveToCache()

    def runProgram(self, labelname, closeAnti):
        label = self.removeSuffix(labelname)
        if closeAnti:
            self.app.cache.write("closeOnLaunch", True)
            self.programs[label].runAndBye()
            sys.exit()
        else:
            self.app.cache.write("closeOnLaunch", False)
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

    def runAndBye(self):
        os.startfile(self.filepath)

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
        self.running = False
        self.suffix = ""
        self.manager.updateList()
        self.manager.app.updateStartBtn(False)

    def getInfo(self):
        size = f"{round(os.path.getsize(self.filepath)/1024/1024, 1)}MB" #in MB

        unix_timestamp = os.path.getctime(self.filepath)
        timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
        creation = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        return (self.filepath, size, creation)
        