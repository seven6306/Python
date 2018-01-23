from re import search
from time import sleep, strftime
from win32com.client import Dispatch
from configparser import ConfigParser
from datetime import datetime, timedelta
from threading import Thread, active_count
from win32pdh import EnumObjects, EnumObjectItems
from os.path import join, isdir, isfile, basename
from os import system, environ, mkdir, listdir, remove, chdir, getcwd
from logging import basicConfig, DEBUG, getLogger, StreamHandler, Formatter
from win32gui import EnumWindows, GetWindowText, ShowWindow, SetForegroundWindow

pwd = getcwd()
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
	logger.debug('Fail count: {} item found.'.format(str(len(FAIL_LIST))))
	return(len(FAIL_LIST))
def getProgram(fileReg, dir):
	for each_file in listdir(dir):
		if search(fileReg, each_file):
			return(join(dir, each_file))
def getProcesses():
	EnumObjects(None, None, 0, 1)
	(items, instance) = EnumObjectItems(None, None, "Process", -1)
	return(instance)
def readConfig(fileName):
	global ch_num, switch, exe_time, Automation, iSMART_PATH, VB_script_steps
	try:
		config = ConfigParser()
		config.read(fileName)
		ch_num, switch, exe_time = int(config.get('Settings', 'CHANNEL_NUMBER')), config.get('Settings', 'AUTO_CLEAR_iSMART_LOG').upper(), config.get('Settings', 'EXE_TIME')
		Automation, iSMART_PATH = config.get('Path', 'AUTOMATION_TOOL'), config.get('Path', 'iSMART_PATH')
		VB_script_steps = config.get('VB_Script', 'SCRIPT_STEPS').split('>')
	except:
		pass
		logger.info('Invalid format of "AutoCheckConfig.ini", initialize varibles...')
		ch_num, switch, exe_time = 64, 'ON', '0945'
		Automation, iSMART_PATH = getProgram('^Recording_log_check_Tool_for_vast_\w+', Desktop), getProgram('^iSMART\w+', r'C:\Program Files (x86)\VIVOTEK Inc')
		VB_script_steps = ['{DOWN}', '{TAB}', '{ENTER}', 'Path', '{TAB}', '{TAB}', '{TAB}', '{ENTER}', ' ', '+{END}', '{TAB}', '{ENTER}', '{TAB}', 'InputDate', '{TAB}', '{ENTER}']
def Waiting(dot='.'):
	for i in range(1,6):
		if i == 5:
			print('                           \r', end='')
			print('Waiting for schedule \r', end='')
		else:
			print('Waiting for schedule {}\r'.format(dot*i), end='')
		sleep(2)
def ProcessAction(action, delay):
	sleep(delay)
	if action == 'automation':
		system(Automation)
	elif action == 'keyControl':
		logger.info('Starting control automation...')
		for each_key in VB_script_steps:
			sleep(2)
			if each_key == 'Path':
				kb.SendKeys(SavePath)
			elif each_key == 'InputDate':
				kb.SendKeys(yesterday)
			else:
				kb.SendKeys(each_key)
		sleep(300)
		round = 0
		while(1):
			if basename(Automation).replace('.exe', '') in getProcesses():
				if round == 1:
					logger.info('Automation still exists, kill the process')
					system('taskkill /f /im ' + basename(Automation))
				else:
					logger.info('Automation is exist, Enter to exit')
					sleep(1)
					kb.SendKeys('{ENTER}')
				round = round + 1
			else:
				chdir(iSMART_PATH)
				logger.info('Execute iSMART command to generate drive information log.')
				system('\"{}\" -s'.format(join(iSMART_PATH, basename(iSMART_PATH) + '.exe')))
				sleep(10)
				chdir(pwd)
				try:
					log_list = []
					for each_log in listdir(iSMART_PATH):
						if search('\w+.log$', each_log):
							log_list.append(each_log)
					with open(join(iSMART_PATH, log_list[-1])) as rf:
						for each_line in rf.read().split('\n'):
							if 'Erase Count Avg.' in each_line:
								logger.debug('Drive erase count: ' + each_line.split('\t')[2])
					if switch == 'ON':
						try:
							for each_rmlog in log_list:
								remove(join(iSMART_PATH, each_rmlog))
						except Exception as err:
							logger.error(str(err))
							pass
				except IOError:
					logger.debug('Log file is not found')
					pass
				break
			sleep(3)
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
[1] Recording check tool default path in Desktop.
[2] iSMART default path in "C:\\Program Files (x86)\\VIVOTEK Inc\\
[3] Edit AutoCheckConfig.ini for script configuration.
[4] Run VAST Playback program before this.
[5] Do not interrupt while script in executing.
[6] Press keyboard "Ctrl + C" to stop service.
======================================================================""")
try:
	readConfig('AutoCheckConfig.ini')
	while(1):
		yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
		weekday, currentTime = strftime('%w'), strftime('%H%M')
		if not getProgram('^Recording_log_check_Tool_for_vast_\w+', Desktop):
			logger.error('\nRecording log check Tool is not found')
			raise Exception
		if 'VMSPlayback' not in getProcesses():
			logger.error('\nProgram VMSPlayback is not in executed')
			raise Exception
		if currentTime == exe_time:
			print('                           \r', end='')
			if weekday in ['2', '3', '4', '5']:
				logger.info('Schduled clear history log file')
				for each_log in listdir(Desktop):
					try:
						if search('FullyAutoCheckScript_\w+.log$', each_log):
							remove(join(Desktop, each_log))
					except:
						pass
			logger.debug('Recording date: ' + yesterday)
			thread_1 = MultiProcess('automation', 0)
			thread_2 = MultiProcess('keyControl', 5)
			SavePath = join(join(Desktop, strftime('%Y') + ' ' + getCurrentQ()), yesterday.split('-')[1] + yesterday.split('-')[2])
			logger.debug('Automation: ' + basename(Automation))
			logger.debug('Log save path: ' + join(Desktop, 'FullyAutoCheckScript.log'))

			if not isdir(SavePath):
				try:
					logger.info('Detect directory is not exists, create new one.\nDirectory: ' + SavePath)
					mkdir(SavePath)
				except Exception as err:
					pass
					logger.error(str(err))

			if basename(Automation).replace('.exe', '') in getProcesses():
				logger.info('Detect automation {} is executing in system, kill the process down.'.format(basename(Automation)))
				system('taskkill /f /im ' + basename(Automation))
			thread_1.start()
			thread_2.start()
			isAlive('lt', 2)
			[kb.SendKeys(i) for i in ['%', ' ', 'N']]
			sleep(1)
			if len(listdir(SavePath)) >= ch_num and checkFail(SavePath) == 0:
				logger.info('\n***** [{0}] Date: {1} check continues recording completed! *****\n'.format(strftime('%Y/%m/%d'), yesterday))
			else:
				logger.error('\n***** [{0}] Date: {1} check continues recording failured. *****\n'.format(strftime('%Y/%m/%d'), yesterday))
		else:
			Waiting()
		sleep(5)
except Exception:
	print('', end='')
except FileNotFoundError as ferr:
	logger.error(str(ferr))
except KeyboardInterrupt:
	logger.info('\nUser press Ctrl+C to exit.')
sleep(2)
