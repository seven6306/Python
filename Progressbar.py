from sys import exit
from time import sleep
from subprocess import call
from tkinter import ttk, Tk, HORIZONTAL
from threading import Thread, active_count

class MultiProcess(Thread):
	def __init__(self, action, delay):
		Thread.__init__(self)
		self.action = action
		self.delay = delay
	def run(self):
		ProcessAction(self.action, self.delay)
def ProcessAction(action=None, delay=0):
	sleep(delay)
	if action == 'ping':
		call('ping 8.8.8.8')
	else:
		app.runbar()
class ProgressBar(Tk):
	def __init__(self):
		super().__init__()
		self.title('Progressing')
		self.geometry('400x48+470+420')
		self.resizable(0, 0)
		self.focus()
		self.grab_set()
		def close_E():
			self.title('Do not close window while progressing')
		self.protocol('WM_DELETE_WINDOW', close_E)
		self.createWidgets()
	def createWidgets(self):
		self.progress = ttk.Progressbar(self, orient=HORIZONTAL, length=400, mode='determinate')
		self.progress.place(x=0, y=0)
		self.BT2 = ttk.Button(self, style="TButton", text='Run')
		self.BT2.place(x=168, y=22)
	def runbar(self):
		self.config(cursor="wait")
		self.BT2.config(state="normal", text='Run')
		ttk.Style().configure("TButton", foreground="blue")
		for count in range(5):
			if count >= 1:
				self.progress['value'] = count * 25
				self.BT2['text'] = str(count * 25) + '%'
				self.update_idletasks()
				sleep(1)
		self.config(cursor="")
		ttk.Style().configure("TButton", foreground="black")
		self.BT2.config(state="normal", text='Complete')
		sleep(1)
		self.quit()
if __name__ == '__main__':
	app = ProgressBar()
	thread_1 = MultiProcess('ping', 0)
	thread_2 = MultiProcess('progress', 0)
	thread_1.start()
	thread_2.start()
	app.mainloop()