#!/usr/bin/python3
import platform
from shutil import move, rmtree
from subprocess import getoutput
from os import getcwd, listdir, remove, system
from os.path import isfile, basename, dirname
OS = platform.system()
if OS == 'Linux':
	if getoutput('dpkg --get-selections python3-tk | awk \'{print $2}\'') != 'install':
		system('xterm -title \'Installing python3-tk\' -e \'sudo apt-get install python3-tk -y && exit\'')
	sysConfig = {'Inspyinscmd':'xterm -title \'Installing pyinstaller\' -e \'sudo pip3 install pyinstaller && exit\'', 'pipcmd':'pip3', 'icobit':'', 'path_split':'/', 'exe_file':'', 'window_w':440, 'Select1_w':407, 'display_w': 75, 'display_h':106, 'compiler_w':340}
elif OS == 'Windows':
	sysConfig = {'Inspyinscmd':'pip install pyinstaller', 'pipcmd':'pip', 'icobit':'.', 'path_split':'\\', 'exe_file':'.exe', 'window_w':400, 'Select1_w':370, 'display_w': 60, 'display_h':105, 'compiler_w':300}
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showerror, askquestion
from tkinter import ttk, Tk, Label, Frame, IntVar, StringVar
def Check_Package(pkg=''):
	if not isfile('/usr/bin/pip3') and OS == 'Linux':
		showinfo('Notice', 'python3-pip is not found, download starting...')
		system('xterm -title \'Installing python3-pip\' -e \'sudo apt-get install python3-pip -y && exit\'')
	packages = getoutput('{0} list'.format(sysConfig['pipcmd'])).split('\n')
	target_pkg = []
	for item in sorted(packages):
		if pkg in item:
			target_pkg.append(item)
	print(target_pkg)
	if target_pkg == []:
		showinfo('Notice', 'PyInstaller is not found, download starting...')
		if system(sysConfig['Inspyinscmd']):
			showerror('ERROR', 'Download PyInstaller failed.')
			if OS == 'Linux':
				showinfo('Notice', 'If occure failed again, please use terminal, then try \'./PytoExe_w\' to execute program.')
			return(False)
		else:
			return(True)
	else:
		return(True)
def RecordLog(ERRMSG=''):
	try:
		showerror('ERROR', 'Oops! There is unexpected error occured.')
		if isfile('ERRMessage.log'):
			action = 'a'
		else:
			action = 'w'
		with open('ERRMessage.log', action) as wlog:
			wlog.write(str(ERRMSG))
	except IOError as ioerr:
		pass
		showerror('ERROR', '{0}'.format(str(ioerr)))
def Convert_EXE(window=1, icon='', script='', resource=0):
	if window == 1:
		w = ''
	else:
		w = '-w'
	if isfile(icon):
		ico_img = '-i {}'.format(basename(icon))
	else:
		ico_img = icon
	try:
		print('pyinstaller -F {0} {1} {2}'.format(w, ico_img, script))
		detectFile = '{0}{1}{2}'.format(getcwd(), sysConfig['path_split'], script.replace('.py', sysConfig['exe_file']))
		if isfile(detectFile):
			if askquestion('FILE EXISTS', 'File: {} is exists, do you want to remove it ?'.format(script.replace('.py', sysConfig['exe_file']))) == 'yes':
				remove(detectFile)
			else:
				return('Canceled')
		if OS == 'Linux':
			system('xterm -title \'Converting {2}\' -e \'pyinstaller -F {0} {1} {2}\''.format(w, ico_img, script))
		elif OS == 'Windows':
			system('pyinstaller -F {1} {2} {3}'.format(w, ico_img, script), creationflags=0x08000000)
		move('dist/{}'.format(script.replace('.py', sysConfig['exe_file'])), getcwd())
		if resource == 0:
			for rm_f in ['__pycache__', 'build', 'dist']:
				rmtree(rm_f)
			remove(script.replace('.py', '.spec'))
		if isfile(detectFile):
			return('Completed')
		else:
			return('Failed')
	except Exception as err:
		RecordLog(err)
		pass
		return('Failed')
def GetSubFileName(subn=''):
	try:
		file_lst = []
		for f in listdir(getcwd()):
			if subn in f:
				file_lst.append(f)
		if 'PytoExe_w.py' in file_lst:
			file_lst.remove('PytoExe_w.py')
		return(file_lst)
	except Exception as err:
		RecordLog(err)
		pass
