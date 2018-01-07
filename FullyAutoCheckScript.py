from re import search
from time import sleep, strftime
from calendar import monthcalendar
from win32com.client import Dispatch
from threading import Thread, active_count
from win32pdh import EnumObjects, EnumObjectItems
from os.path import join, isdir, isfile, basename
from os import system, environ, mkdir, listdir, remove
from logging import basicConfig, DEBUG, getLogger, StreamHandler, Formatter
"""
NOTE:
line94  : iSMART tool command work confirm
line100 : erase count correct keywords
line136 : Schduled clear log file function
line167 : checkFail() fail item keywords
"""
Desktop = join('C:' + environ['HOMEPATH'], 'Desktop')
kb = Dispatch("WScript.Shell")
basicConfig(filename='FullyAutoCheckScript.log', level=DEBUG)
logger = getLogger(__name__)
fhandler = StreamHandler()
fhandler.setFormatter(Formatter())
logger.addHandler(fhandler)

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
def checkFail(path):
	FAIL_LIST = []
	for each_file in listdir(path):
		if 'FAIL' in each_file:
			FAIL_LIST.append(each_file)
	logger.debug('Check Fail Count: {} fail items found.'.format(str(len(FAIL_LIST))))
	return(len(FAIL_LIST))
def getProgram(fileReg, dir):
	for each_file in listdir(dir):
		if search(fileReg, each_file):
			return(join(dir, each_file))
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
def getYesterday(y, m, d):
	if int(d) == 1 and int(m) != 1:
		if int(m) - 1 < 10:
			m = '0' + str(int(m) - 1)
		else:
			m = str(int(m) - 1)
		return('{0}-{1}-{2}'.format(y, m, getMonthDay(y, m)[-1]))
	elif int(d) == 1 and int(m) == 1:
		return('{0}-12-{1}'.format(str(int(y) - 1), str(getMonthDay(int(y) - 1, 12)[-1])))
	for each_d in reversed(getMonthDay(y, m)):
		if each_d < int(d):
			if each_d < 10:
				each_d = '0' + str(each_d)
			return('{0}-{1}-{2}'.format(y, m, str(each_d)))
def getProcesses():
	EnumObjects(None, None, 0, 1)
	(items, instance) = EnumObjectItems(None, None, "Process", -1)
	return(instance)
def ProcessAction(action, delay):
	sleep(delay)
	if action == 'automation':
		system(Automation)
	elif action == 'keyControl':
		logger.info('Starting control automation...')
		for each_key in ['{DOWN}', '{TAB}', '{ENTER}', 'Path', '{TAB}', '{TAB}', '{TAB}', '{ENTER}', ' ', '+{END}', '{TAB}', '{ENTER}', '{TAB}', 'InputDate', '{TAB}', '{ENTER}']:
			sleep(2)
			if each_key == 'Path':
				kb.SendKeys(SavePath)
			elif each_key == 'InputDate':
				kb.SendKeys(yesterday)
			else:
				kb.SendKeys(each_key)
		sleep(250)
		while(1):
			if basename(Automation).replace('.exe', '') in getProcesses():
				logger.info('Automation is exist, Enter to exit')
				kb.SendKeys('{ENTER}')
			else:
				system('\"{} -s\"'.format(join(iSMART_PATH, basename(iSMART_PATH) + '.exe')))
				sleep(3)
				log_list = []
				for each_log in listdir(iSMART_PATH):
					if search('\w+.log$', each_log):
						log_list.append(each_log)
				with open(join(iSMART_PATH, log_list[0])) as rf:
					for each_line in rf.read().split('\n'):
						if 'erase count' in each_line:
							logger.debug('Drive erase count: ' + each_line)
				for each_rmlog in log_list:
					remove(join(iSMART_PATH, each_rmlog))
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

logger.info("""
======================================================================
\tWelcome fully auto check recording log script
======================================================================
\t\t    Follow below listed caution:
[1] Put the automation tool in desktop follow as below example.
    e.g., "Recording_log_check_Tool_for_vast_vx.x.x.exe"
[2] Put iSMART tool in path "C:\\Program Files (x86)\\VIVOTEK Inc\\
[3] Open VAST Playback program as necessary.
[4] Do not interrupt while script has been executing.
[5] Press keyboard "Ctrl + C" to exit.
======================================================================""")
try:
	while(1):
		yesterday = getYesterday(strftime('%Y'), strftime('%m'), strftime('%d'))
		currentTime, iSMART_PATH = strftime('%H%M'), getProgram('^iSMART\w+', r'C:\Program Files (x86)\VIVOTEK Inc')
		weekday = strftime('%w')
		if weekday in ['2', '3', '4', '5']:
			logger.info('Schduled clear yesterday log file')
			if isfile('FullyAutoCheckScript.log'):
				remove('FullyAutoCheckScript.log')
		if currentTime == '0950':
			logger.debug('Check Date: ' + yesterday)
			thread_1 = MultiProcess('automation', 0)
			thread_2 = MultiProcess('keyControl', 5)
			SavePath = join(join(Desktop, strftime('%Y') + ' ' + getCurrentQ()), yesterday.split('-')[1] + yesterday.split('-')[2])
			logger.debug(SavePath)
			Automation = getProgram('^Recording_log_check_Tool_for_vast_\w+', Desktop)
			logger.debug('Execute Automation: ' + basename(Automation))
			if not getProgram('^Recording_log_check_Tool_for_vast_\w+', Desktop):
				logger.error('\nRecording log check Tool is not found')
				raise Exception
			for each_p in ['VMSPlayback', basename(iSMART_PATH)]:
				if each_p not in getProcesses():
					logger.error('\nProgram {} is not in executed'.format(each_p))
					raise Exception	
			logger.debug('Log Save Path: ' + SavePath)

			if not isdir(SavePath):
				logger.info('Detect directory is not exists, create new one.\nDirectory: ' + SavePath)
				mkdir(SavePath)

			if basename(Automation).replace('.exe', '') in getProcesses():
				logger.info('Detect automation {} is executing in system, kill the process down.'.format(basename(Automation)))
				system('taskkill /f /im ' + basename(Automation))
			thread_1.start()
			thread_2.start()
			isAlive('lt', 3)
			if len(listdir(SavePath)) >= 64 and checkFail(SavePath) == 0:
				logger.info('\n***** Date: {} check continues recording completed! *****\n'.format(yesterday))
			else:
				logger.error('\n***** Date: {} check continues recording failured. *****\n'.format(yesterday))
		sleep(10)
except Exception:
	print('', end='')
except FileNotFoundError as ferr:
	logger.error(str(ferr))
except KeyboardInterrupt:
	logger.info('\nUser press Ctrl+C to exit.')
sleep(2)