from re import search
from json import load
from time import sleep
from hashlib import md5
from datetime import datetime
from shutil import move, rmtree
from webbrowser import open as web
from win32com.client import Dispatch
from zipfile import ZipFile, ZIP_DEFLATED
from threading import Thread, active_count
from win32pdh import EnumObjects, EnumObjectItems
from os.path import join, isfile, dirname, basename
from os import mkdir, listdir, remove, walk, chdir, environ
from winreg import OpenKey, KEY_ALL_ACCESS, QueryValueEx, HKEY_CURRENT_USER
from tkinter.simpledialog import askstring as InputBox
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import ttk, Tk, Label, Frame, IntVar, StringVar, PhotoImage, Toplevel, HORIZONTAL

debug_config_build = {}
debug_config_extract = {}
DownloadInfo = """
===============================
OS Image download support below listed only:
===============================
      FAP  -  FortiAP
      FML  -  FortiMail
      FDD  -  FortiDDoS
      FMG  -  FortiManager
      FAZ  -  FortiAnalyzer
      FSW  -  FortiSwitchOS
      FAC  -  FortiAuthenticator
===============================
"""
def Registrar(RegPath='', RegName=''):
	try:
		with OpenKey(HKEY_CURRENT_USER, RegPath, 0, KEY_ALL_ACCESS) as key:
			value = QueryValueEx(key, RegName)[0]
			return(value)
	except FileNotFoundError as regerr:
		return('')
		pass
ImagePath = Registrar(r'Software\TPbuilder', 'TBPath')
def CheckSetup():
	Desktop = join('C:' + environ["HOMEPATH"], 'Desktop')
	if not isfile(join(Desktop, 'TPbuilder.lnk')):
		return(False)
	if not isfile(join(dirname(ImagePath), 'models.json')):
		return(False)
	for each_file in ['Fortilogo.ico', 'Fortilogo.gif']:
		if not isfile(join(ImagePath, each_file)):
			return(False)
	return(True)
class MultiProcess(Thread):
	def __init__(self, action, context, times, percent, delay):
		Thread.__init__(self)
		self.action = action
		self.context = context
		self.times = times
		self.percent = percent
		self.delay = delay
	def run(self):
		ProcessAction(self.action, self.context, self.times, self.percent, self.delay)
def ProcessAction(action=None, context='', times=0, percent=0, delay=0.1):
	global debug_config_build
	global debug_config_extract
	if action == 'progress':
		runbar = TopLV(action, context, times, percent, delay)
	elif action == 'build':
		debug_config_build = app.build()
	elif action == 'extract':
		debug_config_extract = app.extract()
def isAlive(logic=None, threadNum=0):
	while(True):
		if logic == 'lt':
			if active_count() < threadNum:
				break
		elif logic == 'gt':
			if active_count() > threadNum:
				break
		sleep(0.5)
