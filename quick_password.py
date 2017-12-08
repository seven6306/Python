# Reference: https://github.com/boppreh/keyboard#keyboard.remove_hotkey
import keyboard
from time import sleep
from os.path import join
from tkinter import ttk, Tk, Label, Frame, IntVar
from winreg import OpenKey, CreateKey, KEY_ALL_ACCESS, QueryValueEx, SetValueEx, REG_SZ, HKEY_CURRENT_USER

def RegistryPrep():
	if not Registrar('exists', r'HKEY_CURRENT_USER\Software\QKpasswd'):
		Registrar('setkey', r'HKEY_CURRENT_USER\Software', 'QKpasswd')
		for i in range(1,6):
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile{}'.format(str(i)), ';')
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark{}'.format(str(i)), 'Click to add text')
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
def Registrar(Action='get', RegPath='', RegName='', RegValue=''):
	ClassDict = {'HKEY_CURRENT_USER':HKEY_CURRENT_USER}
	mainkey = RegPath.split('\\')[0]
	RegRelativePath = RegPath.replace(mainkey + '\\', '')
	if Action == 'exists':
		try:
			with OpenKey(ClassDict[mainkey], RegRelativePath, 0, KEY_ALL_ACCESS) as key:
				return(True)
		except FileNotFoundError:
			return(False)
	try:
		with OpenKey(ClassDict[mainkey], RegRelativePath, 0, KEY_ALL_ACCESS) as key:
			if Action == 'get':
				value = QueryValueEx(key, RegName)[0]
				return(value)
			elif Action == 'set':
				SetValueEx(key, RegName, 0, REG_SZ, RegValue)
				if QueryValueEx(key, RegName)[0]:
					return(True)
				else:
					return(False)
			elif Action == 'setkey':
				CreateKey(ClassDict[mainkey], join(RegRelativePath, RegName))
	except FileNotFoundError as regerr:
		pass
