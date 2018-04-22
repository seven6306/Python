#!/usr/bin/python3
# 11. Stress
# 11-1: DC Power cycle via IPMI over lan (12 hrs)
#       Boot system to Linux. 
#       Execute ipmi cmd by shell script.
#       BMC should not have abnormal event log.
# (check sel please add "test_6_VerifySEL.py" in pytest input script)

import sys
sys.path.append('./lib')
from PublicModule import *


class TestStressPowerCycle(object):
    @mark.order1
    def test_pwr_cycle(self):
        gLogger.info('\n\n')
        gLogger.debug('\033[93m[11-1]\033[0m \033[1mStress to test DC ' +
                      'Power cycle via IPMI command.\033[0m')

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
            WaitingMessage(message='system booting', delay=60)

        # start to test power cycle, round times variable 
        # "gPwrCyc" is read from "test_config.ini"
        color = '\033[92m'
        b = ' ' * 9
        power_on_fail_count = 0
        power_off_fail_count = 0
        gLogger.info('\n')
        gLogger.info('\033[1m[Test] Start to run power \033[0m' +
                     '\033[93mCYCLE\033[0m \033[1mfor\033[0m ' +
                     '\033[93m{}\033[0m \033[1mrounds:\033[0m'.format(gPwrCyc))
        gLogger.info('=' * 80)
        for i in range(1, gPwrCyc + 1):
            if i == gPwrCyc:
                color = '\033[93m'
            gLogger.debug('\033[93m[\033[0m{0}{1}\033[0m'.format(color, i) +
                          '\033[93m/{}]\033[0m \033[1mSet'.format(gPwrCyc) +
                          ' chassis power cycle.\033[0m')
            PowerControl('cycle')

            # check during power cycle the chassis power is off
            if isPowerCycle(timeout=120):
                gLogger.debug(b + 'check status is off [\033[92mOK\033[0m]')
            else:
                power_off_fail_count += 1
                gLogger.warning(b + 'check status is off [\033[92mFAIL\033[0m]')
            WaitingMessage(message='system buffering', delay=60)

            # check after power cycle the status is power "on"
            boolean = PowerControl('status', 'on')[0]
            if boolean:
                gLogger.debug(b + 'check status is on  [\033[92mOK\033[0m]')
            else:
                power_on_fail_count += 1
                gLogger.warning(b + 'check status is on  [\033[92mFAIL\033[0m]')

        gLogger.info('=' * 80)
        gLogger.info('\n\n')

        # verify if the fail count is not equals 0 then fail
		power_off_result = '\033[91m' + str(power_off_fail_count) + '\033[0m'
		power_on_result = '\033[91m' + str(power_on_fail_count) + '\033[0m'
        gLogger.info('\033[1mTest Finished - during the test period:\033[0m')
        gLogger.debug(' ' * 4 + 'Power off fail count:', power_off_result)
        gLogger.debug(' ' * 4 + 'Power on  fail count:', power_on_result)

        if power_off_fail_count != 0 or power_on_fail_count != 0:
            assert False, 'During the period of power cycle, fail has been found'

        gLogger.info('\n\n')
        gLogger.info('\033[1m=> Test DC power cycle for \033[0m\033[91m' +
                     '{}\033[0m rounds completed.\033[0m'.format(gPwrCyc))
        gLogger.info('\n\n')
        gLogger.debug('\033[1m ***** [{0}] Test DC power cycle via IPMI command [\033[0m{1}\033[1m] *****\033[0m'.format(
                strftime('%Y-%m-%d %H:%M:%S'), gPassGreen))
        assert True