class Windows(Frame):
	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)
		self.master.title('PytoEXE      Support Ver : Python3.5 (less)')
		self.master.geometry('{0}x145'.format(str(sysConfig['window_w'])))
		self.master.resizable(0, 0)
		self.master.iconbitmap(default=sysConfig['icobit'])
		self.createWidgets()
	def createWidgets(self):
		self.master.LB = Label(self.master, text="Script file : ", fg="blue")
		self.master.LB.place(x=10, y=15)
		self.master.Run = ttk.Button(self.master, text='Compiler', command=self.compiler)
		self.master.Run.config(state="disabled")
		self.master.Run.place(x=sysConfig['compiler_w'], y=105)
		self.master.displayText = Label(self.master, text="Execution message", fg="brown")
		self.master.displayText.place(x=sysConfig['display_w'], y=sysConfig['display_h'])
		def entry_event(tf_event):
			if isfile(self.master.TF1.get()):
				self.master.Run.config(state="normal")
			else:
				self.master.Run.config(state="disabled")
		tf_event = StringVar()
		tf_event.trace("w", lambda name, index, mode, tf_event=tf_event: entry_event(tf_event))
		self.master.TF1 = ttk.Entry(self.master, width=39, textvariable=tf_event)
		try:
			self.master.TF1.insert(0, r'{0}{1}{2}'.format(getcwd(), sysConfig['path_split'], GetSubFileName('.py')[0]))
		except IndexError as idxerr:
			showerror('ERROR', 'Python script is not found.')
			self.master.displayText["text"] = '{}'.format(idxerr)
			pass
		self.master.TF1.config(state='readonly')
		self.master.TF1.place(x=80, y=15)
		self.master.LB = Label(self.master, text="EXE Icon : ", fg="blue")
		self.master.LB.place(x=10, y=45)
		self.master.TF2 = ttk.Entry(self.master, width=39)
		try:
			self.master.TF2.insert(0, r'{0}{1}{2}'.format(getcwd(), sysConfig['path_split'], GetSubFileName('.ico')[0]))
		except IndexError as idxerr:
			self.master.displayText["text"] = '{}'.format(idxerr)
			pass
		self.master.TF2.config(state='readonly')
		self.master.TF2.place(x=80, y=45)
		self.master.Select1 = ttk.Button(self.master, text='..', width=1, command=self.selectPyFile)
		self.master.Select1.place(x=sysConfig['Select1_w'], y=14)
		self.master.Select2 = ttk.Button(self.master, text='..', width=1, command=self.selectIcoFile)
		self.master.Select2.place(x=sysConfig['Select1_w'], y=44)
		self.master.LB = Label(self.master, text="Option : ", fg="blue")
		self.master.LB.place(x=10, y=75)
		self.master.CheckVar1 = IntVar()
		self.master.CheckVar2 = IntVar()
		self.master.CheckVar3 = IntVar()
		self.master.CB1 = ttk.Checkbutton(self.master, text='Icon', variable=self.master.CheckVar1, onvalue=1, offvalue=0, command=lambda : self.master.displayText.config(text='option Icon checked') if self.master.CheckVar1.get() == 1 else self.master.displayText.config(text='option Icon canceled'))
		self.master.CB1.place(x=80, y=76)
		self.master.CB2 = ttk.Checkbutton(self.master, text='Window', variable=self.master.CheckVar2, onvalue=1, offvalue=0, command=lambda : self.master.displayText.config(text='option Window checked') if self.master.CheckVar2.get() == 1 else self.master.displayText.config(text='option Window canceled'))
		self.master.CB2.place(x=140, y=76)
		self.master.CB3 = ttk.Checkbutton(self.master, text='Resource', variable=self.master.CheckVar3, onvalue=1, offvalue=0, command=lambda : self.master.displayText.config(text='option Resource checked') if self.master.CheckVar3.get() == 1 else self.master.displayText.config(text='option Resource canceled'))
		self.master.CB3.place(x=220, y=76)
		self.master.LB = Label(self.master, text="Status : ", fg="blue")
		self.master.LB.place(x=10, y=105)
	def compiler(self):
		scriptName = basename(self.master.TF1.get())
		if Check_Package('PyInstaller'):
			if self.master.CheckVar1.get() == 1:
				iconImage = self.master.TF2.get()
			else:
				iconImage = ''
			Result = Convert_EXE(self.master.CheckVar2.get(), iconImage, scriptName, self.master.CheckVar3.get())
			self.master.displayText["text"] = '{0} convert {1}.'.format(scriptName, Result)
	def selectPyFile(self):
		script = askopenfilename(parent=self.master, initialdir=getcwd(), filetypes=[("Python file",'*.py')]).replace('/', sysConfig['path_split'])
		if script:
			if dirname(r'{0}{1}{2}'.format(getcwd(), sysConfig['path_split'], basename(__file__))) == dirname(script):
				self.master.displayText["text"] = 'Script {} selected'.format(basename(script))
				self.master.TF1.config(state='NORMAL')
				self.master.TF1.delete(0, 'end')
				self.master.TF1.insert(0, script)
				self.master.TF1.config(state='readonly')
			elif dirname(r'{0}{1}{2}'.format(getcwd(), sysConfig['path_split'], basename(__file__))) != dirname(script):
				showerror('ERROR', 'Select script only in currently directory.')
	def selectIcoFile(self):
		icon = askopenfilename(parent=self.master, initialdir=getcwd(), filetypes=[("Icon file",'*.ico')]).replace('/', sysConfig['path_split'])
		if icon:
			if dirname(r'{0}{1}{2}'.format(getcwd(), sysConfig['path_split'], basename(__file__))) == dirname(icon):
				self.master.displayText["text"] = 'Icon {} selected'.format(basename(icon))
				self.master.TF2.config(state='NORMAL')
				self.master.TF2.delete(0, 'end')
				self.master.TF2.insert(0, icon)
				self.master.TF2.config(state='readonly')
			elif dirname(r'{0}{1}{2}'.format(getcwd(), sysConfig['path_split'], basename(__file__))) != dirname(icon):
				showerror('ERROR', 'Select icon only in currently directory.')
if __name__ == '__main__':
	root = Tk()
	app = Windows(master=root)
	app.mainloop()