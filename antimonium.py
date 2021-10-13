from modules.gui import GUI

class Application:
    def __init__(self) -> None:
        self.gui = None

    def run(self):
        self.gui = GUI(self)
        self.gui.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()