import os,re,json,winreg
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from subprocess import call
from getpass import getuser
from shutil import copytree
from platform import release
from time import sleep, ctime
from win32wnet import WNetAddConnection2
from webbrowser import open_new
from win32pdh import EnumObjects, EnumObjectItems
from win32serviceutil import RestartService, StartService, StopService, QueryServiceStatus
def process_Getdefault():
	return({	'UserName': 'ift\\allen.liu', 'Password': '1qaz@WSX', 'CREATE_NO_WINDOW': 0x08000000,
				'File': ['watch_log', 'dbManagement_log', 'AutoNas_log', 'AutoNas_cliLog', 'ndmp_log', 'agent_log', 'EonOne_log'], 
				'ATTR': ['rw_log', 'rw_log', 'rw_log', 'rw_log', 'ndmp_log', 'agent_log', 'EonOne'], 
				'STD': ['file_rw', 'file_rw', 'file_rw', 'file_rw', 'file_ndmp', 'file_agent', 'file_EonOne'],
				'Service': ['EonOne-Root-Agent', 'EonOne-NdmpServer', 'EonOne-Recover-Agent', 'RAID-Agent'],
				'Download': ['\\\\192.168.99.35\\RD\\HostSw\\EonOne', '\\\\192.168.99.35\\RD\\HostSw\\EonOne\\EonOne_2.4\\EonOne_2.4.a.01'],
				'Eon_path': 'C:/Program Files/Infortrend Inc/EonOne/', 'Bin_path': 'C:/Program Files/Infortrend Inc/EonOne/bin/', 
				'Setup_Path': 'None', 'SYS_json': 'C:/Program Files/Infortrend Inc/EonOne/bin/dat/record/system.json'})
""" Function of update config: default.json """
def process_Writejson(filename, data={}):
	try:
		with open(filename, 'w') as jwf:
			print(json.dumps(data, sort_keys=True), file=jwf)
	except IOError as jsioerr:
		messagebox.showerror('設定檔錯誤', str(jsioerr))
""" List all process on system """
def process_ListProcess():
	EnumObjects(None, None, 0, 1) # Refresh Processes
	(items, processes) = EnumObjectItems(None, None, 'Process', -1)
	return(processes)
""" Function of recursively remove files """
def process_RegRemove(dir, pattern=''):
	try:
		for each_file in os.listdir(dir):
			if re.search(pattern, each_file):
				filename = dir + '/' + each_file
				if os.path.isfile(filename):
					os.remove(filename)
				elif os.path.exists(filename):
					process_RegRemove(filename)
	except:
		pass
""" Windows registry key settings """
def process_SetRegistry(browser='', RegName=[], RegValue=[]):
	try:
		with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\' + RegName[0] + '\\UserChoice', 0, winreg.KEY_ALL_ACCESS) as key_v:
			value = winreg.QueryValueEx(key_v, 'Progid')[0]
			if value == 'ChromeHTML':
				old_browser = 'Chrome'
			elif value == 'FirefoxURL':
				old_browser = 'Firefox'
			elif value == 'IE.HTTP':
				old_browser = 'IExplore'
			elif value == 'OperaStable':
				old_browser = 'Opera'
			else:
				old_browser = value
		if messagebox.askquestion('變更預設瀏覽器', '預設瀏覽器為: \"' + old_browser + '\", 是否將預設瀏覽器變更為 \"' + browser + '\"?') == 'yes':
			for num in range(2):
				with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\' + RegName[int(num)] + '\\UserChoice', 0, winreg.KEY_ALL_ACCESS) as key:
					winreg.SetValueEx(key, 'Progid', 0, winreg.REG_SZ, RegValue[int(num)])
			messagebox.showinfo('變更預設瀏覽器', '預設瀏覽器已變更為: \"' + browser + '\"')
	except FileNotFoundError as regerr:
		messagebox.showerror('位置錯誤', str(regerr))
def process_service(action=None, serviceName={}):
	try:
		for service in serviceName:
			status = QueryServiceStatus(service)
			if action == 'start':
				if str(status).split(',')[1] == ' 4':
					messagebox.showerror('系統服務錯誤', '服務: \"' + service + '\" 已經被啟用.')
					return(False)
				StartService(service)
			elif action == 'stop':
				if str(status).split(',')[1] == ' 1':
					messagebox.showerror('系統服務錯誤', '服務: \"' + service + '\" 已經被停用.')
					return(False)
				StopService(service)
			elif action == 'unknown':
				if str(status).split(',')[1] == ' 4':
					if messagebox.askquestion('系統服務', '服務' + service + '啟用中, 需要停止嗎?') == 'yes':
						StopService(service)
						sleep(3)
						messagebox.showinfo('系統服務', '服務' + service + '停止完成.')
				elif str(status).split(',')[1] == ' 1':
					if messagebox.askquestion('系統服務', '服務' + service + '停止中, 需要啟用嗎?') == 'yes':
						StartService(service)
						sleep(3)
						messagebox.showinfo('系統服務', '服務' + service + '啟用完成.')
			else:
				RestartService(service)
				try:
					processed = QueryServiceStatus(service)
					if str(processed).split(',')[1] != ' 4':
						StartService(service)
				except Exception:
					pass
		return(True)
	except Exception as win32err:
		messagebox.showerror('系統服務錯誤', str(win32err))
		return(False)
