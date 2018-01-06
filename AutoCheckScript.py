from re import search
from time import sleep, strftime
from win32com.client import Dispatch
from os.path import join, isdir, basename
from threading import Thread, active_count
from os import system, environ, mkdir, listdir
from win32pdh import EnumObjects, EnumObjectItems
from calendar import monthcalendar, IllegalMonthError
from logging import basicConfig, DEBUG, getLogger, StreamHandler, Formatter

Desktop = join('C:' + environ['HOMEPATH'], 'Desktop')
kb = Dispatch("WScript.Shell")
require_debug = input('Enable debug log mode? (default:N) [y/N]: ')
if require_debug in ['y', 'Y']:
	basicConfig(filename='AutoCheckScript_' + strftime('%Y%m%d_%H-%M-%S') + '.log', level=DEBUG)
	logger = getLogger(__name__)
	fhandler = StreamHandler()
	fhandler.setFormatter(Formatter())
	logger.addHandler(fhandler)
	status = 1
else:
	status = 0

class MultiProcess(Thread):
	def __init__(self, action, delay):
		Thread.__init__(self)
		self.action = action
		self.delay = delay
	def run(self):
		ProcessAction(self.action, self.delay)
def prt_message(text, status, mode):
	if status == 0:
		print(text)
	else:
		if mode == 'info':
			logger.info(text)
		elif mode == 'debug':
			logger.debug(text)
		elif mode == 'error':
			logger.error(text)
def getCurrentQ():
	Season = {'Q1': ['01', '02', '03'], 'Q2': ['04', '05', '06'], 'Q3': ['07', '08', '09'], 'Q4': ['10', '11', '12']}
	for i in range(1,5):
		if strftime('%m') in Season['Q'+str(i)]:
			return('Q' + str(i))
def getProgram(fileReg):
	for each_file in listdir(Desktop):
		if search(fileReg, each_file):
			return(join(Desktop, each_file))
def getMonthDay(y, m):
	tmp_list = []
	for i in range(6):
		try:
			for each_d in monthcalendar(int(y), int(m))[i]:
				if each_d != 0:
					tmp_list.append(each_d)
		except IndexError:
			pass
	return(tmp_list)
def getProcesses():
	EnumObjects(None, None, 0, 1)
	(items, instance) = EnumObjectItems(None, None, "Process", -1)
	return(instance)
def ProcessAction(action, delay):
	sleep(delay)
	if action == 'automation':
		system(Automation)
	elif action == 'keyControl':
		prt_message('Starting control automation...', status, 'info')
		for each_key in ['{DOWN}', '{TAB}', '{ENTER}', 'Path', '{TAB}', '{TAB}', '{TAB}', '{ENTER}', ' ', '+{END}', '{TAB}', '{ENTER}', '{TAB}', 'InputDate', '{TAB}', '{ENTER}']:
			sleep(2)
			if each_key == 'Path':
				kb.SendKeys(SavePath)
			elif each_key == 'InputDate':
				kb.SendKeys(date_range)
			else:
				kb.SendKeys(each_key)
		sleep(250)
		while(1):
			if basename(Automation).replace('.exe', '') in getProcesses():
				prt_message('Automation is exist, Enter to exit', status, 'info')
				kb.SendKeys('{ENTER}')
			else:
				"""
				prt_message('Automation is not exist, Start iSMART_V5.2.11.exe', status, 'info')
				system('Powershell Start-Process \"C:\\Program Files (x86)\\VIVOTEK Inc\\iSMART_V5.2.11\\iSMART_V5.2.11.exe\" -Verb RunAs')
				sleep(2)
				if 'iSMART_V5.2.11' in getProcesses():
				"""
				break
			sleep(5)
def isAlive(logic=None, threadNum=0):
	while(True):
		if logic == 'lt':
			if active_count() < threadNum:
				break
		elif logic == 'gt':
			if active_count() > threadNum:
				break
		sleep(0.5)

