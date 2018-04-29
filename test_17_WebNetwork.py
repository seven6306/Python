#!/usr/bin/python3
# 9. Web UI
# 9-1: Dashboard
#      Network information - Verify the all of Lan information are correct.

import sys
sys.path.append('./lib')
from PublicModule import *


class TestWebUserInterface(object):
    @mark.order1
    def test_network(self):
        gLogger.info('\n\n')
        gLogger.debug('\033[93m[9-1]\033[0m \033[1mVerify the all of lan' +
                      ' information are correct.\033[0m')

        # get network settings by IPMI command and parse data
        ft = ''
        idx = 0
        fail_item_count = 0
        ipmi_dict = {}
        ipmi_dict_v6 = {}
        mark1 = '\033[94m(ipmi)\033[0m'
        mark2 = '\033[93m(web)\033[0m'
        key_list = ['Source',
                    'IP Address',
                    'Subnet Mask',
                    'MAC Address',
                    'Default Gateway IP',
                    '802.1q VLAN ID']

        item_list = ['IP Address Source',
                     'IP Address',
                     'Subnet Mask',
                     'MAC Address',
                     'Default Gateway IP',
                     'VLAN ID']

        ipmi_cmd = ''.join(['ipmitool -H {}'.format(gBmcIp),
                            ' -I lanplus -U {}'.format(gUserName),
                            ' -P {} lan'.format(gPassWord)])
        try:
            for i in [1, 8]:
                if os.system(ipmi_cmd +
                             ' print ' +
                             str(i) +
                             ' >> /dev/null 2>&1') == 0:
                    # ipv4
                    tmp = os.popen(ipmi_cmd + ' print ' + str(i)).read()
                    if 'Invalid channel:' not in tmp and 'IP Address' in tmp:
                        tmp_dict = {}
                        d_list = tmp.split('\n')
                        for j in d_list:
                            for k in key_list:
                                if k in j:
                                    key = j.split(' : ')[0].strip()
                                    value = j.split(' : ')[1].strip()
                                    tmp_dict[key] = value
                        ipmi_dict['eth' + str(idx)] = tmp_dict
                    # ipv6
                    tmp = os.popen(ipmi_cmd + '6 print ' + str(i)).read()
                    if 'Invalid channel:' not in tmp and 'IPv6' in tmp:
                        tmp_dict = {}
                        d_list = tmp.split('\n')
                        idx1 = int(''.join(str(i) for i, e in enumerate(d_list)
                                   if 'IPv6 Static Address 0:' in e))
                        idx2 = int(''.join(str(i) for i, e in enumerate(d_list)
                                   if 'DHCPv6 Dynamic DUID Storage Length' in e))
                        d_list = tmp.split('\n')[idx1:idx2]
                        for i, e in enumerate(d_list):
                            if 'IPv6 Static Address' in e:
                                tmp_dict[e[:-1]] = {
                                'Enabled': d_list[i + 1].split(': ')[1].strip(),
                                'Address': d_list[i + 2].split(': ')[1].strip(),
                                'Status':  d_list[i + 3].split(': ')[1].strip(),
                                }
                            elif 'IPv6 Dynamic Address' in e:
                                tmp_dict[e[:-1]] = {
                                'Source/Type': d_list[i + 1].split(': ')[1].strip(),
                                'Address': d_list[i + 2].split(': ')[1].strip(),
                                'Status':  d_list[i + 3].split(': ')[1].strip(),
                                }
                        ipmi_dict_v6['eth' + str(idx) + '_v6'] = tmp_dict
                    idx += 1
        except Exception as err:
            gLogger.error(str(err))
            assert False, 'unexpected error command execute failed.'

        # get network settings by web API and parse data
        api_dict = {}
        api = RestfulApi()
        network_list = api.GetInformation(api='settings/network')
        api.Close()

        # if session create failed
        if 'cc' in network_list:
            if network_list['cc'] == 7:
                gLogger.warning('\033[1mMax retries exceeded request' +
                                ' from web api.\033[0m')
        if not isinstance(network_list, list):
            network_list = [network_list]

        for i, e in enumerate(network_list):
            for j in range(0,10):
                if network_list[i]['interface_name'] == 'eth' + str(j):
                    api_dict['eth' + str(j)] = network_list[i]

        # compare the data betweeen ipmi and web
        if len(ipmi_dict) == len(api_dict):
            for i in range(len(ipmi_dict)):
                intf = 'eth' + str(i)
                tmp_list1 = [ipmi_dict[intf]['IP Address Source'],
                             ipmi_dict[intf]['IP Address'],
                             ipmi_dict[intf]['Subnet Mask'],
                             ipmi_dict[intf]['MAC Address'].upper(),
                             ipmi_dict[intf]['Default Gateway IP'],
                             ipmi_dict[intf]['802.1q VLAN ID']]

                if api_dict[intf]['ipv4_dhcp_enable'] == 1:
                    ipv4_status = 'DHCP Address'
                else:
                    ipv4_status = 'Static Address'
                if api_dict[intf]['vlan_id'] == 0:
                    vlan_id = 'Disabled'
                else:
                    vlan_id = 'Enabled'
                tmp_list2 = [ipv4_status,
                             api_dict[intf]['ipv4_address'],
                             api_dict[intf]['ipv4_subnet'],
                             api_dict[intf]['mac_address'],
                             api_dict[intf]['ipv4_gateway'],
                             vlan_id]
                api_dict[intf]['ipv6_enable']

                gLogger.debug('')
                gLogger.debug('\033[1m## Print NIC - {} (ipv4)\033[0m'.format(intf))
                gLogger.debug('=' * 45)
                for j, e in enumerate(item_list):
                    if tmp_list1[j] != tmp_list2[j]:
                        ft = '\033[91m <- mis-match\033[0m'
                        fail_item_count += 1
                    gLogger.debug(' {0}{1}'.format(e, ft))
                    gLogger.debug('    {2} {0} {1}'.format(tmp_list1[j],
                                                           mark1,
                                                           gTreeBranch))
                    gLogger.debug('    {2} {0} {1}'.format(tmp_list2[j],
                                                           mark2,
                                                           gTreeRoot))
                    
                gLogger.debug('=' * 45)
                gLogger.debug('')


                #compare ipv6 data between api and ipmi
                gLogger.debug('')
                gLogger.debug('\033[1m## Print NIC - {} (ipv6)\033[0m'.format(intf))
                gLogger.debug('=' * 45)
                static_list = []
                dynamic_list = []
                t1 = 'ipv6_enable'
                t2 = 'ipv6_dhcp_enable'
                v6_type_list = ['IPv6 Static Address', 'IPv6 Dynamic Address']

                # sort the list
                for e_d in sorted(ipmi_dict_v6[intf + '_v6']):
                    if int(e_d[-2:]) < 10:
                        e_d = e_d[:-1] + '0' + e_d[-1]
                    if 'Static' in e_d:
                        static_list.append(e_d)
                    else:
                        dynamic_list.append(e_d)
                static_list.sort()
                dynamic_list.sort()
                for k in static_list + dynamic_list:
                    if int(k[-2:]) < 10:
                        k = k[:-2] + k[-1]
                    gLogger.debug(' ' + k)
                    n = 0
                    for key, value in ipmi_dict_v6[intf + '_v6'][k].items():
                        correct = ''
                        # ipv6: off, ipv6_dhcp = off
                        if api_dict[intf][t1] == 0 and api_dict[intf][t2] == 0:
                            if v6_type_list[0] in k:
                                for e_k in ['Enabled=no', 'Status=active']:
                                    kk = e_k.split('=')[0]
                                    vv = e_k.split('=')[1]
                                    if key == kk and value != vv:
                                        correct = '\033[91m <- must be {}\033[0m'.format(vv)
                            elif v6_type_list[1] in k:
                                for e_k in ['Status=disabled']:
                                    kk = e_k.split('=')[0]
                                    vv = e_k.split('=')[1]
                                    if key == kk and value != vv:
                                        correct = '\033[91m <- must be {}\033[0m'.format(vv)
                        # ipv6: on, ipv6_dhcp = off
                        elif api_dict[intf][t1] == 1 and api_dict[intf][t2] == 0:
                            if v6_type_list[0] in k:
                                for e_k in ['Enabled=yes', 'Status=active']:
                                    kk = e_k.split('=')[0]
                                    vv = e_k.split('=')[1]
                                    if key == kk and value != vv:
                                        correct = '\033[91m <- must be {}\033[0m'.format(vv)
                            elif v6_type_list[1] in k:
                                for e_k in ['Status=active']:
                                    kk = e_k.split('=')[0]
                                    vv = e_k.split('=')[1]
                                    if key == kk and value != vv:
                                        correct = '\033[91m <- must be {}\033[0m'.format(vv)
                        # ipv6: on, ipv6_dhcp = on
                        elif api_dict[intf][t1] == 1 and api_dict[intf][t2] == 1:
                            if v6_type_list[0] in k:
                                for e_k in ['Enabled=no']:
                                    kk = e_k.split('=')[0]
                                    vv = e_k.split('=')[1]
                                    if key == kk and value != vv:
                                        correct = '\033[91m <- must be {}\033[0m'.format(vv)
                            elif v6_type_list[1] in k:
                                for e_k in ['Status=active']:
                                    kk = e_k.split('=')[0]
                                    vv = e_k.split('=')[1]
                                    if key == kk and value != vv:
                                        correct = '\033[91m <- must be {}\033[0m'.format(vv)
                        tab = ''
                        tree = gTreeBranch
                        if n == 2:
                            tree = gTreeRoot
                        if len(key) < 8:
                            tab = '\t'
                        if not correct:
                            fail_item_count += 1
                        gLogger.debug('    {3} {0}\t{1}{2}{4}'.format(key,
                                                                   tab,
                                                                   value,
                                                                   tree,
                                                                   correct))
                        n += 1

                gLogger.debug('=' * 45)
                gLogger.debug('')


        # verify fail item count is equals "0"
        if fail_item_count != 0:
            gLogger.warning('\033[91mnetwork setting is mis-match.\033[0m')
            assert False, 'network setting is mis-match.'

        gLogger.info('')
        gLogger.info('\033[1m=> All the lan information are correct.\033[0m')
        gLogger.info('\n')
        gLogger.debug(
            '\033[1m ***** [{0}] Verify the all of lan information via web [\033[0m{1}\033[1m] *****\033[0m'.format(
                strftime('%Y-%m-%d %H:%M:%S'), gPassGreen))
        assert True