class TopLV(Toplevel):
	def __init__(self, action, context, times, percent, delay):
		Toplevel.__init__(self)
		self.action = action
		self.context = context
		self.times = times
		self.percent = percent
		self.delay = delay
		self.title(self.context[0].upper() + self.context[1:] + 'ing')
		self.geometry('400x48+470+420')
		self.resizable(0, 0)
		self.focus()
		self.grab_set()
		def close_E():
			self.title('DON\'T CLOSE WINDOW while {0}ing'.format(self.context))
		self.protocol('WM_DELETE_WINDOW', close_E)
		global debug_config_build
		global debug_config_extract
		self.progress = ttk.Progressbar(self, orient=HORIZONTAL, length=400, mode='determinate')
		self.progress.place(x=0, y=0)
		self.BT2 = ttk.Button(self, style="TButton", text='Run')
		self.BT2.place(x=168, y=22)
		self.config(cursor="wait")
		self.BT2.config(state="normal", text='Run')
		ttk.Style().configure("TButton", foreground="blue")
		for count in range(self.times):
			if count >= 1:
				self.progress['value'] = count * self.percent
				self.BT2['text'] = str(count * self.percent) + '%'
				self.update_idletasks()
				self.title(self.context[0].upper() + self.context[1:] + 'ing')
				sleep(self.delay)
				if self.progress['value'] == 99:
					isAlive('lt', 3)
		self.config(cursor="")
		ttk.Style().configure("TButton", foreground="black")
		self.BT2.config(state="normal", text='Complete')
		sleep(1)
		if self.context == 'build':
			showinfo('Information', 'Test Package: \"{0}\"\nhas been created at \"{1}\"'.format(basename(debug_config_build['TPQAzip']), debug_config_build['ProjectDir']))
			self.master.displayText["text"] = '{0} has been created'.format(basename(debug_config_build['TPQAzip']))
		elif self.context == 'extract':
			showinfo('Information', 'Test Package: \"{0}\"\nextract completed'.format(debug_config_extract['zipFile1']))
			self.master.displayText["text"] = '{0} extract completed'.format(debug_config_extract['zipFile1'])
		self.destroy()
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
def checkDateformat(date=''):
	if not search('^20\d{2}[0-1][0-9][0-3]\d$', date) or int(date[4:6]) > 12 or int(date[4:6]) == 0 or int(date[6:8]) == 0:
		return(False)
	elif int(date[4:6]) == 2 and int(date[6:8]) > 28:
		return(False)
	elif int(date[4:6]) in [1, 3, 5, 7, 8, 10, 12] and int(date[6:8]) > 31:
		return(False)
	elif int(date[4:6]) in [4, 6, 9, 11] and int(date[6:8]) > 30:
		return(False)
	return(True)
def getData(fileName='', reg='', action='r'):
	try:
		with open(fileName, action) as output:
			if action == 'r':
				for each_line in output.read().split('\n'):
					if search(reg, each_line):
						return(each_line)
			else:
				output.write(reg)
	except IOError as ioerr:
		pass
		self.master.displayText["text"] = str(ioerr)
		showerror('ERROR', str(ioerr))
def getJsonData(fileName=''):
	try:
		with open(fileName) as jsrf:
			jdata = load(jsrf)
			return(jdata)
	except IOError as ioerr:
		pass
		showerror('ERROR', str(ioerr))
def getWordData(fileName='', row=0, column=0):
	try:
		word = Dispatch("Word.Application")
		word.Visible = 0
		word.Documents.Open(fileName)
		docx = word.ActiveDocument
		table = docx.Tables(1)
		text = table.Cell(Row=row, Column=column).Range.Text
		if 'WINWORD' in getProcesses(['WINWORD']):
			docx.Close(SaveChanges=0)
			word.Quit()
		return(text)
	except Exception as err:
		pass
		self.master.displayText["text"] = str(err)
		showerror('ERROR', str(err))
def md5checksums(fileName=''):
	checksum = md5()
	try:
		with open(fileName,"rb") as encode:
			data = encode.read()
			checksum.update(data)
			return(checksum.hexdigest())
	except IOError as ioerr:
		self.master.displayText["text"] = str(ioerr)
		showerror('ERROR', str(ioerr))
		return(False)
def createQATestpkg(named='', dirList=[]):
	temp_ver = 1
	range = '0'
	while(True):
		if temp_ver >= 10:
			range = ''
		if '{0}{1}{2}.zip'.format(named, range, str(temp_ver)) in dirList:
			temp_ver = temp_ver + 1
		else:
			if temp_ver < 10:
				return('{0}0{1}'.format(named, str(temp_ver)))
			elif temp_ver >= 10:
				return('{0}{1}'.format(named, str(temp_ver)))
def zipSpecifyFile(zipName='default.zip', action='compress', fullPath=''):
	if action == 'compress':
		path = basename(fullPath) + '\\'
		chdir(dirname(fullPath))
		with ZipFile(zipName, 'w', ZIP_DEFLATED) as zipf:
			for root, dir, files in walk(path):
				for each_file in files:
					file_path = join(root, each_file)
					zipf.write(file_path)
					#print(r'Compressing {0} to {1}'.format(file_path, zipName))
			return(join(dirname(fullPath), zipName))
	else:
		with ZipFile(zipName) as zipf:
			if fullPath != '':
				zipf.extractall(fullPath)
			else:
				zipf.extractall(dirname(zipName))
