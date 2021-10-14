from modules.gui import GUI
from modules.manager import AppManager
from modules.cachemngr import CacheManager

class Application:
    def __init__(self) -> None:
        self.gui = None
        self.manager = None
        self.cache = CacheManager()

    def run(self):
        self.gui = GUI(self)
        self.manager = AppManager(self)
        self.gui.mainloop()

    def gui_addProgram(self, filepath):
        self.manager.addProgram(filepath)

    def gui_renameProgram(self, new, old):
        self.manager.renameProgram(new, old)

    def gui_removeProgram(self, labelname):
        self.manager.removeProgram(labelname)
    
    def gui_runProgram(self, labelname, closeAnti):
        self.manager.runProgram(labelname, closeAnti)

    def gui_stopProgram(self, labelname):
        self.manager.stopProgram(labelname)

    def gui_updateInfo(self, labelname):
        self.manager.updateFileInfo(labelname)

    def gui_changeSort(self, _sort):
        self.manager.changeSort(_sort)

    def updateInfo(self, filepath, size, creation):
        self.gui.right_frame.info_frame.setInfo(filepath, size, creation)

    def updateStartBtn(self, running):
        if running:
            self.gui.right_frame.start_frame.setRunning()
        else:
            self.gui.right_frame.start_frame.setRun()

if __name__ == "__main__":
    app = Application()
    app.run()