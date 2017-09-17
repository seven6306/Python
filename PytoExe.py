#!/usr/bin/python3
UsageInfo = '''
Usage: ./PytoExe [Script] [Option]
     This tool support Windows and Linux system, easily convert Python
     script to executable program.

     -ico, --icon       Convert script with icon logo, please put
                        icon image: "image.ico" under this directory
     -nwd, --nowindow   Convert script to exe without window
     -res, --resource   Keep resource files alive
      e.g.,
           ./PytoExe example.py --resource
'''
from sys import argv
from re import search
from shutil import move, rmtree
from os.path import isfile
from os import getcwd, remove, system, listdir
def fileList(extension=''):
	templist = []
	for each_ico in listdir():
		if search('\w+\.{}$'.format(extension), each_ico):
			templist.append(each_ico)
	return(templist)
def Check_Package():
	if not isfile('/usr/bin/pip3'):
		system('sudo apt-get install python3-pip -y')
	if not isfile('/usr/local/bin/pyinstaller'):
		system('sudo pip3 install pyinstaller')
	if isfile('/usr/bin/pip3') and isfile('/usr/local/bin/pyinstaller'):
		return(True)
	else:
		return(False)
try:
	script = argv[1]
	if script in ['-h', '--help', '?']:
		raise ImportWarning
	if not search('\w+\.py$', script):
		errtext = 'Invalid python script name'
		raise ImportError
	try:
		if len(argv) > 2:
			option = argv
			for rm_argv in [argv[0], argv[1]]:
				option.remove(rm_argv)
			for each_argv in option:
				if each_argv not in ['-res', '--resource', '-nwd', '--nowindow', '-ico', '--icon']:
					raise Exception
		else:
			option = []
	except:
		pass
		raise Exception
	option_ = ''
	if '-nwd' in option or '--nowindow' in option:
		option_ = '-w'
	if '-ico' in option or '--icon' in option:
		if len(fileList('ico')) == 0:
			errtext = 'Icon image is not found'
			raise ImportError
		option_ = '{0} -i {1}'.format(option_, fileList('ico')[0])
	if not Check_Package():
		errtext = 'Requirements install failed.'
		raise ImportError
	system('pyinstaller -F {0} {1}'.format(option_, script))
	try:
		move('dist/{}'.format(script.replace('.py', '')), getcwd())
		if '-res' not in option and '--resource' not in option:
			for rm_f in ['__pycache__', 'build', 'dist']:
				rmtree(rm_f)
			remove(script.replace('.py', '.spec'))
	except Exception as err:
		print(str(err))
except ImportWarning:
	pass
	print(UsageInfo)
except ImportError:
	pass
	print('{}'.format(errtext))
except:
	pass
	print('Invalid argument: Try \'PytoExe --help\' for more information')