class Windows(Frame):
	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)
		self.master.title('TP Builder   Support Ver : Python3.5 (less)')
		self.master.geometry('400x225')
		self.master.resizable(0, 0)
		if isfile(join(ImagePath, 'Fortilogo.ico')):
			self.master.iconbitmap(default=join(ImagePath, 'Fortilogo.ico'))
		self.createWidgets()
	def createWidgets(self):
		self.master.LB = Label(self.master, text="TP Path : ", fg="blue")
		self.master.LB.place(x=10, y=15)
		self.master.LB = Label(self.master, text="MD5 : ", fg="blue")
		self.master.LB.place(x=10, y=48)
		self.master.Run = ttk.Button(self.master, text='Build', command=self.buildProgress)
		self.master.Run.config(state="disabled")
		self.master.Run.place(x=300, y=138)
		self.master.Ext = ttk.Button(self.master, text='Extract', command=self.extractProgress)
		self.master.Ext.place(x=210, y=138)
		self.master.OSImage = ttk.Button(self.master, text='Download', command=self.openInfosite)
		self.master.OSImage.config(state="disabled")
		self.master.OSImage.place(x=120, y=138)
		self.master.LB = Label(self.master, text="OS Image:", fg="blue")
		self.master.LB.place(x=10, y=80)
		self.master.LB = Label(self.master, text="Status : ", fg="blue")
		self.master.LB.place(x=10, y=110)
		self.master.displayText = Label(self.master, text="Execution message", fg="brown")
		self.master.displayText.place(x=67, y=111)
		self.master.CheckVar1 = IntVar()
		self.master.CB1 = ttk.Checkbutton(self.master, text='Set Date', variable=self.master.CheckVar1, onvalue=1, offvalue=0, command=lambda : self.master.displayText.config(text='Customize date checked') if self.master.CheckVar1.get() == 1 else self.master.displayText.config(text='Customize date canceled'))
		self.master.CB1.config(state="disabled")
		self.master.CB1.place(x=14, y=140)
		def entry_event_run(tf_event1):
			if not isfile(self.master.TF1.get()):
				self.master.Run.config(state="normal")
				self.master.CB1.config(state="normal")
			else:
				self.master.Run.config(state="disabled")
				self.master.CB1.config(state="disabled")
		tf_event1 = StringVar()
		tf_event1.trace("w", lambda name, index, mode, tf_event1=tf_event1: entry_event_run(tf_event1))
		def entry_event_img(tf_event2):
			if self.master.TF3.get():
				self.master.OSImage.config(state="normal")
			else:
				self.master.OSImage.config(state="disabled")
		tf_event2 = StringVar()
		tf_event2.trace("w", lambda name, index, mode, tf_event2=tf_event2: entry_event_img(tf_event2))
		self.master.TF1 = ttk.Entry(self.master, width=47, textvariable=tf_event1)
		self.master.TF1.config(state='readonly')
		self.master.TF1.place(x=70, y=16)
		self.master.TF2 = ttk.Entry(self.master, width=47)
		self.master.TF2.config(state='readonly')
		self.master.TF2.place(x=70, y=49)
		self.master.TF3 = ttk.Entry(self.master, width=47, textvariable=tf_event2)
		self.master.TF3.config(state='readonly')
		self.master.TF3.place(x=70, y=82)
		self.master.Select1 = ttk.Button(self.master, text='..', width=1, command=self.selectAutotest)
		self.master.Select1.place(x=370, y=14)
		self.master.Clipboard = ttk.Button(self.master, text='..', width=1, command=self.copyText)
		self.master.Clipboard.place(x=370, y=47)
		self.master.Select2 = ttk.Button(self.master, text='..', width=1, command=self.selectRequestform)
		self.master.Select2.place(x=370, y=80)
		if isfile(join(ImagePath, 'Fortilogo.gif')):
			banner_img = PhotoImage(file=join(ImagePath, 'Fortilogo.gif'))
			self.master.Fortibanner = Label(self.master, image=banner_img)
			self.master.Fortibanner.photo = banner_img
		else:
			self.master.Fortibanner = Label(self.master)
		self.master.Fortibanner.place(x=0, y=170)
	def build(self):
		self.master.Ext.config(state="disabled")
		self.master.displayText["text"] = 'TP building please wait...'
		Autotest = self.master.TF1.get()
		if Autotest:
			global date
			try:
				ProjectDir = dirname(Autotest)
				fasDir = listdir('{0}\\fas'.format(Autotest))[0]
				ScriptDir = '{0}\\fas\\{1}'.format(Autotest, fasDir)
				for each_file in listdir(ProjectDir):
					if search('^{0}.*signature.csv$'.format(fasDir), each_file):
						Excel = '{0}\\{1}'.format(ProjectDir, each_file)
						break
				if not isfile(Excel):
					showerror('ERROR', 'Requirment: {0} is not found'.format(basename(Excel)))
					self.master.displayText["text"] = 'Requirment: {0} is not found'.format(basename(Excel))
					return(False)
				for each_fas in listdir(ScriptDir):
					if search('^CM-.*\.fas$', each_fas):
						fasScript = each_fas
						break
					else:
						showerror('ERROR', 'fas script is not found')
						self.master.displayText["text"] = 'fas script is not found'
						return(False)
				fasPath = '{0}\\{1}'.format(ScriptDir, fasScript)
				fasVer = getData(fasPath, '^#define.*\%FAS_VERSION\%.*\"$').split('"')[-2].replace('.', '')
				SYSPN = fasScript.split('-')[-1].replace('.fas', '')
				TP = 'Test_Package_{0}_{1}_{2}'.format(fasDir, SYSPN, date)
				TPQA = createQATestpkg('Test_Package_{0}_QA_V{1}_'.format(fasDir, fasVer), listdir(ProjectDir))
				for each_dir in [TP, TPQA]:
					mkdir('{0}\\{1}'.format(ProjectDir, each_dir), 755)
				TPdir = '{0}\\{1}'.format(ProjectDir, TP)
				TPQAdir = '{0}\\{1}'.format(ProjectDir, TPQA)
				for each_file in [Autotest, Excel]:
					move(each_file, TPdir)
				TPzip = zipSpecifyFile(TPdir + '.zip', 'compress', TPdir)
				if isfile(TPzip):
					rmtree(TPdir)
					move(TPzip, TPQAdir)
					TPQAzip = zipSpecifyFile(TPQAdir + '.zip', 'compress', TPQAdir)
					if isfile(TPQAzip):
						rmtree(TPQAdir)
				MD5code = md5checksums(TPQAzip)
				if MD5code:
					getData('{0}\\md5_{1}.txt'.format(ProjectDir, fasDir), 'Model: {0}\nMD5: {1}'.format(fasDir, MD5code), action='w')
					self.master.TF2.config(state='NORMAL')
					self.master.TF2.delete(0, 'end')
					self.master.TF2.insert(0, MD5code)
					self.master.TF2.config(state='readonly')
				global debug_config_build
				debug_config_build = {
					'ProjectDir':ProjectDir, 'Model':fasDir, 'ScriptDir':ScriptDir, 'Excel':Excel,
					'fasScript':fasScript, 'fasFile':fasPath, 'fasVer':fasVer, 'syspn':SYSPN,
					'TP':TP, 'TPQA':TPQA, 'TPdir':TPdir, 'TPQAdir':TPQAdir,
					'TPzip':TPzip, 'TPQAzip':TPQAzip, 'MD5code':MD5code
				}
				self.master.Ext.config(state="normal")
				self.master.CB1.config(state="disabled")
				self.master.Run.config(state="disabled")
				return(debug_config_build)
			except Exception as exerr:
				pass
				self.master.displayText["text"] = str(exerr)
				showerror('ERROR', str(exerr))
	def extract(self):
		global TestPkg1
		self.master.displayText["text"] = '\"{0}  selected\"'.format(TestPkg1)
		zipFile1 = basename(TestPkg1)
		zipDir = dirname(TestPkg1)
		self.master.displayText["text"] = 'Extracting Test Package please wait...'
		self.master.TF1.config(state='NORMAL')
		self.master.TF1.delete(0, 'end')
		self.master.TF1.insert(0, TestPkg1)
		self.master.TF1.config(state='readonly')
		self.master.TF2.config(state='NORMAL')
		self.master.TF2.delete(0, 'end')
		self.master.TF2.config(state='readonly')
		try:
			zipSpecifyFile(TestPkg1, 'extract')
			extDir = '{0}\\{1}'.format(zipDir, zipFile1.replace('.zip', ''))
			zipFile2 = listdir(extDir)[0]
			tempzipFile2 = '{0}\\{1}'.format(extDir, zipFile2)
			if not isfile(tempzipFile2):
				self.master.displayText["text"] = '{0} is not found'.format(tempzipFile2)
				showerror('ERROR', '{0} is not found'.format(tempzipFile2))
			move(tempzipFile2, zipDir)
			TestPkg2 = '{0}\\{1}'.format(zipDir, zipFile2)
			zipSpecifyFile(TestPkg2, 'extract')
			rmtree(extDir)
			remove(TestPkg2)
			global debug_config_extract
			debug_config_extract = {
				'TestPkg1':TestPkg1, 'TestPkg2':TestPkg2,
				'zipFile1':zipFile1, 'zipFile2':zipFile2,
				'zipDir':zipDir, 'extDir':extDir
			}
			return(debug_config_extract)
		except IOError as ioerr:
			pass
			self.master.displayText["text"] = str(ioerr)
			showerror('ERROR', str(ioerr))
	def selectAutotest(self):
		self.master.OSImage.config(state="disabled")
		if askyesno('Notice', 'Make sure each TP file(fas, docx, csv) has been save and close,\nthen pess yes', icon='warning'):
			if len(getProcesses(['WINWORD', 'EXCEL'])) != 0:
				pp = ''
				for each_p in getProcesses(['WINWORD', 'EXCEL']):
					pp = '{0} {1}'.format(pp, each_p.replace('WINWORD', 'WORD')) 
				showerror('ERROR', 'Please close each {0} file before build TP'.format(pp))
				return(False)
			directory = askdirectory(parent=self.master, initialdir='/', title='Select Autotest Directory').replace('/', '\\')
			if directory:
				if not search(r'\\[a|A]utotest$', directory):
					showerror('ERROR', 'Invalid Autotest directory: should be \".\\example\\Autotest\"')
					return(False)
				self.master.displayText["text"] = '\"{0}  selected\"'.format(directory)
				self.master.TF1.config(state='NORMAL')
				self.master.TF1.delete(0, 'end')
				self.master.TF1.insert(0, directory)
				self.master.TF1.config(state='readonly')
	def selectRequestform(self):
		self.master.CB1.config(state="disabled")
		self.master.Run.config(state="disabled")
		if askyesno('Notice', 'Make sure each MS-WORD file(doc, docx)  has been save and close,\nthen pess yes', icon='warning'):
			if len(getProcesses(['WINWORD'])) != 0:
				showerror('ERROR', 'Please close each {0} file before download OS'.format(getProcesses(['WINWORD'])[0].replace('WINWORD', 'WORD')))
				return(False)
			Requestform = askopenfilename(parent=self.master, initialdir='/', title='Select TP-REQUEST-REQUEST FORM-*.docx', filetypes=[("Word",'TP-REQUEST-REQUEST FORM*.docx'), ("Word 97-2003",'TP-REQUEST-REQUEST FORM*.doc')]).replace('/', '\\')
			if Requestform:
				if not search('\w+-TP-REQUEST-REQUEST.*FORM-.*\.doc|docx$', basename(Requestform)):
					showerror('ERROR', 'Invalid TP request form')
					return(False)
				OSInfo = getWordData(Requestform, 4, 4).split('\r')[0]
				strList = basename(Requestform).split('-')
				modelName = '{0}_{1}'.format(strList[-2], strList[-1].replace('.docx', '').replace('.doc', ''))
				self.master.TF3.config(state='NORMAL')
				self.master.TF3.delete(0, 'end')
				self.master.TF3.insert(0, '{0}, {1}'.format(OSInfo, modelName))
				self.master.TF3.config(state='readonly')
				self.master.displayText["text"] = 'Get information, build: {0}, model: {1}'.format(OSInfo, modelName)
				self.master.OSImage.config(state="normal")
		else:
			self.master.displayText["text"] = 'Select request form canceled'
	def copyText(self):
		md5 = self.master.TF2.get()
		if md5:
			self.master.clipboard_clear()
			self.master.clipboard_append(md5)
			self.master.update()
			self.master.displayText["text"] = '\"{0}\" has been copy to clipboard'.format(md5)
			showinfo('Information', 'md5: {0} has been copy to clipboard'.format(md5))
		else:
			showerror('ERROR', 'Field of MD5 is empty')
	def openInfosite(self):
		try:
			FullVerInfo = self.master.TF3.get().replace(' ', '')
			if FullVerInfo:
				showinfo('Information', DownloadInfo)
				VerInfo = FullVerInfo.split(',')[0]
				version = VerInfo.split('.')[0]
				osbuild = VerInfo.split('B')[1]
				model = FullVerInfo.split(',')[1]
				Fullmodel = model.split('_')[0]
				model_dict = getJsonData(join(dirname(ImagePath), 'models.json'))
				Fullmodel = model_dict[Fullmodel]
				web('https://info.fortinet.com/files/{0}/v{1}.00/images/build{2}/{3}-v{1}-build{2}-FORTINET.out'.format(Fullmodel, version, osbuild, model))
			else:
				showerror('ERROR', 'Please select  TP request form,\nsuch as \"04-TP-REQUEST-REQUEST FORM-FAZ-XXXE.docx\"')
		except IOError as ioerr:
			pass
			self.master.displayText["text"] = str(ioerr)
			showerror('ERROR', str(ioerr))
	def buildProgress(self):
		if self.master.CheckVar1.get() == 1:
			global date
			date = InputBox('Customize Date', '\nPlease assign the TP customized date [YYYYMMDD]:\n\ne.g., 20170922\n')
			if date == None:
				date = datetime.now().strftime("%Y%m%d")
				showinfo('Information', 'User clicked cancel, load default date: ' + date)
			else:
				if not checkDateformat(date):
					showerror('ERROR', 'Date: {0} is invalid date format'.format(date))
					self.master.displayText["text"] = 'Date: {0} is invalid date format'.format(date)
					return(False)
		else:
			date = datetime.now().strftime("%Y%m%d")
		thread_2 = MultiProcess('progress', 'build', 101, 1, 0.2)
		thread_1 = MultiProcess('build', 'build', 0, 0, 0)
		thread_2.start()
		thread_1.start()
	def extractProgress(self):
		self.master.CB1.config(state="disabled")
		self.master.Run.config(state="disabled")
		global TestPkg1
		TestPkg1 = askopenfilename(parent=self.master, initialdir='/', title='Select Test_Package_*.zip', filetypes=[("ZIP File",'Test_Package_*.zip')]).replace('/', '\\')
		if TestPkg1:
			thread_2 = MultiProcess('progress', 'extract', 101, 1, 0.07)
			thread_1 = MultiProcess('extract', 'extract', 0, 0, 0)
			thread_2.start()
			thread_1.start()
if __name__ == '__main__':
	root = Tk()
	if getProcesses(['TPbuilder'], 0).count('TPbuilder') == 2:
		if CheckSetup():
			app = Windows(master=root)
			app.mainloop()
		else:
			root.withdraw()
			showerror('ERROR', 'TPbuilder is not installed')
	else:
		root.withdraw()
		showerror('ERROR', 'TPbuilder.exe is already executing')