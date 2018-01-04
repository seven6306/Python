from re import search
from threading import Thread
from os.path import join, isdir
from time import sleep, strftime
from win32com.client import Dispatch
from os import system, environ, mkdir, listdir
from win32pdh import EnumObjects, EnumObjectItems
from calendar import monthcalendar, IllegalMonthError

Desktop = join('C:' + environ['HOMEPATH'], 'Desktop')
kb = Dispatch("WScript.Shell")

class MultiProcess(Thread):
	def __init__(self, action, delay):
		Thread.__init__(self)
		self.action = action
		self.delay = delay
	def run(self):
		ProcessAction(self.action, self.delay)
def getCurrentQ():
	Season = {'Q1': ['01', '02', '03'], 'Q2': ['04', '05', '06'], 'Q3': ['07', '08', '09'], 'Q4': ['10', '11', '12']}
	for i in range(1,5):
		if strftime('%m') in Season['Q'+str(i)]:
			return('Q' + str(i))
def getProgram(fileReg):
	for each_file in listdir(Desktop):
		if search(fileReg, each_file):
			return(each_file)
def getMonthDay(y, m):
	tmp_list = []
	for i in range(5):
		for each_d in monthcalendar(int(y), int(m))[i]:
			if each_d != 0:
				tmp_list.append(each_d)
	return(tmp_list)
def getProcesses():
	EnumObjects(None, None, 0, 1)
	(items, instance) = EnumObjectItems(None, None, "Process", -1)
	return(instance)
def ProcessAction(action, delay):
	sleep(delay)
	if action == 'program':
		system(Program)
	elif action == 'keyControl':
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
			if Program.replace('.exe', '') in getProcesses():
				print('Program is exist, Enter to exit')
				kb.SendKeys('{ENTER}')
			"""
			else:
				print('Program is not exist, Start iSMART_V5.2.11.exe')
				system('\"C:\\Program Files (x86)\\VIVOTEK Inc\\iSMART_V5.2.11\\iSMART_V5.2.11.exe\"')
				sleep(2)
				if 'iSMART_V5.2.11' in getProcesses():
					break
			"""
			sleep(5)

print("""==================================================================
\t   Welcome to auto check recording log script
==================================================================
\t\t  Follow below listed caution:
[1] Put the program "Recording_log_check_Tool_for_vast_vx.x.x.exe"
    in desktop.
[2] Open VAST Playback program.
[3] Do not interrupt when script executing.
[4] Date range format must be 
    e.g., 2017/12/29
          2017/12/29-2018/01/01 or 2017/02/28-2017/03/01
==================================================================""")
try:
	while(1):
		date_range = input('Please input date range e.g., [2000/01/01-2017/12/31]: ')
		d_lst1, d_lst2 = [], []
		if search('^20\d{2}/\d{2}/\d{2}\-20\d{2}/\d{2}/\d{2}$', date_range):
			date_range1, date_range2 = date_range.split('-')[0], date_range.split('-')[1]
			y1, y2 = date_range1.split('/')[0], date_range2.split('/')[0]
			m1, m2 = date_range1.split('/')[1], date_range2.split('/')[1]
			d1, d2 = date_range1.split('/')[2], date_range2.split('/')[2]
			if int(y1) > int(y2) or int(m1) > 12 or int(m2) > 12 or 0 in [int(m1), int(m2), int(d1), int(d2)]:
				print('\nInvalid date format')
				continue
			elif y1 == y2 and int(m1) > int(m2):
				print('\nInvalid date format')
				continue
			def DatePart1(d1):
				for d in getMonthDay(y1, m1):
					if d1[0] == '0':
						d1 = d1[1]
					if d >= int(d1):
						d_lst1.append(y1 + '-' + m1 + '-' + str(d))
			def DatePart2(d2):		
				for d in getMonthDay(y2, m2):
					if d2[0] == '0':
						d2 = d2[1]
					if d <= int(d2):
						d_lst2.append(y2 + '-' + m2 + '-' + str(d))
			#case 2017/12/29-2018/01/04 or 2018/01/29-2018/02/04
			if y1 < y2 or (y1 == y2 and int(m2) - int(m1) == 1):
				DatePart1(d1)
				DatePart2(d2)
			#case 2017/01/10-2017/05/04
			elif y1 == y2 and int(m2) - int(m1) > 1:
				DatePart1(d1)
				for i in range(int(m1)+1, int(m2)):
					for j in getMonthDay(y1, i):
						d_lst1.append(y1 + '-' + str(i) + '-' + str(j))
				DatePart2(d2)
			#case 2017/10/10-2018/02/04
			# +> 2017/10/10-2017/12/31 : 2018/01/01-2018/02/04
			#elif y1 < y2 and int(m1) > int(m2):
			
			#case 2018/01/09-2018/01/20
			elif y1 == y2 and m1 == m2:
				for d in getMonthDay(y1, m1):
					if d1[0] == '0':
						d1 = d1[1]
					if d >= int(d1) and d <= int(d2):
						d_lst1.append(y1 + '-' + m1 + '-' + str(d))
			break
		elif search('^20\d{2}/\d{2}/\d{2}$', date_range):
			date_range = date_range.replace('/', '-')
			d_lst1.append(date_range)
			print('Check Date: ' + date_range)
			break
		else:
			print('\nInvalid date format')

	date_list = d_lst1 + d_lst2
	print(date_list)
	"""
	for each_date in date_list:
		date_range = each_date
		thread_1 = MultiProcess('program', 0)
		thread_2 = MultiProcess('keyControl', 5)
		SavePath = join(join(Desktop, strftime('%Y') + ' ' + getCurrentQ()), date_range.split('-')[1] + date_range.split('-')[2])
		Program = getProgram('^Recording_log_check_Tool_for_vast_\w+')
		if not getProgram('^Recording_log_check_Tool_for_vast_\w+'):
			print('\nRecording log check Tool is not found')
			raise Exception
		if 'VMSPlayback' not in getProcesses():
			print('\nVAST Playback program is not executed')
			raise Exception
		print('Log Save Path: ' + SavePath)

		if not isdir(SavePath):
			mkdir(SavePath)

		while(Program.replace('.exe', '') not in getProcesses()):
			thread_1.start()
			thread_2.start()
	"""
#except Exception:
	#print('', end='')
except KeyboardInterrupt:
	print('\nUser press Ctrl+C to exit.')