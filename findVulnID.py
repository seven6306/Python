#!/usr/bin/python3
UsageInfo = """
Usage: ./findVulnID [Type] [IP Address] [Quality] [LogFile] [vulnerability ID]
     This tool use for Trend Micro Inc. QA test, It mostly used to filiter
     vulnerability in nmaplog generated by ./isc_sample_1059, and generate
     result file at last.

     Argument: {IP Address, vulnerability ID} required use ',' to split each IP or ID
     e.g.,
         ./findVulnID Normal 192.168.2.130 A nmap.log YM_IPCAM_CVE-2017-8225
         ./findVulnID Quick 192.168.1.10,192.168.1.12 B nmap_Quick_192.168.1.10,192.168.1.12_4_B YM_WANNACRY_MS17-010,YM_POODLE_CVE-2014-3566
"""
import datetime
from sys import argv
from re import search
from os.path import isfile
template1 = """
NAME={0}_{2}_Scan_{1}_{3}

IP = [ {2} ]
"""
template2 = """
Total Vulnerability Found Amount: {1}

Scan Type: [ {0} ]
============================================================================== 
{2}
==============================================================================

Result: {3}
"""
def GetVulnID(file='', is_vuln=''):
	templist = []
	vulnlist = []
	try:
		with open(file, 'r') as rf:
			NmapLog = rf.read()
			for each_line in NmapLog.split('\n'):
				if search('^API.*\"}$', each_line):
					templist.append(each_line)
			API = templist[-1]
			templist = []
			for each_line in API.split('{'):
				if search('^\"id\":\".*\",\"is_vuln\":(true|false)', each_line):
					templist.append(each_line.split(',\"risk')[0])
	except IOError as ioerr:
		print(str(ioerr))
	if is_vuln == 'API':
		return(API)
	elif is_vuln != '':
		for each_line in templist:
			if search('{}$'.format(is_vuln), each_line):
				vulnlist.append(each_line)
		return(vulnlist)
	else:
		return(templist)
try:
	if argv[1] in ['-h', '--help', '?']:
		raise ImportError
	findID_list = []
	Type = argv[1]
	IPaddr = argv[2]
	Quality = argv[3]
	filename = argv[4]
	findID = argv[5]
	date = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
	if findID == '':
		raise Exception
	if isfile(filename):
		for each_id in findID.split(','):
			for each_line in GetVulnID(filename, 'true'):
				if '\"id\":\"{}\",\"is_vuln\":'.format(each_id) in each_line:
					findID_list.append(each_line)
		print(template1.format(date, Type, IPaddr, Quality))
		print('Vulnerability Details:\n')
		set([print('\t' + t) for t in GetVulnID(filename)])
		print('\nSearching Vulnerability List:\n')
		set([print('\t' + t) for t in findID_list])
		vuln_num = len(findID_list)
		if vuln_num == 0:
			findID_list.append('Vulnerability not found')
			result = 'Failed'
		elif vuln_num == len(findID.split(',')):
			result = 'Passed'
		else:
			result = 'Failed'
		print(template2.format(Type, vuln_num, GetVulnID(filename, 'API'), result))
	else:
		print('ERROR: file {} is not found.'.format(filename))
except ImportError:
	pass
	print(UsageInfo)
except:
	pass
	print('Invalid argument: Try \'findVulnID --help\' for more information')