import npyscreen

class MainForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.BoxTitle, name="Pages", relx=1, rely=1, width=20)
        self.add(npyscreen.BoxTitle, name="Recipes", relx=1, width=20)

    def afterEditing(self):
        self.parentApp.setNextForm(None)

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm)
        return super().onStart()

if __name__=="__main__":
    app = App().run()