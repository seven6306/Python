#!/usr/bin/python3
# 11. Stress
# 11-3: Get SDR list  via IPMI over lan (12 hrs)
#       Boot system to Linux. 
#       Execute the cmd(ipmitool -I lanplus -H <ip> -U <username> -P <password> sdr list) by shell script.
#       BMC should not have abnormal event log.
# (check sel please add "test_6_VerifySEL.py" in pytest input script)

import sys
sys.path.append('./lib')
from PublicModule import *


class TestStressGetSDR(object):
    @mark.order1
    def test_get_sdr(self):
        gLogger.info('\n\n')
        gLogger.debug('\033[93m[11-3]\033[0m \033[1mStress to test get SDR' +
                      'over lan via IPMI command.\033[0m')

        # make the chassis power on for test
        if PowerControl('status')[1] == 'off':
            gLogger.info('\n')
            gLogger.info(' * Detect system power status is: [' +
                         '\033[91moff\033[0m], set to power on for test')
            gLogger.info('\n')
            boolean, err_msg = PowerControl('on')
            if not boolean:
                gLogger.warning(err_msg)
                assert False, err_msg
            WaitingMessage(message='system booting', delay=120)

        # start to test get SDR list, round times variable "gGetSdr"
        # is read from "test_config.ini"
        color = '\033[92m'
        b = ' ' * 4
        cmd_exe_fail_count = 0
        sdr_abnormal_count = 0
        sdr_abnormal_list = []
        sdr_opt = ['NVME', 'DISK']
        ipmi_cmd = 'ipmitool -H ' + gBmcIp +
                   ' -I lanplus -U ' + gUserName +
                   ' -P ' + gPassWord + ' sdr list'
        gLogger.info('\n')
        gLogger.info('\033[1m[Test] Start to execute IPMI command \033[0m' +
                     '\033[93msdr list\033[0m \033[1mfor\033[0m ' +
                     '\033[93m{}\033[0m \033[1mrounds:\033[0m'.format(gGetSdr))
        gLogger.info('=' * 45)
        # list abnormal SDR
        for i in range(1, gGetSdr + 1):
            if i == gGetSdr:
                color = '\033[93m'
            gLogger.debug('\033[93m[\033[0m{0}{1}\033[0m'.format(color, i) +
                          '\033[93m/{}]\033[0m \033[1mTo'.format(gGetSdr) +
                          ' get SDR list.\033[0m')
            try:
			    # execute get sdr list command and parse it to list
                sdr_list = os.popen(ipmi_cmd).read().split('\n')
                [sdr_list.remove('') for e in sdr_list if e == '']
                for i in sdr_list:
                    for j in sdr_opt:
                        for k in range(1, 60):
                            if (i[-2:] != 'ok' and i[:4] not in sdr_opt) or (
                                gSdrVerifyDict[j + str(k)] and j + str(k) in sdr_opt):
                                sdr_abnormal_list.append(i)
                                sdr_abnormal_count += 1
                                gLogger.debug(i)
            except Exception as err:
                gLogger.error(str(err))
                cmd_exe_fail_count += 1
            WaitingMessage(message='next round', delay=9)

        if sdr_abnormal_count == 0:
            gLogger.info('\033[92mNo abnormal SDR in the list\033[0m')
        gLogger.info('=' * 45)
        gLogger.info('\n\n')

        # verify if the fail count is not equals 0 then fail
        cmd_exe_result = '\033[91m' + str(cmd_exe_fail_count) + '\033[0m'
        sdr_abnormal_result = '\033[91m' + str(sdr_abnormal_count) + '\033[0m'
        gLogger.info('\033[1mTest Finished - during the test period:\033[0m')
        gLogger.debug(b + 'Command execute fail count:', cmd_exe_result)
        gLogger.debug(b + 'Abnormal SDR count:', sdr_abnormal_result)

        if cmd_exe_fail_count != 0 or sdr_abnormal_count != 0:
            assert False, 'During the period of get SDR, fail has been found'

        gLogger.info('\n\n')
        gLogger.info('\033[1m=> Test get SDR list for \033[0m\033[91m' +
                     '{}\033[0m rounds completed.\033[0m'.format(gGetSdr))
        gLogger.info('\n\n')
        gLogger.debug('\033[1m ***** [{0}] Test get SDR list via IPMI command [\033[0m{1}\033[1m] *****\033[0m'.format(
                strftime('%Y-%m-%d %H:%M:%S'), gPassGreen))
        assert True
