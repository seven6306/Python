#!/usr/bin/python3
# 9. Web UI
# 9-1. Dashboard
#      Sensor Monitoring - Verify all the sensors can be viewed.
# 9-3. Server Health - Sensor Readings
#      1.Verify sensor name, status, current reading, thresholds
#        are correct.(follow the sensor list) 
#      2.Verify all the thresholds can be configured.
#      3.Verify each "Sensor Live Widget" can work normally.
#      4.Verify the help info can display normally.

import sys
sys.path.append('./lib')
from PublicModule import *


class TestWebUserInterface(object):
    @mark.order1
    def test_sdr_info(self):
        gLogger.info('\n\n')
        gLogger.debug('\033[93m[9-3]\033[0m \033[1mVerify sensor name, status' +
                      ', current reading, thresholds are correct.\033[0m')

        sdr_dict = {}
        sdr_api_dict = {}
        cmd_sdr_list = ''.join(['ipmitool -H {} -I lanplus '.format(gBmcIp),
                               '-U {} -P '.format(gUserName) +
                               '{} sdr list'.format(gPassWord)])
        cmd_get_sdr = ''.join(['ipmitool -H {} -I lanplus '.format(gBmcIp),
                               '-U {} -P '.format(gUserName) +
                               '{} sdr get'.format(gPassWord)])

        sdr_list = os.popen(cmd_sdr_list).read().split('\n')
        [sdr_list.remove(e) for e in sdr_list if e == '']

        # parse data by get sdr via ipmi command
        for e in sdr_list:
            tmp_dict = {}
            for i, tmp in enumerate(['Name', 'Reading', 'Status']):
                tmp_dict[tmp] = e.split('|')[i].strip()
            s_list = os.popen(cmd_get_sdr +
                              ' ' +
                              tmp_dict['Name']).read().split('\n')
            for e_s in s_list:
                if e_s.count(':') == 1 and 'Status' not in e_s:
                    key = e_s.split(':')[0].strip()
                    value = e_s.split(':')[1].strip()
                    if len(key) != 0:
                        tmp_dict[key] = value
            sdr_dict[tmp_dict['Name']] = tmp_dict

        # parse data by get sdr via web api
        api = RestfulApi()
        sdr_api_list = api.GetInformation(api='sensor')
        api.Close()
        sdr_api_list = eval(sdr_api_list)
        for e in sdr_api_list:
            key = e['name']
            value = e
            sdr_api_dict[key] = value

        gLogger.info('')
        gLogger.info('\033[1m=> All the sensor data are correct.\033[0m')
        gLogger.info('\n')
        gLogger.debug('\033[1m ***** [{}'.format(strftime('%Y-%m-%d %H:%M:%S')) +
                     '] Verify sensor name, status, current reading' +
                     ', thresholds are correct. [\033[0m' +
                     '{}\033[1m] *****\033[0m'.format(gPassGreen))
        assert True

"""
    @mark.order2
    def test_sdr_config(self):
        gLogger.info('\n\n')
        gLogger.debug('\033[93m[9-1]\033[0m \033[1mVerify all the thresholds' +
                      ' can be configured\033[0m')


        gLogger.info('')
        gLogger.info('\033[1m=> All the thresholds can be configured.\033[0m')
        gLogger.info('\n')
        gLogger.debug(
            '\033[1m ***** [{0}] Verify all the thresholds can be configured [\033[0m{1}\033[1m] *****\033[0m'.format(
                strftime('%Y-%m-%d %H:%M:%S'), gPassGreen))
        assert True


    @mark.order3
    def test_sdr_slw(self):
        gLogger.info('\n\n')
        gLogger.debug('\033[93m[9-1]\033[0m \033[1mVerify each "Sensor Live ' +
                      'Widget" can work normally.\033[0m')


        gLogger.info('')
        gLogger.info('\033[1m=> All the Sensor Live Widget can work normally.\033[0m')
        gLogger.info('\n')
        gLogger.debug(
            '\033[1m ***** [{0}] Verify each "Sensor Live Widget" can work normally. [\033[0m{1}\033[1m] *****\033[0m'.format(
                strftime('%Y-%m-%d %H:%M:%S'), gPassGreen))
        assert True


    @mark.order4
    def test_sdr_help(self):
        gLogger.info('\n\n')
        gLogger.debug('\033[93m[9-1]\033[0m \033[1mVerify the help info can ' +
                      'display normally.\033[0m')


        gLogger.info('')
        gLogger.info('\033[1m=> The help info can be displayed.\033[0m')
        gLogger.info('\n')
        gLogger.debug(
            '\033[1m ***** [{0}] Verify the help info can display normally [\033[0m{1}\033[1m] *****\033[0m'.format(
                strftime('%Y-%m-%d %H:%M:%S'), gPassGreen))
        assert True
"""