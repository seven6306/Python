# Reference: https://github.com/boppreh/keyboard#keyboard.remove_hotkey
import keyboard
from time import sleep
from tkinter import ttk, Tk, Label, Frame
def kb_action(account, password):
	keyboard.write(account)
	sleep(1)
	keyboard.press('Tab')
	sleep(1)
	keyboard.write(password)
	sleep(1)
	keyboard.press('Enter')
def restore_key(key):
	try:
		keyboard.remove_hotkey(key)
	except Exception:
		pass

class Windows(Frame):
	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)
		self.master.title('QuickPassword')
		self.master.geometry('350x145')
		self.master.resizable(0, 0)
		self.createWidgets()
		
	def createWidgets(self):
		self.master.LB = Label(self.master, text="1.Account: ", fg="blue")
		self.master.LB.place(x=40, y=15)
		self.master.TF1 = ttk.Entry(self.master, width=10)
		self.master.TF1.place(x=105, y=15)
		self.master.LB = Label(self.master, text="Password: ", fg="blue")
		self.master.LB.place(x=190, y=15)
		self.master.TF2 = ttk.Entry(self.master, width=10)
		self.master.TF2.place(x=255, y=15)
		self.master.Run = ttk.Button(self.master, text='OK', command=self.submit)
		self.master.Run.place(x=250, y=105)
	def submit(self):
		restore_key('F2')
		keyboard.add_hotkey('F2', lambda: kb_action(self.master.TF1.get(), self.master.TF2.get()))
		
if __name__ == '__main__':
	root = Tk()
	app = Windows(master=root)
	app.mainloop()