def process_rfile(filename):
	if os.path.isfile(filename):
		try:
			with open(filename) as r_sysjson:
				rdata = json.loads((r_sysjson.read()))
				if rdata['intoOverview'] and rdata['Initial']:
					return('啟用')
				elif rdata == {}:
					return('停用')
				else:
					return('None')
		except IOError as err:
			messagebox.showerror('檔案錯誤', str(err))
	else:
		return('未安裝')
def process_result(result=None, action=None, object={}, string=''):
	if result:
		if action:
			object["text"] = '停用'
			messagebox.showinfo('Log 狀態', string + ' 已經被\"啟用\"')
		else:
			object["text"] = '啟用'
			messagebox.showinfo('Log 狀態', string + ' 已經被\"停用\"')
def process_action(filename=None, count=0):
	if os.path.isfile(filename):
		with open(filename) as rlog:
			for log_data in rlog:
				try:
					if re.search('^log4j.logger.*=OFF$', log_data) or re.search('^#log4j.logger.*=DEBUG, std, .*$', log_data):
						count = count + 1
					elif re.search('^#log4j.logger.*=OFF$', log_data) or re.search('^log4j.logger.*=DEBUG, std, .*$', log_data):
						count = count + 2
				except AttributeError as attrerr:
					pass
		if count == 2:
			return('啟用')
		elif count == 4:
			return('停用')
	else:
		return('未安裝')
def process_file(action=None, filename=None, log_attr=None, log_file=None, log_std=None):
	try:
		with open(filename) as rf:
			data_A = rf.read()
			if action:
				mark = ''
				remark = '#'
				if data_A.count(mark + 'log4j.logger.' + log_attr + '=OFF') == 0 or data_A.count(remark + 'log4j.logger.' + log_file + '=DEBUG, std, ' + log_std) == 0:
					messagebox.showerror('Log 錯誤', 'Log: ' + log_file + ' is already enabled.')
					return(False)
			else:
				mark = '#'
				remark = ''
				if data_A.count(mark + 'log4j.logger.' + log_attr + '=OFF') == 0 or data_A.count(remark + 'log4j.logger.' + log_file + '=DEBUG, std, ' + log_std) == 0:
					messagebox.showerror('Log 錯誤', 'Log: ' + log_file + ' is already disabled.')
					return(False)
			data_B = data_A.replace(mark + 'log4j.logger.' + log_attr + '=OFF', remark + 'log4j.logger.' + log_attr + '=OFF')
			data_C = data_B.replace(remark + 'log4j.logger.' + log_file + '=DEBUG, std, ' + log_std, mark + 'log4j.logger.' + log_file + '=DEBUG, std, ' + log_std)
		with open(filename, 'w') as wf:
			print(data_C, file=wf)	
		return(True)
	except IOError as ioerr:
		messagebox.showerror('檔案錯誤', str(ioerr))
		return(False)
class TopLV(Toplevel):
	def __init__(self, SetText=''):
		Toplevel.__init__(self)
		self.geometry('400x150+400+100')
		self.title('執行中請稍候')
		self.TextLabel = Label(self, text=SetText, fg="blue", font="Verdana 10")
		self.focus()
		self.grab_set()
		self.resizable(0, 0)
		def TopLV_Close():
			print(None)
		self.protocol('WM_DELETE_WINDOW', TopLV_Close)
		self.TextLabel.place(x=60, y=60)
