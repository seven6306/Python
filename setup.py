from time import sleep
from zipfile import ZipFile
from shutil import copy, rmtree
from pythoncom import CoInitialize
from win32com.client import Dispatch
from win32pdh import EnumObjects, EnumObjectItems
from os import getcwd, environ, remove, rename
from os.path import join, isfile, isdir, basename, dirname
from threading import Thread, active_count
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showinfo, askyesno
from tkinter import ttk, Tk, Frame, Label, Text, Toplevel, INSERT, HORIZONTAL
from winreg import OpenKey, CreateKey, KEY_ALL_ACCESS, QueryValueEx, SetValueEx, REG_SZ, HKEY_CURRENT_USER, DeleteKey, DeleteValue

fileName = 'TPbuilder.exe'
Desktop = join('C:' + environ["HOMEPATH"], 'Desktop')
def CheckSetup(Path=''):
	if not isfile(join(Desktop, 'TPbuilder.lnk')):
		return(False)
	if not isfile(join(Path, 'models.json')):
		return(False)
	for each_file in ['Fortilogo.ico', 'Fortilogo.gif']:
		if not isfile(join(join(Path, 'image'), each_file)):
			return(False)
	return(True)
def getProcesses(ProcessList=[], all=1):
	templist = []
	for each_process in ProcessList:
		EnumObjects(None, None, 0, 1)
		(items, instance) = EnumObjectItems(None, None, "Process", -1)
		if each_process in instance:
			templist.append(each_process)
	if all == 0:
		return(instance)
	else:
		return(templist)
def Realeasepkg(pkg='', dest=''):
	if isfile(pkg):
		package = pkg + '.zip'
		copy(pkg, package)
		try:
			with ZipFile(package) as zipf:
				zipf.extractall(dest, pwd=b'P)h>@6aWAK2mm&gW=RK-r8gW8002}h000jF003}la4%n9X>MtBUtcb8d8JxybK5o&{;pqv$n}tHC^l~')
			remove(package)
		except IOError as ioerr:
			showerror('ERROR', str(ioerr))
def Registrar(Action='get', RegPath='', RegName='', RegValue=''):
	try:
		ClassDict = {'HKEY_CURRENT_USER':HKEY_CURRENT_USER}
		mainkey = RegPath.split('\\')[0]
		RegRelativePath = RegPath.replace(mainkey + '\\', '')
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
			elif Action == 'rmvalue':
				DeleteValue(key, RegName)
			elif Action == 'rmkey':
				DeleteKey(ClassDict[mainkey], join(RegRelativePath, RegName))
	except FileNotFoundError as regerr:
		pass
def createShortcut(fileName):
	try:
		CoInitialize()
		winscript = Dispatch("wscript.shell")
		link = join(Desktop, fileName.replace('.exe', '.lnk'))
		if isfile(link):
			remove(link)
		shortcut = winscript.CreateShortcut(link)
		shortcut.TargetPath = '\"{0}\"'.format(join(installPath, fileName))
		shortcut.Save()
	except Exception as err:
		showerror('ERROR', str(err))
def isAlive(logic=None, threadNum=0):
	while(True):
		if logic == 'lt':
			if active_count() < threadNum:
				break
		elif logic == 'gt':
			if active_count() > threadNum:
				break
		sleep(0.5)
class MultiProcess(Thread):
	def __init__(self, action, event, delay):
		Thread.__init__(self)
		self.action = action
		self.event = event
		self.delay = delay
	def run(self):
		ProcessAction(self.action, self.event, self.delay)
def ProcessAction(action=None, event=None, delay=0):
	global fileName
	global installPath
	if action == 'create':
		if event == 'Install':
			Realeasepkg(join(getcwd(), 'package'), installPath)
			createShortcut(fileName)
			Registrar('setkey', r'HKEY_CURRENT_USER\Software', 'TPbuilder')
			Registrar('set', r'HKEY_CURRENT_USER\Software\TPbuilder', 'TBPath', join(installPath, 'image'))
		elif event == 'Uninstall':
			if isdir(installPath):
				try:
					rmtree(installPath)
				except:
					pass
			if isfile(join(Desktop, 'TPbuilder.lnk')):
				remove(join(Desktop, 'TPbuilder.lnk'))
			Registrar('rmvalue', r'HKEY_CURRENT_USER\Software\TPbuilder', 'TBPath')
			Registrar('rmkey', r'HKEY_CURRENT_USER\Software', 'TPbuilder')
	else:
		ProgressBar(delay, event)
		root.withdraw()
		Finish(event)
