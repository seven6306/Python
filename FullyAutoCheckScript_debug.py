from datetime import datetime, timedelta

def getLastDate(day=1):
	return((datetime.today() - timedelta(days=day)).strftime('%Y-%m-%d'))

def readConfig():
	try:
		global Automation, iSMART_PATH
		with open('configuration.txt') as rconf:
			for each_line in rconf.read().split('\n'):
				if isfile(each_line):
					Automation = each_line
				elif isdir(each_line):
					iSMART_PATH = each_line
			logger.info('Read the file: "configuration.txt" to define varibles.')
	except IOError as ioerr:
		logger.error(str(ioerr))
try:
	exe_round, d_list = 1, [getLastDate(3), getLastDate(2), getLastDate(1)]
	while(1):
		readConfig()
		yesterday = d_list[exe_round - 1]
		if 'Automation' not in globals():
			Automation = getProgram('^Recording_log_check_Tool_for_vast_\w+', Desktop)
		if 'iSMART_PATH' not in globals():
			iSMART_PATH = getProgram('^iSMART\w+', r'C:\Program Files (x86)\VIVOTEK Inc')
		...
		...
		...
		exe_round = exe_round + 1
		if exe_round == len(d_list):
			break
		sleep(10)
except Exception:
	print('', end='')
except FileNotFoundError as ferr:
	logger.error(str(ferr))
except KeyboardInterrupt:
	logger.info('\nUser press Ctrl+C to exit.')
sleep(2)