prt_message("""
======================================================================
\t     Welcome to auto check recording log script
======================================================================
\t\t    Follow below listed caution:
[1] Put the automation tool in desktop follow as below example.
    e.g., "Recording_log_check_Tool_for_vast_vx.x.x.exe"
[2] Open VAST Playback program as necessary.
[3] Do not interrupt while script has been executing.
[4] Press keyboard "Ctrl + C" to exit.
[5] Date range format must be:
    e.g., 2017/12/29
          2017/12/29-2018/01/01 or 2017/02/28-2017/03/01
======================================================================""", status, 'info')
try:
	while(1):
		date_range = input('Please input date range e.g., [2000/01/01-2018/12/31]:\n ==> ')
		d_lst1, d_lst2 = [], []
		if search('^20\d{2}/\d{2}/\d{2}\-20\d{2}/\d{2}/\d{2}$', date_range):
			date_range1, date_range2 = date_range.split('-')[0], date_range.split('-')[1]
			y1, y2 = date_range1.split('/')[0], date_range2.split('/')[0]
			m1, m2 = date_range1.split('/')[1], date_range2.split('/')[1]
			d1, d2 = date_range1.split('/')[2], date_range2.split('/')[2]
			if int(y1) > int(y2) or int(m1) > 12 or int(m2) > 12 or 0 in [int(m1), int(m2), int(d1), int(d2)]:
				prt_message('\nInvalid date format', status, 'error')
				continue
			elif (y1 == y2 and int(m1) > int(m2)) or (y1 == y2 and m1 == m2 and int(d1) > int(d2)) or int(d1) > 31 or int(d2) > 31:
				prt_message('\nInvalid date format', status, 'error')
				continue
			def DateSum1(d1):
				for d in getMonthDay(y1, m1):
					if d1[0] == '0':
						d1 = d1[1]
					if d >= int(d1):
						if d < 10:
							d = '0' + str(d)
						d_lst1.append(y1 + '-' + m1 + '-' + str(d))
			def DateSum2(d2):		
				for d in getMonthDay(y2, m2):
					if d2[0] == '0':
						d2 = d2[1]
					if d <= int(d2):
						if d < 10:
							d = '0' + str(d)
						d_lst2.append(y2 + '-' + m2 + '-' + str(d))
			def DateSum3(w, x, y, z):
				for i in range(x, y):
					if i < 10:
						fr_i = '0' + str(i)
					else:
						fr_i = str(i)
					for j in getMonthDay(z, i):
						if j < 10:
							j = '0' + str(j)
						w.append(z + '-' + fr_i + '-' + str(j))
			#case1: 2017/12/29-2018/01/04 or 2018/01/29-2018/02/04
			if (y1 < y2 and m1 == '12' and m2 == '01') or (y1 == y2 and int(m2) - int(m1) == 1):
				DateSum1(d1)
				DateSum2(d2)
			#case2: 2017/01/10-2017/05/04
			elif y1 == y2 and int(m2) - int(m1) > 1:
				DateSum1(d1)
				DateSum3(d_lst1, int(m1)+1, int(m2), y1)
				DateSum2(d2)
			#case3: 2017/10/10-2018/02/04 or 2017/12/05-2018/03/05 or 2017/10/05-2018/01/05
			elif (y1 < y2 and m1 != '12' and m2 != '01') or (y1 < y2 and m1 == '12' and m2 != '01') or (y1 < y2 and m1 != '12' and m2 == '01'):
				prt_message('this case', status, 'debug')
				DateSum1(d1)
				DateSum3(d_lst1, int(m1)+1, 13, y1)
				DateSum3(d_lst2, 1, int(m2), y2)
				DateSum2(d2)
			#case4: 2018/01/09-2018/01/20
			elif y1 == y2 and m1 == m2:
				for d in getMonthDay(y1, m1):
					if d1[0] == '0':
						d1 = d1[1]
					if d >= int(d1) and d <= int(d2):
						if d < 10:
							d = '0' + str(d)
						d_lst1.append(y1 + '-' + m1 + '-' + str(d))
			break
		elif search('^20\d{2}/\d{2}/\d{2}$', date_range):
			date_range = date_range.replace('/', '-')
			d_lst1.append(date_range)
			break
		else:
			prt_message('\nInvalid date format', status, 'error')

	date_list = d_lst1 + d_lst2
	prt_message(date_list, status, 'debug')
	for each_date in date_list:
		date_range = each_date
		prt_message('Check Date: ' + date_range, status, 'debug')
		thread_1 = MultiProcess('automation', 0)
		thread_2 = MultiProcess('keyControl', 5)
		SavePath = join(join(Desktop, strftime('%Y') + ' ' + getCurrentQ()), date_range.split('-')[1] + date_range.split('-')[2])
		prt_message(SavePath, status, 'debug')
		Automation = getProgram('^Recording_log_check_Tool_for_vast_\w+')
		prt_message('Execute Automation: ' + basename(Automation), status, 'debug')
		if not getProgram('^Recording_log_check_Tool_for_vast_\w+'):
			prt_message('\nRecording log check Tool is not found', status, 'error')
			raise Exception
		if 'VMSPlayback' not in getProcesses():
			prt_message('\nVAST Playback program is not executed', status, 'error')
			raise Exception
		prt_message('Log Save Path: ' + SavePath, status, 'error')

		if not isdir(SavePath):
			prt_message('Detect directory is not exists, create new one.\nDirectory: ' + SavePath, status, 'info')
			mkdir(SavePath)

		if basename(Automation).replace('.exe', '') in getProcesses():
			prt_message('Detect automation {} is executing in system, kill the process down.'.format(basename(Automation)), status, 'info')
			system('taskkill /f /im ' + basename(Automation))
		thread_1.start()
		thread_2.start()
		isAlive('lt', 3)
		if len(listdir(SavePath)) >= 64:
			prt_message('\n***** Date: {} check continues recording completed! *****\n'.format(date_range), status, 'info')
		else:
			prt_message('\n***** Date: {} check continues recording failured. *****\n'.format(date_range), status, 'error')
except Exception:
	print('', end='')
except KeyboardInterrupt:
	prt_message('\nUser press Ctrl+C to exit.', status, 'info')
sleep(2)
