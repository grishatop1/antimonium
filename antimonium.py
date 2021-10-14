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

    def gui_removeProgram(self, labelname):
        self.manager.removeProgram(labelname)
    
    def gui_runProgram(self, labelname):
        self.manager.runProgram(labelname)

if __name__ == "__main__":
    app = Application()
    app.run()