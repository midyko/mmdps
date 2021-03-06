import tkinter as tk
from mmdps.gui import guiframe, toolman

class MainApplication(guiframe.MainWindow):
	def __init__(self, master=None, **kw):
		guiframe.MainWindow.__init__(self, master, **kw)

	def setup(self, toolsmanager):
		self.toolsmanager = toolsmanager
		self.build_widgets()

	def build_widgets(self):
		tools = self.toolsmanager.tools
		for tool in tools:
			w = tool.build_widget(self.mainframe)
			w.pack(fill='x', expand=True)

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('800x600')
	app = MainApplication(root, height = 480, width = 640)

	manager = toolman.get_default_manager()

	app.setup(manager)
	app.pack(fill='both', expand=True)
	root.title('MMDPS Main')
	root.mainloop()