class Windows(Frame):
	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)
		self.master.title('EonOne測試輔助工具')
		self.master.geometry('300x300')
		self.master.resizable(0, 0)
		if os.path.isfile('./image/default.ico'):
			self.master.iconbitmap(default='./image/default.ico')
		self.createMenu()
		self.createWidgets()
		self.master.bind('<Button-3>', self.popup_menu)
	def createMenu(self):
		self.master.PopM = Menu(self.master.master, tearoff=0)
		self.master.PopM.add_command(label="開啟 EonOne", command=self.EonOne_open)
		self.master.PopM.add_command(label="下載 EonOne", command=self.EonOne_download)
		self.master.PopM.add_command(label="安裝 EonOne", command=self.EonOne_install)
		self.master.PopM.add_command(label="匯出設定檔", command=self.export_config)
		self.master.PopM.add_command(label="儲存設定檔", command=self.save_config)
		self.master.PopM.add_command(label="離開", command=self.exit)
		self.master.Mbar = Menu(self.master.master)
		self.master.FileM = Menu(self.master.Mbar, tearoff=0)
		self.master.FileM.add_command(label="選擇 EonOne 路徑", command=self.select_path)
		self.master.FileM.add_command(label="開啟 EonOne 路徑", command=self.open_path)
		self.master.FileM.add_separator()
		self.master.FileM.add_command(label="下載 EonOne", command=self.EonOne_download)
		self.master.FileM.add_command(label="安裝 EonOne", command=self.EonOne_install)
		self.master.FileM.add_command(label="移除 EonOne", command=self.EonOne_remove)
		self.master.FileM.add_separator()
		self.master.FileM.add_command(label="離開", command=self.exit)
		self.master.Mbar.add_cascade(label="檔案", menu=self.master.FileM)
		self.master.WebM = Menu(self.master.Mbar, tearoff=0)
		self.master.WebM.add_command(label="開啟 EonOne", command=self.EonOne_open)
		self.master.WebM.add_command(label="登入 GS-NAS", command=self.GS_NAS_open)
		self.master.WebM.add_command(label="登入 RedMine", command=self.RedMine_open)
		self.master.WebM.add_separator()
		self.master.WebM.add_command(label="Workflow 首頁", command=self.Workflow_open)
		self.master.WebM.add_separator()
		self.master.WebM.add_command(label="刪除瀏覽器 Cookie", command=self.remove_cookie)
		self.master.Mbar.add_cascade(label="網頁", menu=self.master.WebM)
		self.master.HelpM = Menu(self.master.Mbar, tearoff=0)
		self.master.HelpM.add_command(label="幫助", command=self.help)
		self.master.HelpM.add_command(label="關於", command=self.about)
		self.master.Mbar.add_cascade(label="幫助", menu=self.master.HelpM)
		self.master.config(menu=self.master.Mbar)
	def popup_menu(self, event):
		self.master.PopM.post(event.x_root, event.y_root)
	""" ====================================== Right-Clicked menu events ====================================== """
	def export_config(self):
		save_path = filedialog.askdirectory(parent=root, initialdir="/", title='選擇設定檔存放位置')
		if save_path != '':
			if os.path.exists(save_path):
				config = save_path + '/' + 'default.json'
				process_Writejson(config, LogDict)
				if os.path.isfile(config):
					messagebox.showinfo('匯出設定檔', '設定檔以匯出至: ' + config)
			else:
				messagebox.showerror('匯出設定檔', '無效的設定檔存放路徑.')
	def save_config(self):
		process_Writejson('default.json', LogDict)
	""" ================================================= EOF ================================================= """
	def select_path(self):
		path = filedialog.askdirectory(parent=root, initialdir="/", title='選擇 EonOne 資料夾')
		if path != '':
			if os.path.exists(path):
				LogDict['Eon_path'] = path + '/'
				LogDict['Bin_path'] = LogDict['Eon_path'] + 'bin/'
				LogDict['SYS_json'] = LogDict['Bin_path'] + 'dat/record/system.json'
				process_Writejson('default.json', LogDict)
				messagebox.showinfo('EonOne 路徑變更', 'EonOne 路徑變更為: \n\"' + LogDict['Eon_path'] + '\"')
			else:
				messagebox.showerror('EonOne 路徑變更', '無效的資料夾路徑.')
	def open_path(self):
		directory = LogDict['Eon_path']
		if os.path.exists(directory):
			os.startfile(directory)
		else:
			messagebox.showerror('安裝錯誤', '請檢查 EonOne 是否正確安裝.')
	def EonOne_download(self):
		DL_w = Toplevel()
		DL_w.geometry('510x135+400+100')
		DL_w.title('EonOne 下載')
		DL_w.focus()
		DL_w.grab_set()
		DL_w.resizable(0, 0)
		LB = Label(DL_w, text="1. 預設下載路徑 : ", fg="purple").place(x=10, y=10)
		TF1 = ttk.Entry(DL_w, width=40)
		TF1.insert(0, LogDict['Download'][0])
		TF1.config(state='readonly')
		TF1.place(x=115, y=10)
		LB = Label(DL_w, text="2. EonOne 版本 : ", fg="purple").place(x=10, y=40)
		TF2 = ttk.Entry(DL_w, width=40)
		TF2.insert(0, LogDict['Download'][1])
		TF2.config(state='readonly')
		TF2.place(x=115, y=40)
		LB = Label(DL_w, text="3. IFT 個人帳號 : ", fg="purple").place(x=10, y=70)
		TF3 = ttk.Entry(DL_w, width=15)
		TF3.insert(0, LogDict['UserName'])
		TF3.config(state='readonly')
		TF3.place(x=115, y=70)
		LB = Label(DL_w, text="4. IFT 個人密碼 : ", fg="purple").place(x=10, y=100)
		TF4 = ttk.Entry(DL_w, width=15, show='*')
		TF4.insert(0, LogDict['Password'])
		TF4.config(state='readonly')
		TF4.place(x=115, y=100)
		def check_credentials():
			try:
				if call(['ping', '-n', '1', '-w', '1', '192.168.99.35'], creationflags=LogDict['CREATE_NO_WINDOW']) != 0:
					messagebox.showerror('連線錯誤', '無法連接到檔案伺服器 nasshare (192.168.99.35)')
					return(False)
				if TF3.get() == '' or TF4.get() == '':
					messagebox.showerror('帳號密碼錯誤', 'Infortrend 帳號密碼不得為空白.')
					return(False)
				WNetAddConnection2(0, None, '\\\\192.168.99.35', None, TF3.get(), TF4.get())
				if not os.path.exists(TF1.get()):
					messagebox.showerror('連線錯誤', '無法連接到檔案伺服器 192.168.99.35 可能是帳號密碼有錯.')
					return(False)
				return(True)
			except Exception as win32err:
				messagebox.showerror('連線錯誤', str(win32err))
				return(False)
		def select_EonOne_Path():
			if check_credentials():
				default = filedialog.askdirectory(parent=DL_w, initialdir=TF1.get(), title='選擇 EonOne 預設路徑')
				if default != '' and TF1.get() != '':
					default = default.replace('/', '\\')
					LogDict['Download'][0] = default
					TF1.config(state='NORMAL')
					TF1.delete(0, END)
					TF1.insert(0, default)
					TF1.config(state='readonly')
		def select_EonOne_File():
			if check_credentials():
				installer = filedialog.askdirectory(parent=DL_w, initialdir=TF1.get(), title='選擇欲下載的 EonOne 版本')
				if installer != '' and TF2.get() != '':
					installer = installer.replace('/', '\\')
					LogDict['Download'][1] = installer
					TF2.config(state='NORMAL')
					TF2.delete(0, END)
					TF2.insert(0, installer)
					TF2.config(state='readonly')
		def download_file():
			if check_credentials():
				try:
					DL_w.config(cursor="wait")
					self.window_update('檔案: ' + TF2.get().split('\\')[-1] + '下載中請稍候...')
					SavePath = filedialog.askdirectory(parent=DL_w, initialdir="/", title='選擇存放路徑')
					if SavePath != '':
						LogDict['Setup_Path'] = SavePath + '/' + TF2.get().split('\\')[-1]
						copytree(TF2.get(), LogDict['Setup_Path'])
						if os.path.exists(LogDict['Setup_Path']):
							messagebox.showinfo('EonOne 下載', '檔案: ' + TF2.get().split('\\')[-1] + '下載完成!')
							self.EonOne_install()
						else:
							messagebox.showerror('EonOne 下載', '檔案: ' + TF2.get().split('\\')[-1] + '下載失敗.')
					else:
						messagebox.showerror('EonOne 下載', '檔案存放路徑不能為空白.')
					DL_w.focus()
					DL_w.grab_set()
					DL_w.config(cursor="")
					self.call_window.config(cursor="")
					self.master.config(cursor="")
					self.call_window.destroy()
				except IOError as ioerr:
					messagebox.showerror('ERROR', str(ioerr))
		def change_user():
			if BT3['text'] == '變更帳密':
				TF3.config(state='NORMAL')
				TF4.config(state='NORMAL')
				BT3['text'] = '確定變更'
			else:
				LogDict['UserName'] = TF3.get()
				LogDict['Password'] = TF4.get()
				TF3.config(state='readonly')
				TF4.config(state='readonly')
				BT3['text'] = '變更帳密'
		BT1 = ttk.Button(DL_w, text="自訂路徑", command=select_EonOne_Path)
		BT1.place(x=410, y=10)
		BT2 = ttk.Button(DL_w, text="選擇檔案", command=select_EonOne_File)
		BT2.place(x=410, y=40)
		BT3 = ttk.Button(DL_w, text="變更帳密", command=change_user)
		BT3.place(x=410, y=70)
		BT4 = ttk.Button(DL_w, text="下載檔案", command=download_file)
		BT4.place(x=410, y=100)
		def DL_w_Close():
			process_Writejson('default.json', LogDict)
			DL_w.destroy()
		DL_w.protocol('WM_DELETE_WINDOW', DL_w_Close)
	def EonOne_install(self):
		if os.path.exists(LogDict['Setup_Path']):
			if messagebox.askquestion('EonOne 安裝', '是否需要安裝 ' + LogDict['Setup_Path'].split('/')[-1] + ' ?') == 'yes':
				pwd = os.getcwd()
				if os.path.isfile(LogDict['Setup_Path'] + '/setup.exe'):
					os.chdir(LogDict['Setup_Path'])
					call('setup.exe')
					os.chdir(pwd)
		else:
			messagebox.showerror('安裝錯誤', '未指定 EonOne 安裝程式路徑, 或該安裝檔已不存在.')
	def EonOne_remove(self):
		path = LogDict['Eon_path']
		uninstall = path + 'uninstall.bat'
		if os.path.isfile(uninstall):
			call(uninstall, creationflags=LogDict['CREATE_NO_WINDOW'])
		else:
			messagebox.showerror('安裝錯誤', '請檢查 EonOne 是否正確安裝.')
	def exit(self):
		self.master.quit()
	def EonOne_open(self):
		open_new(r"https://127.0.0.1:8817/")
	def GS_NAS_open(self):
		open_new(r"http://swd.infortrend/linux_login_util.py#")
	def RedMine_open(self):
		open_new(r"http://pms.infortrend/projects/")
	def Workflow_open(self):
		open_new(r"http://login.infortrend.com/")
	def remove_cookie(self):
		""" ==================================== Clean browser cache and cookie ====================================  """
		if messagebox.askquestion('刪除瀏覽器 Cookie', '請確認瀏覽器都已關閉, 是否刪除網頁瀏覽器 Cookie?') == 'yes':
			current_user = getuser()
			process_RegRemove('C:/Users/' + current_user + '/AppData/Roaming/Microsoft/Windows/Cookies/', '.txt$')
			process_RegRemove('C:/Users/' + current_user + '/AppData/Roaming/Microsoft/Windows/Cookies/Low/', '.txt$')
			chrome_path = 'C:/Users/' + current_user + '/AppData/Local/Google/Chrome/User Data/Default/'
			firefox_path = 'C:/Users/' + current_user + '/AppData/Roaming/Mozilla/Firefox/Profiles/'
			try:
				if os.path.exists(chrome_path):
					if os.path.isfile(chrome_path + 'Cookies'):
						os.remove(chrome_path + 'Cookies')
					for each_cache in ['Cache', 'Media Cache']:
						process_RegRemove(chrome_path + each_cache)
				if os.path.exists(firefox_path):
					firefox_default = os.listdir(firefox_path)[0]
					if os.path.isfile(firefox_path + firefox_default + '/cookies.sqlite'):
						os.remove(firefox_path + firefox_default + '/cookies.sqlite')
					for each_cache in ['Cache', 'cache2', 'jumpListCache', 'OfflineCache', 'safebrowsing', 'startupCache', 'thumbnails']:
						process_RegRemove('C:/Users/' + current_user + '/AppData/Local/Mozilla/Firefox/Profiles/'+ firefox_default + '/' + each_cache)
				messagebox.showinfo('刪除瀏覽器 Cookie', '瀏覽器 Cookie 刪除完成!')
			except PermissionError as perr:
				messagebox.showerror('刪除錯誤', '瀏覽器可能正被其他程式使用中, 請關閉瀏覽器後再重試\n(仍有少數未被使用的暫存已經刪除)')
			except Exception as ex:
				messagebox.showerror('錯誤', str(ex))
	def help(self):
		help_w = Toplevel()
		help_w.geometry('600x640+350+30')
		help_w.title('使用說明書')
		help_w.focus()
		help_w.grab_set()
		help_w.resizable(0, 0)
		TB = Label(help_w, font="Verdana 10 bold", text="1. 使用建議:").place(x=10, y=10)
		TB = Label(help_w, fg="blue", font="Verdana 8", text="   a. 第一項單獨開啟/關閉 Debug Log,").place(x=10, y=40)
		TB = Label(help_w, fg="blue", font="Verdana 8", text="      不要和 開啟/關閉 所有 Log 一起使用.").place(x=10, y=60)
		TB = Label(help_w, fg="#5B4B00", font="Verdana 8", text="   b. 在每一次啟用或關閉 Log 的動作後,").place(x=10, y=80)
		TB = Label(help_w, fg="#5B4B00", font="Verdana 8", text="      都會即時更新按鈕狀態.").place(x=10, y=100)
		TB = Label(help_w, fg="#66009D", font="Verdana 8", text="   c. 若 Log 按鈕狀態為啟用, 表示 Log 已被關閉,").place(x=10, y=120)
		TB = Label(help_w, fg="#66009D", font="Verdana 8", text="      只能透過啟用來操作它, 以免發生邏輯問題.").place(x=10, y=140)
		TB = Label(help_w, font="Verdana 10 bold", text="2. 使用條件:").place(x=10, y=170)
		TB = Label(help_w, fg="#007979", font="Verdana 8", text="   必須在擁有安裝 EonOne 的環境下才能使用輔助工具,").place(x=10, y=200)
		TB = Label(help_w, fg="#007979", font="Verdana 8", text="   否則按鈕會顯示未安裝的提示, 並且所有功能會禁用.").place(x=10, y=220)
		TB = Label(help_w, font="Verdana 10 bold", text="3. 選單功能:").place(x=10, y=250)
		TB = Label(help_w, fg="#0066CC", font="Verdana 8", text="   a. 若您的 EonOne 不是安裝在預設路徑下,").place(x=10, y=280)
		TB = Label(help_w, fg="#0066CC", font="Verdana 8", text="      必須選擇自訂安裝路徑來提供程式使用需求.").place(x=10, y=300)
		TB = Label(help_w, fg="#9F0050", font="Verdana 8", text="   b. 開啟 EonOne 預設安裝路徑.").place(x=10, y=320)
		TB = Label(help_w, fg="#0066CC", font="Verdana 8", text="   c. 透過 nasshare 掛載的共享資料夾, 提供各").place(x=10, y=340)
		TB = Label(help_w, fg="#0066CC", font="Verdana 8", text="      種版本 EonOne, 令使用者更方便去下載").place(x=10, y=360)
		TB = Label(help_w, fg="#9F0050", font="Verdana 8", text="   d. 可直接呼叫 EonOne 解除安裝程式").place(x=10, y=380)
		TB = Label(help_w, font="Verdana 10 bold", text="4. 新增功能:").place(x=10, y=410)
		TB = Label(help_w, fg="#663300", font="Verdana 8", text="   a. EonOne 四種服務個別為:").place(x=10, y=440)
		TB = Label(help_w, font="Verdana 8", text="      1. EonOne-Root-Agent  2. EonOne-NdmpServer").place(x=10, y=460)
		TB = Label(help_w, font="Verdana 8", text="      3. EonOne-Recover-Agent  4. RAID-Agent").place(x=10, y=480)
		TB = Label(help_w, fg="#663300", font="Verdana 8", text="      可全部或個別進行 啟用/停用/重啟 的動作.").place(x=10, y=500)
		TB = Label(help_w, fg="#660066", font="Verdana 8", text="   b. 提供可將三種瀏覽器設成預設瀏覽器.").place(x=10, y=530)
		TB = Label(help_w, font="Verdana 8", text="      (前提系統上必須擁有該瀏覽器方能生效)").place(x=10, y=550)
		TB = Label(help_w, fg="#003366", font="Verdana 8", text="   c. 在 Windows Server 系列等系統, 設定完後開啟網頁時,").place(x=10, y=580) 
		TB = Label(help_w, fg="#003366", font="Verdana 8", text="      系統會自動要求再一次選擇並確認預設瀏覽器.").place(x=10, y=600)
		TB = Label(help_w, font="Verdana 10 bold", text="5. 網頁捷徑:").place(x=320, y=10)
		TB = Label(help_w, fg="purple", font="Verdana 8", text="   a. 網頁選單列提供以下四種網頁捷徑:").place(x=320, y=40)
		TB = Label(help_w, font="Verdana 8", text="      1. EonOne 登入  2. GS-NAS 解密網站").place(x=320, y=60)
		TB = Label(help_w, font="Verdana 8", text="      3. RedMine BUG系統  4. Workflow 平台").place(x=320, y=80)
		TB = Label(help_w, fg="#cc9900", font="Verdana 8", text="   b. 可以刪除 IE, Chrome, Firefox Cookie 暫存.").place(x=320, y=100)
		TB = Label(help_w, font="Verdana 8", text="      (只會刪除系統上有安裝的瀏覽器)").place(x=320, y=120)
		TB = Label(help_w, font="Verdana 10 bold", text="6. EonOne 下載:").place(x=320, y=150)
		TB = Label(help_w, fg="#990033", font="Verdana 8", text="   a. 透過 Windows Share 協定, 將存有各版本").place(x=320, y=180)
		TB = Label(help_w, fg="#990033", font="Verdana 8", text="      EonOne 之 nasshare 檔案伺服器, 經由虛").place(x=320, y=200)
		TB = Label(help_w, fg="#990033", font="Verdana 8", text="      擬掛載在系統上, 令使用者可用選擇檔案").place(x=320, y=220)
		TB = Label(help_w, fg="#990033", font="Verdana 8", text="      式來下載所需的 EonOne 主程式.").place(x=320, y=240)
		TB = Label(help_w, fg="#000066", font="Verdana 8", text="   b. 可自訂預設路徑即選擇檔案時會先從指定").place(x=320, y=260)
		TB = Label(help_w, fg="#000066", font="Verdana 8", text="      目錄開始列出.").place(x=320, y=280)
		TB = Label(help_w, fg="#003300", font="Verdana 8", text="   c. 選擇檔案即選擇使用者所需的 EonOne 版").place(x=320, y=300)
		TB = Label(help_w, fg="#003300", font="Verdana 8", text="      本 (檔案為目錄).").place(x=320, y=320)
		TB = Label(help_w, fg="#000066", font="Verdana 8", text="   d. 變更帳密: 登入 nasshare 時必須擁有一").place(x=320, y=340)
		TB = Label(help_w, fg="#000066", font="Verdana 8", text="      組可登入的帳戶, 預設使用設計者本身的").place(x=320, y=360)
		TB = Label(help_w, fg="#000066", font="Verdana 8", text="      帳戶, 哪天帳戶無法使用時再自行修改.").place(x=320, y=380)
		TB = Label(help_w, fg="#003300", font="Verdana 8", text="   e. 下載檔案時會要求使用者選擇檔案存放的目").place(x=320, y=400)
		TB = Label(help_w, fg="#003300", font="Verdana 8", text="      錄, 目錄不得為空.").place(x=320, y=420)
		TB = Label(help_w, font="Verdana 10 bold", text="7. EonOne 安裝:").place(x=320, y=450)
		TB = Label(help_w, fg="#333300", font="Verdana 8", text="      可透過選單, 右鍵選單, 來進行此功能, 前提").place(x=320, y=480)
		TB = Label(help_w, fg="#333300", font="Verdana 8", text="      必須是已經使用下載 EonOne 功能後的檔案,").place(x=320, y=500)
		TB = Label(help_w, fg="#333300", font="Verdana 8", text="      才會將安裝程式路徑帶入安裝功能中, 否則使.").place(x=320, y=520)
		TB = Label(help_w, fg="#333300", font="Verdana 8", text="      用時只會提示錯誤訊息: 找不到安裝檔路徑!").place(x=320, y=540)
	def about(self):
		about_w = Toplevel()
		about_w.geometry('300x380+350+150')
		about_w.title('關於我們')
		about_w.focus()
		about_w.grab_set()
		about_w.resizable(0, 0)
		if os.path.isfile('./image/Infortrend.png'):
			img = PhotoImage(file='./image/Infortrend.png')
			TB = Label(about_w, image=img)
			TB.photo = img
		else:
			TB = Label(about_w)
		TB.place(x=-2, y=-38)
		TB = Label(about_w, text="Version:   v1.0.0").place(x=10, y=70)
		TB = Label(about_w, text="Author:    Allen.Liu").place(x=10, y=100)
		TB = Label(about_w, text="Website:").place(x=10, y=130)
		def hyperlinks(event):
			open_new(r"http://www.infortrend.com")
		TB = Label(about_w, text="http://www.infortrend.com", fg="blue", cursor="hand2")
		TB.bind("<Button-1>", hyperlinks)
		TB.place(x=70, y=130)
		TB = Label(about_w, text="Description:").place(x=10, y=160)
		T = Text(about_w, bg="#E0E0E0")
		T.insert(END, "This application designed base on\nEonOne, Support tester to set environment effectively on testing.\n\nYou would easy to enable or disable debug log, and take the annoying\nservice manager off.\n\nIf this plugin has any bug, please\nfeedback to us, finally hope you\nhave wonderful day!")
		if release() == '7':
			T.config(state=DISABLED, width=36, height=11)
			T.place(x=21, y=190)
		else:
			T.config(state=DISABLED, width=34, height=9)
			T.place(x=13, y=190)
		def close_about():
			about_w.destroy()
		BT = ttk.Button(about_w, text="關閉", command=close_about).place(x=110, y=347)
	def createWidgets(self):
		self.master.LB = Label(self.master, text="1. 啟用/停用 Debug Log : ", fg="blue")
		self.master.LB.place(x=10, y=15)
		CBox_value = StringVar()
		self.master.CBox = ttk.Combobox(self.master, width=14, textvariable=CBox_value, state='readonly')
		self.master.CBox['values'] = ('1. watch_log', '2. dbManagement_log', '3. AutoNas_log', '4. AutoNas_cliLog', '5. ndmp_log', '6. agent_log', '7. EonOne_log')
		self.master.CBox.current(0)
		self.master.CBox.place(x=165, y=15)
		self.master.CBox.bind('<<ComboboxSelected>>', self.each_debug_log)
		self.master.LB = Label(self.master, text="2. 啟用/停用 所有 Log : ", fg="blue")
		self.master.LB.place(x=10, y=55)
		self.master.BT1 = ttk.Button(self.master)
		for num in range(7):
			self.master.BT1["text"] = process_action(LogDict['Bin_path'] + LogDict['File'][int(num)] + '.properties')
		self.master.BT1["command"] = self.all_debug_log
		self.master.BT1.place(x=180, y=55)
		self.master.LB = Label(self.master, text="3. 啟用/停用 服務管理員 : ", fg="blue")
		self.master.LB.place(x=10, y=95)
		self.master.BT2 = ttk.Button(self.master)
		self.master.BT2["text"] = process_rfile(LogDict['SYS_json'])
		self.master.BT2["command"] = self.service_manager
		self.master.BT2.place(x=180, y=95)
		self.master.LB = Label(self.master, text="4. 啟動/停止 EonOne 服務 : ", fg="blue")
		self.master.LB.place(x=10, y=135)
		CBox_value2 = StringVar()
		self.master.CBox2 = ttk.Combobox(self.master, width=9, textvariable=CBox_value2, state='readonly')
		self.master.CBox2['values'] = ('1. 重啟', '2. 啟動', '3. 停止', '4. ' + LogDict['Service'][0], '5. ' + LogDict['Service'][1], '6. ' + LogDict['Service'][2], '7. ' + LogDict['Service'][3])
		self.master.CBox2.current(0)
		self.master.CBox2.place(x=180, y=135)
		self.master.CBox2.bind('<<ComboboxSelected>>', self.service_engine)
		self.master.LB = Label(self.master, text="5. 變更預設瀏覽器 : ", fg="blue")
		self.master.LB.place(x=10, y=175)
		CBox_value3 = StringVar()
		self.master.CBox3 = ttk.Combobox(self.master, width=9, textvariable=CBox_value3, state='readonly')
		self.master.CBox3['values'] = ('1. Chrome', '2. Firefox', '3. IExplore', '4. Opera')
		self.master.CBox3.current(0)
		self.master.CBox3.place(x=180, y=175)
		self.master.CBox3.bind('<<ComboboxSelected>>', self.change_browser)
		if os.path.isfile('./image/infortrend-banner.png'):
			banner_img = PhotoImage(file='./image/infortrend-banner.png')
			self.master.IFTbanner = Label(self.master, image=banner_img)
			self.master.IFTbanner.photo = banner_img
		else:
			self.master.IFTbanner = Label(self.master)
		self.master.IFTbanner.place(x=-101, y=210)
	def each_debug_log(self, event):
		each_num = self.master.CBox.get().split('.')[0]
		each_num = int(each_num) - 1
		if process_action(LogDict['Bin_path'] + LogDict['File'][each_num] + '.properties') == '啟用':
			if messagebox.askquestion('EonOne Debug Log', 'Debug Log: ' + LogDict['File'][each_num] + ' 已經被\"停用, 需要\"啟用\"嗎?') == 'no':
				return(False)
			action = True
		elif process_action(LogDict['Bin_path'] + LogDict['File'][each_num] + '.properties') == '停用':
			if messagebox.askquestion('EonOne Debug Log', 'Debug Log: ' + LogDict['File'][each_num] + ' 已經被\"啟用\", 需要\"停用\"嗎?') == 'no':
				return(False)
			action = False
		else:
			messagebox.showerror('安裝錯誤', '請檢查 EonOne 是否正確安裝.')
			return(False)
		result = process_file(action, LogDict['Bin_path'] + LogDict['File'][each_num] + '.properties', LogDict['ATTR'][each_num], LogDict['File'][each_num], LogDict['STD'][each_num])
		process_result(result, action, {},'Log ' + LogDict['File'][each_num])
	def all_debug_log(self):
		if self.master.BT1["text"] == '啟用':
			action = True
		elif self.master.BT1["text"] == '停用':
			action = False
		else:
			messagebox.showerror('安裝錯誤', '請檢查 EonOne 是否正確安裝.')
			return(False)
		for num in range(7):
			result = process_file(action, LogDict['Bin_path'] + LogDict['File'][int(num)] + '.properties', LogDict['ATTR'][int(num)], LogDict['File'][int(num)], LogDict['STD'][int(num)])
		process_result(result, action, self.master.BT1, 'EonOne Log')
	def service_manager(self):
		if self.master.BT2["text"] == '啟用':
			data = {}
		elif self.master.BT2["text"] == '停用':
			data = {"Initial" : "true", "intoOverview" : "true" }
		else:
			messagebox.showerror('安裝錯誤', '請檢查 EonOne 是否正確安裝.')
			return(False)
		try:
			with open(LogDict['SYS_json'], 'w') as w_sysjson:
				print(json.dumps(data, sort_keys=True), file=w_sysjson)
				messagebox.showinfo('服務管理員', '服務管理員已經被' + self.master.BT2["text"])
				if self.master.BT2["text"] == '啟用':
					self.master.BT2["text"] = '停用'
				else:
					self.master.BT2["text"] = '啟用'
		except IOError as jerr:
			messagebox.showerror('檔案錯誤', str(jerr))
	def window_update(self, selected=''):
		self.call_window = TopLV(selected)
		self.call_window.config(cursor="wait")
		self.master.config(cursor="wait")
		self.call_window.update()
		self.master.update()
	def service_engine(self, event):
		service_num = self.master.CBox2.get().split('.')[0]
		service_num = int(service_num) - 1
		service_select = self.master.CBox2.get().split('.')[1].split(' ')[1]
		if service_num < 3:
			self.window_update('EonOne 服務' + service_select + '中請稍候...')
			if messagebox.askquestion('系統服務', '確定需要\"' + service_select + '\"服務嗎') == 'yes':
				if service_num == 0:
					if process_service('restart', LogDict['Service']):
						sleep(15)
						print('End: ' + ctime())
						messagebox.showinfo('系統服務', 'EonOne 服務已被' + service_select)
				elif service_num == 1:
					if process_service('start', LogDict['Service']):
						sleep(15)
						print('End: ' + ctime())
						messagebox.showinfo('系統服務', 'EonOne 服務已被' + service_select)
				elif service_num == 2:
					if process_service('stop', LogDict['Service']):
						sleep(15)
						messagebox.showinfo('系統服務', 'EonOne 服務已被' + service_select)
		else:
			self.window_update('服務: ' + service_select + ' 處理中請稍候...')
			if service_num == 3:
				process_service('unknown', [LogDict['Service'][0]])
			elif service_num == 4:
				process_service('unknown', [LogDict['Service'][1]])
			elif service_num == 5:
				process_service('unknown', [LogDict['Service'][2]])
			elif service_num == 6:
				process_service('unknown', [LogDict['Service'][3]])
		self.call_window.config(cursor="")
		self.master.config(cursor="")
		self.call_window.destroy()
	def change_browser(self, event):
		browser_num = self.master.CBox3.get().split('.')[0]
		browser_num = int(browser_num) - 1
		if browser_num == 0:
			process_SetRegistry('Chrome', ['http', 'https'], ['ChromeHTML', 'ChromeHTML'])
		elif browser_num == 1:
			process_SetRegistry('Firefox', ['http', 'https'], ['FirefoxURL', 'FirefoxURL'])
		elif browser_num == 2:
			process_SetRegistry('IExplore', ['http', 'https'], ['IE.HTTP', 'IE.HTTPS'])
		elif browser_num == 3:
			process_SetRegistry('Opera', ['http', 'https'], ['OperaStable', 'OperaStable'])
if __name__ == '__main__':
	root = Tk()
	""" Check if no config file, then given default dict """
	if os.path.isfile('./default.json'):
		with open('default.json') as jrf:
			LogDict = json.loads(jrf.read())
	else:
		LogDict = process_Getdefault()
	""" Check if program has been execute. """
	if process_ListProcess().count('EonPlugin') > 2:
		root.withdraw()
		messagebox.showerror('程序錯誤', '系統上已有 EonPlugin.exe 正在執行中.')
		root.quit()
	else:
		app = Windows(master=root)
		app.mainloop()