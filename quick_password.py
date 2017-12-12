# Reference: https://github.com/boppreh/keyboard#keyboard.remove_hotkey
import keyboard
from time import sleep
from os.path import join
from tkinter.messagebox import showerror
from tkinter.colorchooser import askcolor
from tkinter import ttk, Tk, Label, Frame, IntVar
from winreg import OpenKey, CreateKey, KEY_ALL_ACCESS, QueryValueEx, SetValueEx, REG_SZ, HKEY_CURRENT_USER

def kb_action(account, password, combotext):
	for each_part in combotext.split('>'):
		if each_part == 'account':
			keyboard.write(account)
		elif each_part == 'password':
			keyboard.write(password)
		else:
			keyboard.press(each_part)
		sleep(1)
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
def RegistryPrep():
	if not Registrar('exists', r'HKEY_CURRENT_USER\Software\QKpasswd'):
		Registrar('setkey', r'HKEY_CURRENT_USER\Software', 'QKpasswd')
		Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'comboset', 'account>Tab>password>Enter')
		for i in range(1,6):
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile{}'.format(str(i)), ';')
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark{}'.format(str(i)), 'Click to add text')
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color{}'.format(str(i)), '#000000')
def det_color(num):
	if 'color' in globals():
		global color
		Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color{}'.format(num), color)
		return_c = color
		globals().pop('color', None)
		return(return_c)
	else:
		return(Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color{}'.format(num)))
class Windows(Frame):
	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)
		self.master.title('QuickPassword')
		self.master.geometry('350x355')
		self.master.resizable(0, 0)
		keyboard.add_hotkey('Home', self.Home_key)
		self.createWidgets()
	def createWidgets(self):
		self.master.CheckVar = IntVar()
		val, y_val = 16, 0
		for value in range(1,6):
			self.master.RB = ttk.Radiobutton(self.master, text='', variable=self.master.CheckVar, value=value, command=lambda: self.master.Run.config(state="normal")).place(x=15, y=val)
			self.master.LB = Label(self.master, text="{}.Account: ".format(str(value)), fg="blue").place(x=40, y=15 + y_val)
			self.master.LB = Label(self.master, text="Password: ", fg="blue").place(x=190, y=15 + y_val)
			val, y_val = val + 47, y_val + 48
		def editText1(event):
			self.master.TF_1 = ttk.Entry(self.master, width=30, foreground=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color1'))
			self.master.TF_1.place(x=40, y=39)
			self.master.TF_1.focus_set()
			self.master.TF_1.insert(0, self.master.Tag1['text'])
			self.master.Color1 = ttk.Button(self.master, width=5, text='Color', command=self.cc)
			self.master.Color1.place(x=256, y=37)
			self.master.Done1 = ttk.Button(self.master, width=3, text='OK', command=self.save_Text1)
			self.master.Done1.place(x=300, y=37)
		self.master.Tag1 = Label(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark1'), fg=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color1'))
		self.master.Tag1.place(x=40, y=37)
		self.master.Tag1.bind('<Button-1>', editText1)
		def editText2(event):
			self.master.TF_2 = ttk.Entry(self.master, width=30, foreground=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color2'))
			self.master.TF_2.place(x=40, y=87)
			self.master.TF_2.focus_set()
			self.master.TF_2.insert(0, self.master.Tag2['text'])
			self.master.Color2 = ttk.Button(self.master, width=5, text='Color', command=self.cc)
			self.master.Color2.place(x=256, y=85)
			self.master.Done2 = ttk.Button(self.master, width=3, text='OK', command=self.save_Text2)
			self.master.Done2.place(x=300, y=85)
		self.master.Tag2 = Label(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark2'), fg=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color2'))
		self.master.Tag2.place(x=40, y=85)
		self.master.Tag2.bind('<Button-1>', editText2)
		def editText3(event):
			self.master.TF_3 = ttk.Entry(self.master, width=30, foreground=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color3'))
			self.master.TF_3.place(x=40, y=136)
			self.master.TF_3.focus_set()
			self.master.TF_3.insert(0, self.master.Tag3['text'])
			self.master.Color3 = ttk.Button(self.master, width=5, text='Color', command=self.cc)
			self.master.Color3.place(x=256, y=134)
			self.master.Done3 = ttk.Button(self.master, width=3, text='OK', command=self.save_Text3)
			self.master.Done3.place(x=300, y=134)
		self.master.Tag3 = Label(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark3'), fg=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color3'))
		self.master.Tag3.place(x=40, y=134)
		self.master.Tag3.bind('<Button-1>', editText3)
		def editText4(event):
			self.master.TF_4 = ttk.Entry(self.master, width=30, foreground=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color4'))
			self.master.TF_4.place(x=40, y=183)
			self.master.TF_4.focus_set()
			self.master.TF_4.insert(0, self.master.Tag4['text'])
			self.master.Color4 = ttk.Button(self.master, width=5, text='Color', command=self.cc)
			self.master.Color4.place(x=256, y=181)
			self.master.Done4 = ttk.Button(self.master, width=3, text='OK', command=self.save_Text4)
			self.master.Done4.place(x=300, y=181)
		self.master.Tag4 = Label(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark4'), fg=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color4'))
		self.master.Tag4.place(x=40, y=181)
		self.master.Tag4.bind('<Button-1>', editText4)
		def editText5(event):
			self.master.TF_5 = ttk.Entry(self.master, width=30, foreground=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color5'))
			self.master.TF_5.place(x=40, y=231)
			self.master.TF_5.focus_set()
			self.master.TF_5.insert(0, self.master.Tag5['text'])
			self.master.Color5 = ttk.Button(self.master, width=5, text='Color', command=self.cc)
			self.master.Color5.place(x=256, y=229)
			self.master.Done5 = ttk.Button(self.master, width=3, text='OK', command=self.save_Text5)
			self.master.Done5.place(x=300, y=229)
		self.master.Tag5 = Label(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark5'), fg=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_color5'))
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
		self.master.Combo = Label(self.master, text="Keyboard Combo: ", fg="purple").place(x=20, y=255)
		def editCombo(event):
			self.master.TF_6 = ttk.Entry(self.master, width=24)
			self.master.TF_6.place(x=130, y=256)
			self.master.TF_6.focus_set()
			self.master.TF_6.insert(0, self.master.ComboStatus['text'])
			self.master.Done6 = ttk.Button(self.master, width=3, text='OK', command=self.save_Combo)
			self.master.Done6.place(x=300, y=254)
		self.master.ComboStatus = Label(self.master, text=Registrar('get', r'HKEY_CURRENT_USER\Software\QKpasswd', 'comboset'))
		self.master.ComboStatus.place(x=130, y=255)
		self.master.ComboStatus.bind('<Button-1>', editCombo)
		self.master.Label = Label(self.master, text='Home:', fg='red').place(x=20, y=285)
		self.master.Label = Label(self.master, text='F2:', fg='red').place(x=20, y=305)
		self.master.Label = Label(self.master, text='Hide/Display program').place(x=67, y=285)
		self.master.Label = Label(self.master, text='Start to insert keyboard settings').place(x=67, y=305)
		self.master.Run = ttk.Button(self.master, width=10, text='Save', state="disabled", command=self.submit)
		self.master.Run.place(x=255, y=318)
	def Home_key(self):
		if self.master.state() == 'normal':
			self.master.withdraw()
		elif self.master.state() == 'withdrawn':
			self.master.deiconify()
	def cc(self):
		global color
		color = askcolor()[1]
		if not color:
			globals().pop('color', None)
		try: self.master.TF_1['foreground'] = color
		except: pass
		try: self.master.TF_2['foreground'] = color
		except: pass
		try: self.master.TF_3['foreground'] = color
		except: pass
		try: self.master.TF_4['foreground'] = color
		except: pass
		try: self.master.TF_5['foreground'] = color
		except: pass
	def save_Text1(self):	
		if self.master.TF_1.get():
			self.master.Tag1.config(text=self.master.TF_1.get())
			self.master.Tag1['fg'] = det_color('1')
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark1', self.master.TF_1.get())
		self.master.TF_1.destroy()
		self.master.Color1.destroy()
		self.master.Done1.destroy()
	def save_Text2(self):
		if self.master.TF_2.get():
			self.master.Tag2.config(text=self.master.TF_2.get())
			self.master.Tag2['fg'] = det_color('2')
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark2', self.master.TF_2.get())
		self.master.TF_2.destroy()
		self.master.Color2.destroy()
		self.master.Done2.destroy()
	def save_Text3(self):
		if self.master.TF_3.get():
			self.master.Tag3.config(text=self.master.TF_3.get())
			self.master.Tag3['fg'] = det_color('3')
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark3', self.master.TF_3.get())
		self.master.TF_3.destroy()
		self.master.Color3.destroy()
		self.master.Done3.destroy()
	def save_Text4(self):
		if self.master.TF_4.get():
			self.master.Tag4.config(text=self.master.TF_4.get())
			self.master.Tag4['fg'] = det_color('4')
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark4', self.master.TF_4.get())
		self.master.TF_4.destroy()
		self.master.Color4.destroy()
		self.master.Done4.destroy()
	def save_Text5(self):
		if self.master.TF_5.get():
			self.master.Tag5.config(text=self.master.TF_5.get())
			self.master.Tag5['fg'] = det_color('5')
			Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'Text_mark5', self.master.TF_5.get())
		self.master.TF_5.destroy()
		self.master.Color5.destroy()
		self.master.Done5.destroy()
	def save_Combo(self):
		comboText = self.master.TF_6.get()
		if '>' not in comboText or len(comboText) < 3 or comboText.count(' ') != 0:
			showerror('ERROR', 'Oops! Invalid format of keyboard combo.')
			self.master.TF_6.destroy()
			self.master.Done6.destroy()
			return(False)
		self.master.ComboStatus.config(text=self.master.TF_6.get())
		Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'comboset', self.master.TF_6.get())
		self.master.TF_6.destroy()
		self.master.Done6.destroy()
	def submit(self):
		restore_key('F2')
		TF_list = [self.master.TF1.get() + ';' + self.master.TF2.get(), self.master.TF3.get() + ';' + self.master.TF4.get(),
				   self.master.TF5.get() + ';' + self.master.TF6.get(), self.master.TF7.get() + ';' + self.master.TF8.get(),
				   self.master.TF9.get() + ';' + self.master.TF10.get(),
				   ]
		Registrar('set', r'HKEY_CURRENT_USER\Software\QKpasswd', 'profile{}'.format(self.master.CheckVar.get()), TF_list[self.master.CheckVar.get()-1])
		keyboard.add_hotkey('F2', lambda: kb_action(TF_list[self.master.CheckVar.get()-1].split(';')[0], TF_list[self.master.CheckVar.get()-1].split(';')[1], self.master.ComboStatus['text']))

if __name__ == '__main__':
	RegistryPrep()
	root = Tk()
	app = Windows(master=root)
	app.mainloop()
