from sys import argv
from winreg import OpenKey, CreateKey, KEY_ALL_ACCESS, QueryValueEx, SetValueEx, REG_SZ, REG_LINK, HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, HKEY_USERS, HKEY_CURRENT_CONFIG
UsageInfo = """
Usage:
       python Registrar.py [action] [Registry Path] [Registry Key] [Registry Value]
       Argument1 : [action] - set / get / setkey

e.g.,
     python Registrar.py set "HKEY_CURRENT_USER\Software\Skype\Phone" MyPhone 0935111174
     python Registrar.py get "HKEY_LOCAL_MACHINE\SOFTWARE\ODBC\ODBCINST.INI\SQL Server" Driver
     python Registrar.py setkey "HKEY_CURRENT_USER\Software" Fortinet
"""
def Registrar(Action='get', RegPath='', RegName='', RegValue=''):
	try:
		ClassDict = {'HKEY_LOCAL_MACHINE':HKEY_LOCAL_MACHINE, 'HKEY_CURRENT_USER':HKEY_CURRENT_USER, 'HKEY_USERS':HKEY_USERS, 'HKEY_CURRENT_CONFIG':HKEY_CURRENT_CONFIG}
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
				 CreateKey(ClassDict[mainkey], RegRelativePath + '\\' + RegName)
	except FileNotFoundError as regerr:
		print(str(regerr))
if len(argv) == 2 and argv[1] in ['?', '-h', '--help']:
	print(UsageInfo)
elif len(argv) >= 4:
	try:
		action = argv[1]
		keyPath = argv[2]
		keyName = argv[3]
		try:
			keyValue = argv[4]
		except:
			keyValue = ''
			pass
		if action:
			print(Registrar(action, keyPath, keyName, keyValue))
	except Exception as err:
		print(str(err))
		print('Invalid argument')
else:
	print('Try \'python Registrar.py --help\' for more information')