import os

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
            app_list.append(app_item.labelname)

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
        del self.programs[labelname]
        self.updateList()
        self.saveToCache()

class AppItem:
    def __init__(self, manager, filepath, filename, labelname) -> None:
        self.manager = manager
        self.filepath = filepath
        self.filename = filename
        self.labelname = labelname