class ProgressBar(Toplevel):
	def __init__(self, delay, event):
		Toplevel.__init__(self)
		self.event = event
		self.delay = delay
		self.geometry('400x48+470+420')
		self.resizable(0, 0)
		self.focus()
		self.grab_set()
		self.createWidgets()
	def createWidgets(self):
		self.progress = ttk.Progressbar(self, orient=HORIZONTAL, length=400, mode='determinate')
		self.progress.place(x=0, y=0)
		self.BT = ttk.Button(self, style="TButton", text='Run')
		self.BT.place(x=168, y=22)
		self.title('{0}ing TPbuilder'.format(self.event))
		def close_E():
			self.title('Do not close window while {0}ing'.format(self.event.lower()))
		self.protocol('WM_DELETE_WINDOW', close_E)
		self.config(cursor="wait")
		self.BT.config(state="normal", text='Run')
		ttk.Style().configure("TButton", foreground="blue")
		for count in range(101):
			if count >= 1:
				self.progress['value'] = count
				self.BT['text'] = str(count) + '%'
				self.update_idletasks()
				sleep(self.delay)
				if self.progress['value'] == 99:
					isAlive('lt', 3)
		self.config(cursor="")
		ttk.Style().configure("TButton", foreground="black")
		self.BT.config(state="normal", text='Complete')
		sleep(1)
		showinfo('Information', 'TPbuilder has been {0}ed'.format(self.event.lower()))
		self.destroy()
class Finish(Toplevel):
	def __init__(self, event):
		Toplevel.__init__(self)
		self.event = event
		self.title('TPbuilder Setup')
		self.geometry('450x250+450+300')
		self.resizable(0, 0)
		if isfile(join(getcwd(), 'install.ico')):
			self.iconbitmap(default=join(getcwd(), 'install.ico'))
		self.createWidgets()
		self.protocol('WM_DELETE_WINDOW', root.quit)
	def createWidgets(self):
		self.TA = Text(self, height=5, width=65, bg='#FFFFFF', cursor='', selectbackground='#FFFFFF')
		self.TA.config(state='disabled')
		self.TA.place(x=-5, y=0)
		self.LB = Label(self, text="Finish {0}".format(self.event), font='Calibri 11 bold', bg='#FFFFFF')
		self.LB.place(x=10, y=10)
		self.LB2 = Label(self, text="At last {0} complete!".format(self.event))
		if self.event == 'Uninstall':
			global insDir
			LBText = "    TPbuilder has been removed, click Finish to exit."
			self.LB1 = Label(self, text="Removed item listed:")
			self.LB1.place(x=15, y=71)
			self.TA1 = Text(self, height=6, width=47, bg='#FFFFFF', cursor='')
			self.TA1.insert(INSERT, join(Desktop, 'TPbuilder.lnk') + '\n')
			self.TA1.insert(INSERT, join(insDir, 'TPbuilder.exe') + '\n')
			self.TA1.insert(INSERT, join(insDir, 'models.json') + '\n')
			self.TA1.insert(INSERT, join(insDir, 'image') + '\n')
			self.TA1.insert(INSERT, join(insDir, 'uninstall.exe') + '\n')
			self.TA1.insert(INSERT, insDir)
			self.TA1.config(state='disabled')
			self.TA1.place(x=15, y=93)
			self.LB2.place(x=15, y=176)
		else:
			LBText = "    TPbuilder has been installed, click Finish to exit."
			self.LB2.place(x=15, y=77)
		self.LB = Label(self, text=LBText, font='Calibri 10', bg='#FFFFFF')
		self.LB.place(x=10, y=37)
		self.Spline1 = ttk.Separator(self, orient=HORIZONTAL)
		self.Spline1.place(x=0, y=67, width=450)
		self.Spline2 = ttk.Separator(self, orient=HORIZONTAL)
		self.Spline2.place(x=0, y=200, width=450)
		self.BT2 = ttk.Button(self, text='Finish', command=root.quit)
		def KeyPress_F(event):
			root.quit()
		self.BT2.bind("<KeyPress-F>", KeyPress_F)
		self.BT2.bind("<KeyPress-f>", KeyPress_F)
		self.BT2.place(x=340, y=213)
