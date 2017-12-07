from tkinter.filedialog import askopenfilename
from tkinter import ttk, Tk, Label, Frame
from tkinter.messagebox import showinfo, showerror, askokcancel

class Windows(Frame):
	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)
		self.master.title('ProgramName         Support Ver : Python3.5 (less)')
		self.master.geometry('400x160')
		self.master.resizable(0, 0)
		self.master.iconbitmap(default='')
		self.createWidgets()
	def createWidgets(self):
		self.master.LB = Label(self.master, text="Specified file : ", fg="blue")
		self.master.LB.place(x=10, y=18)
		self.master.Run = ttk.Button(self.master, text='GO', command=self.method)
		self.master.Run.config(state="disabled")
		self.master.Run.place(x=310, y=120)
		self.master.LB = Label(self.master, text="Message box : ", fg="blue")
		self.master.LB.place(x=10, y=120)
		self.master.displayText = Label(self.master, text="Execution message", fg="brown")
		self.master.displayText.place(x=90, y=120)
	def method(self):
		self.master.displayText["text"] = 'Commant here'
if __name__ == '__main__':
	root = Tk()
	app = Windows(master=root)
	app.mainloop()