class Windows(Frame):
	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)
		self.master.title('QuickPassword')
		self.master.geometry('350x285')
		self.master.resizable(0, 0)
		self.createWidgets()
	def createWidgets(self):
		self.master.CheckVar = IntVar()
		val, y_val = 16, 0
		for value in range(1,6):
			self.master.RB = ttk.Radiobutton(self.master, text='', variable=self.master.CheckVar, value=value, command=self.checked_event).place(x=15, y=val)
			self.master.LB = Label(self.master, text="{}.Account: ".format(str(value)), fg="blue").place(x=40, y=15 + y_val)
			self.master.LB = Label(self.master, text="Password: ", fg="blue").place(x=190, y=15 + y_val)
			val, y_val = val + 47, y_val + 48
		def editText1(event):
			self.master.TF_1 = ttk.Entry(self.master, width=35)
			self.master.TF_1.place(x=40, y=39)
			self.master.TF_1.focus_set()
			self.master.Done1 = ttk.Button(self.master, width=5, text='Done', command=self.save_Text1)
			self.master.Done1.place(x=290, y=37)
		self.master.Tag1 = Label(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark1'))
		self.master.Tag1.place(x=40, y=37)
		self.master.Tag1.bind('<Button-1>', editText1)
		def editText2(event):
			self.master.TF_2 = ttk.Entry(self.master, width=35)
			self.master.TF_2.place(x=40, y=87)
			self.master.TF_2.focus_set()
			self.master.Done2 = ttk.Button(self.master, width=5, text='Done', command=self.save_Text2)
			self.master.Done2.place(x=290, y=85)
		self.master.Tag2 = Label(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark2'))
		self.master.Tag2.place(x=40, y=85)
		self.master.Tag2.bind('<Button-1>', editText2)
		def editText3(event):
			self.master.TF_3 = ttk.Entry(self.master, width=35)
			self.master.TF_3.place(x=40, y=136)
			self.master.TF_3.focus_set()
			self.master.Done3 = ttk.Button(self.master, width=5, text='Done', command=self.save_Text3)
			self.master.Done3.place(x=290, y=134)
		self.master.Tag3 = Label(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark3'))
		self.master.Tag3.place(x=40, y=134)
		self.master.Tag3.bind('<Button-1>', editText3)
		def editText4(event):
			self.master.TF_4 = ttk.Entry(self.master, width=35)
			self.master.TF_4.place(x=40, y=183)
			self.master.TF_4.focus_set()
			self.master.Done4 = ttk.Button(self.master, width=5, text='Done', command=self.save_Text4)
			self.master.Done4.place(x=290, y=181)
		self.master.Tag4 = Label(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark4'))
		self.master.Tag4.place(x=40, y=181)
		self.master.Tag4.bind('<Button-1>', editText4)
		def editText5(event):
			self.master.TF_5 = ttk.Entry(self.master, width=35)
			self.master.TF_5.place(x=40, y=231)
			self.master.TF_5.focus_set()
			self.master.Done5 = ttk.Button(self.master, width=5, text='Done', command=self.save_Text5)
			self.master.Done5.place(x=290, y=229)
		self.master.Tag5 = Label(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark5'))
		self.master.Tag5.place(x=40, y=229)
		self.master.Tag5.bind('<Button-1>', editText5)
		self.master.TF1 = ttk.Entry(self.master, width=10)
		self.master.TF1.insert(0, Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile1').split(';')[0])
		self.master.TF1.place(x=105, y=15)
		self.master.TF2 = ttk.Entry(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile1').split(';')[1], show="●", width=10)
		self.master.TF2.insert(0, Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile1').split(';')[1])
		self.master.TF2.place(x=255, y=15)
		self.master.TF3 = ttk.Entry(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile2').split(';')[0], width=10)
		self.master.TF3.insert(0, Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile2').split(';')[0])
		self.master.TF3.place(x=105, y=63)
		self.master.TF4 = ttk.Entry(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile2').split(';')[1], show="●", width=10)
		self.master.TF4.insert(0, Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile2').split(';')[1])
		self.master.TF4.place(x=255, y=63)
		self.master.TF5 = ttk.Entry(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile3').split(';')[0], width=10)
		self.master.TF5.place(x=105, y=112)
		self.master.TF6 = ttk.Entry(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile3').split(';')[1], show="●", width=10)
		self.master.TF6.place(x=255, y=112)
		self.master.TF7 = ttk.Entry(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile4').split(';')[0], width=10)
		self.master.TF7.place(x=105, y=160)
		self.master.TF8 = ttk.Entry(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile4').split(';')[1], show="●", width=10)
		self.master.TF8.place(x=255, y=160)
		self.master.TF9 = ttk.Entry(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile5').split(';')[0], width=10)
		self.master.TF9.place(x=105, y=207)
		self.master.TF10 = ttk.Entry(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile5').split(';')[1], show="●", width=10)
		self.master.TF10.place(x=255, y=207)
		self.master.Run = ttk.Button(self.master, text='Save', state="disabled", command=self.submit)
		self.master.Run.place(x=250, y=255)
	def checked_event(self):
		self.master.Run.config(state="normal")
	def save_Text1(self):
		if self.master.TF_1.get():
			self.master.Tag1.config(text=self.master.TF_1.get())
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark1', self.master.TF_1.get())
		self.master.TF_1.destroy()
		self.master.Done1.destroy()
	def save_Text2(self):
		if self.master.TF_2.get():
			self.master.Tag2.config(text=self.master.TF_2.get())
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark2', self.master.TF_2.get())
		self.master.TF_2.destroy()
		self.master.Done2.destroy()
	def save_Text3(self):
		if self.master.TF_3.get():
			self.master.Tag3.config(text=self.master.TF_3.get())
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark3', self.master.TF_3.get())
		self.master.TF_3.destroy()
		self.master.Done3.destroy()
	def save_Text4(self):
		if self.master.TF_4.get():
			self.master.Tag4.config(text=self.master.TF_4.get())
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark4', self.master.TF_4.get())
		self.master.TF_4.destroy()
		self.master.Done4.destroy()
	def save_Text5(self):
		if self.master.TF_5.get():
			self.master.Tag5.config(text=self.master.TF_5.get())
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark5', self.master.TF_5.get())
		self.master.TF_5.destroy()
		self.master.Done5.destroy()
	def submit(self):
		restore_key('F2')
		TF_list = [self.master.TF1.get() + ';' + self.master.TF2.get(), self.master.TF3.get() + ';' + self.master.TF4.get(),
				   self.master.TF5.get() + ';' + self.master.TF6.get(), self.master.TF7.get() + ';' + self.master.TF8.get(),
				   self.master.TF9.get() + ';' + self.master.TF10.get(),
				   ]
		Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile{}'.format(self.master.CheckVar.get()), TF_list[self.master.CheckVar.get()-1])
		keyboard.add_hotkey('F2', lambda: kb_action(TF_list[self.master.CheckVar.get()-1].split(';')[0], TF_list[self.master.CheckVar.get()-1].split(';')[1]))

if __name__ == '__main__':
	RegistryPrep()
	root = Tk()
	app = Windows(master=root)
	app.mainloop()