class Windows(Frame):
	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)
		self.master.title('TPbuilder Setup')
		self.master.geometry('450x250+450+300')
		self.master.resizable(0, 0)
		if isfile(join(getcwd(), 'install.ico')):
			self.master.iconbitmap(default=join(getcwd(), 'install.ico'))
		self.createWidgets()
		self.master.protocol('WM_DELETE_WINDOW', self.cancel)
	def createWidgets(self):
		global insDir
		try:
			insDir = dirname(Registrar('get', r'HKEY_CURRENT_USER\Software\TPbuilder', 'TBPath'))
		except:
			insDir = ''
		if CheckSetup(insDir):
			LBText1 = "Remove TPbuilder"
			LBText2 = "    Click Next to uninstall TPbuilder or click Cancel to exit."
			self.master.LB = Label(self.master, text="TPbuilder installed path: ")
			self.master.LB.place(x=15, y=77)
			self.master.TF1 = ttk.Entry(self.master, width=57)
			self.master.TF1.insert(0, insDir)
			self.master.TF1.config(state='readonly')
			self.master.TF1.place(x=19, y=102)
			self.master.BT1 = ttk.Button(self.master, text='Next', command=self.exeUninstall)
			def KeyPress_N(event):
				self.exeUninstall()
			self.master.BT1.place(x=240, y=213)
		else:
			LBText1 = "Destination Folder"
			LBText2 = "    Click Next to install to the default folder or click Change to choose another."
			self.master.LB = Label(self.master, text="Install TPbuilder to: ")
			self.master.LB.place(x=15, y=77)
			self.master.TF1 = ttk.Entry(self.master, width=57)
			self.master.TF1.insert(0, 'C:\\Program Files\\TPbuilder')
			self.master.TF1.place(x=19, y=102)
			self.master.BT0 = ttk.Button(self.master, text='Change...', command=self.selectPath)
			self.master.BT0.place(x=19, y=130)
			self.master.BT1 = ttk.Button(self.master, text='Next', command=self.exeInstall)
			def KeyPress_N(event):
				self.exeInstall()
			self.master.BT1.place(x=240, y=213)
		self.master.BT1.bind("<KeyPress-N>", KeyPress_N)
		self.master.BT1.bind("<KeyPress-n>", KeyPress_N)
		self.master.TA = Text(self.master, height=5, width=65, bg='#FFFFFF', cursor='', selectbackground='#FFFFFF')
		self.master.TA.config(state='disabled')
		self.master.TA.place(x=-5, y=0)
		self.master.LB = Label(self.master, text=LBText1, font='Calibri 11 bold', bg='#FFFFFF')
		self.master.LB.place(x=10, y=10)
		self.master.LB = Label(self.master, text=LBText2, font='Calibri 10', bg='#FFFFFF')
		self.master.LB.place(x=10, y=37)
		self.master.Spline1 = ttk.Separator(self.master, orient=HORIZONTAL)
		self.master.Spline1.place(x=0, y=67, width=450)
		self.master.Spline2 = ttk.Separator(self.master, orient=HORIZONTAL)
		self.master.Spline2.place(x=0, y=200, width=450)
		self.master.BT2 = ttk.Button(self.master, text='Cancel', command=self.cancel)
		def KeyPress_C(event):
			self.cancel()
		self.master.BT2.bind("<KeyPress-C>", KeyPress_C)
		self.master.BT2.bind("<KeyPress-c>", KeyPress_C)
		self.master.BT2.place(x=340, y=213)
	def selectPath(self):
		Path = askdirectory(parent=self.master, initialdir='C:\\Program Files\\', title='Select Install Directory').replace('/', '\\')
		if Path:
			self.master.TF1.delete(0, 'end')
			self.master.TF1.insert(0, join(Path, 'TPbuilder'))
	def exeInstall(self):
		if not isdir(dirname(self.master.TF1.get())):
			showerror('ERROR', 'Invalid installation path')
			return(False)
		if not isfile(join(getcwd(), 'package')):
			showerror('ERROR', 'Install package lost')
			return(False)
		global installPath
		installPath = self.master.TF1.get()
		if askyesno('TPbuilder Setup', 'Next will be install TPbuilder?', icon='warning'):
			thread_1 = MultiProcess('create', 'Install', 0)
			thread_2 = MultiProcess('progress', 'Install', 0.08)
			thread_1.start()
			thread_2.start()
	def exeUninstall(self):
		global installPath
		installPath = self.master.TF1.get()
		if askyesno('TPbuilder Setup', 'Are you sure you want to uninstall it?', icon='warning'):
			if getProcesses(['TPbuilder'], 0).count('TPbuilder') == 0:
				thread_1 = MultiProcess('create', 'Uninstall', 0)
				thread_2 = MultiProcess('progress', 'Uninstall', 0.08)
				thread_1.start()
				thread_2.start()
			else:
				showerror('ERROR', 'Please close TPbuilder.exe then try again')
	def cancel(self):
		if askyesno('TPbuilder Setup', 'Are you sure you want to cancel TPbuilder installation?'):
			self.master.quit()
if __name__ == '__main__':
	root = Tk()
	app = Windows(master=root)
	root.withdraw()
	if getProcesses(['Setup'], 0).count('Setup') in [0, 2]:
		root.deiconify()
		app.mainloop()
	else:
		showerror('ERROR', 'Setup.exe is already executing')