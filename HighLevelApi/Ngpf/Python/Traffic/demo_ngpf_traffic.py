################################################################################
################################################################################

################################################################################
#                                                                              #
#                                LEGAL  NOTICE:                                #
#                                ==============                                #
# The following code and documentation (hereinafter "the script") is an        #
# example script for demonstration purposes only.                              #
# The script is not a standard commercial product offered by Ixia and have     #
# been developed and is being provided for use only as indicated herein. The   #
# script [and all modifications, enhancements and updates thereto (whether     #
# made by Ixia and/or by the user and/or by a third party)] shall at all times #
# remain the property of Ixia.                                                 #
#                                                                              #
# Ixia does not warrant (i) that the functions contained in the script will    #
# meet the user's requirements or (ii) that the script will be without         #
# omissions or error-free.                                                     #
# THE SCRIPT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, AND IXIA        #
# DISCLAIMS ALL WARRANTIES, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,          #
# INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF MERCHANTABILITY AND FITNESS FOR #
# A PARTICULAR PURPOSE OR OF NON-INFRINGEMENT.                                 #
# THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SCRIPT  IS WITH THE #
# USER.                                                                        #
# IN NO EVENT SHALL IXIA BE LIABLE FOR ANY DAMAGES RESULTING FROM OR ARISING   #
# OUT OF THE USE OF, OR THE INABILITY TO USE THE SCRIPT OR ANY PART THEREOF,   #
# INCLUDING BUT NOT LIMITED TO ANY LOST PROFITS, LOST BUSINESS, LOST OR        #
# DAMAGED DATA OR SOFTWARE OR ANY INDIRECT, INCIDENTAL, PUNITIVE OR            #
# CONSEQUENTIAL DAMAGES, EVEN IF IXIA HAS BEEN ADVISED OF THE POSSIBILITY OF   #
# SUCH DAMAGES IN ADVANCE.                                                     #
# Ixia will not be required to provide any software maintenance or support     #
# services of any kind (e.g., any error corrections) in connection with the    #
# script or any part thereof. The user acknowledges that although Ixia may     #
# from time to time and in its sole discretion provide maintenance or support  #
# services for the script, any such services are subject to the warranty and   #
# damages limitations set forth herein and will not obligate Ixia to provide   #
# any additional maintenance or support services.                              #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Description:                                                                 #
# This script configures a scenario with 2 topologies:		                   #
#        - Topology 1 with Ethernet and IPv4 stacks							   #
#        - Topology 2 with Ethernet and IPv4 stacks 						   #
# The script does:										                       #
#    	 - start/stop protocol												   #
# - collect and display IPv4 and Ethernet statistics 				   #
# #
# Module:                                                                      #
#    The sample was tested on a 1GE LSM XMVDC16NG module.                      #
#                                                                              #
################################################################################
# Append paths to python APIs
#sys.path.append('/opt/ixia/hltapi/8.40.1123.18/TclScripts/lib/hltapi/library/common/ixiangpf/python')
#sys.path.append('C:/Program Files (x86)/Ixia/IxNetwork/8.40-EA/API/Python')

from pprint import pprint
import os
import sys
import time
import pdb

# Append paths to python APIs

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

ixiatcl = IxiaTcl()
ixiahlt = IxiaHlt(ixiatcl)
ixiangpf = IxiaNgpf(ixiahlt)


try:
    ErrorHandler('', {})
except (NameError,):
    def ErrorHandler(cmd, retval):
        global ixiatcl

        err = ixiatcl.tcl_error_info()
        log = retval['log']
        additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (
            cmd, err, log)
        raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)

# previous version
#chassis_ip = "10.36.88.71"
#ixnetwork_tcl_server = '10.36.94.244'  
#port_list = ['8/3', '8/4']     

#ixnetwork_tcl_server = '10.36.94.229'  # SY 11.10 ixNetwork web
#ixnetwork_tcl_server = '10.36.94.228'  # SY 10.00 ixNetwork web

chassis_ip = "10.36.88.110"
ixnetwork_tcl_server = '10.36.94.229'  # SY 11.10 ixNetwork web
port_list = ['1/3', '1/4']             #      
cfgErrors = 0


##########################################
##  CONNECT AND PRINT CONNECTION RESULT ##
##########################################

connect_result = ixiangpf.connect(
    ixnetwork_tcl_server=ixnetwork_tcl_server,
    device=chassis_ip,
    port_list=port_list,
    break_locks=1,
    reset=1,
    user_name='admin',      # Linux
    user_password='admin'   # Linux
)

if connect_result['status'] != '1':
    ErrorHandler('connect', connect_result)

pprint(connect_result)

ports = connect_result['vport_list'].split()

result = ixiahlt.interface_config(
    mode='config',
    port_handle = ports, 
    phy_mode = ['fiber', 'fiber']
)

if result['status'] != '1':
    ErrorHandler('interface_config', result)
    
# import pdb; pdb.set_trace()
############################################################
##  CREATING FIRST TOPOLOGY WITH ETHERNET AND IPV4 STACKS ##
############################################################

topology_1 = ixiangpf.topology_config(
    topology_name="{Topology 1}",
    port_handle=ports[0],
)
if topology_1['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', topology_1)

topology_1_handle = topology_1['topology_handle']

# pdb.set_trace()

deviceGroup_1 = ixiangpf.topology_config(
    topology_handle=topology_1_handle,
    device_group_name="{Device Group 1}",
    device_group_multiplier="10",
    device_group_enabled="1",
)
if deviceGroup_1['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', deviceGroup_1)

deviceGroup_1_handle = deviceGroup_1['device_group_handle']
# pdb.set_trace()
mv1 = ixiangpf.multivalue_config(
    pattern="counter",
    counter_start="00.11.01.00.00.01",
    counter_step="00.00.00.00.00.01",
    counter_direction="increment",
    nest_step="00.00.01.00.00.00",
    nest_owner=topology_1_handle,
    nest_enabled="1",
)
# note:  nest_step is port_step in GUI

if mv1['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv1)

multivalue_1_handle = mv1['multivalue_handle']

mv2 = ixiangpf.multivalue_config(
    pattern="custom",
    nest_step="1",
    nest_owner=topology_1_handle,
    nest_enabled="0",
)
if mv2['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv2)

multivalue_2_handle = mv2['multivalue_handle']

mv3 = ixiangpf.multivalue_config(
    multivalue_handle=multivalue_2_handle,
    custom_start="1",
    custom_step="1",
)
if mv3['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv3)

custom_1_handle = mv3['custom_handle']

mv4 = ixiangpf.multivalue_config(
    custom_handle=custom_1_handle,
    custom_increment_value="0",
    custom_increment_count="3",
)
if mv4['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv4)

increment_1_handle = mv4['increment_handle']

interface_1 = ixiangpf.interface_config(
    protocol_name="{Ethernet 1}",
    protocol_handle=deviceGroup_1_handle,
    mtu="1500",
    src_mac_addr=multivalue_1_handle,
    vlan="1",
    vlan_id=multivalue_2_handle,
    vlan_id_step="0",
    vlan_id_count="1",
    vlan_tpid="0x8100",
    vlan_user_priority="0",
    vlan_user_priority_step="0",
    use_vpn_parameters="0",
    site_id="0",
)
if interface_1['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', interface_1)

ethernet_1_handle = interface_1['ethernet_handle']

# pdb.set_trace()

interface_2 = ixiangpf.interface_config(
    protocol_name="{IPv4 1}",
    protocol_handle=ethernet_1_handle,
    ipv4_resolve_gateway="1",
    ipv4_manual_gateway_mac="00.00.00.00.02.01",
    ipv4_manual_gateway_mac_step="00.00.00.00.00.00",
    gateway="100.1.0.1",
    gateway_step="0.0.1.0",
    intf_ip_addr="100.1.0.2",
    intf_ip_addr_step="0.0.1.0",
    netmask="255.255.255.0",
)
if interface_2['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', interface_2)


ipv4_1_handle = interface_2['ipv4_handle']

# pdb.set_trace()

#############################################################
##  CREATING SECOND TOPOLOGY WITH ETHERNET AND IPV4 STACKS ##
#############################################################

topology_2 = ixiangpf.topology_config(
    topology_name="{Topology 2}",
    port_handle=ports[1],
)
if topology_2['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', topology_2)

topology_2_handle = topology_2['topology_handle']

deviceGroup_2 = ixiangpf.topology_config(
    topology_handle=topology_2_handle,
    device_group_name="{Device Group 2}",
    device_group_multiplier="10",
    device_group_enabled="1",
)
if deviceGroup_2['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('topology_config', deviceGroup_2)

deviceGroup_2_handle = deviceGroup_2['device_group_handle']


mv11 = ixiangpf.multivalue_config(
    pattern="counter",
    counter_start="00.12.01.00.00.01",
    counter_step="00.00.00.00.00.01",
    counter_direction="increment",
    nest_step="00.00.01.00.00.00",
    nest_owner=topology_2_handle,
    nest_enabled="1",
)
if mv11['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv11)

multivalue_5_handle = mv11['multivalue_handle']

mv12 = ixiangpf.multivalue_config(
    pattern="custom",
    nest_step="1",
    nest_owner=topology_2_handle,
    nest_enabled="0",
)
if mv12['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv12)

multivalue_6_handle = mv12['multivalue_handle']

mv13 = ixiangpf.multivalue_config(
    multivalue_handle=multivalue_6_handle,
    custom_start="1",
    custom_step="1",
)
if mv13['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv13)

custom_4_handle = mv13['custom_handle']

mv14 = ixiangpf.multivalue_config(
    custom_handle=custom_4_handle,
    custom_increment_value="0",
    custom_increment_count="3",
)
if mv14['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('multivalue_config', mv14)

increment_4_handle = mv14['increment_handle']

interface_3 = ixiangpf.interface_config(
    protocol_name="{Ethernet 2}",
    protocol_handle=deviceGroup_2_handle,
    mtu="1500",
    src_mac_addr=multivalue_5_handle,
    vlan="1",
    vlan_id=multivalue_6_handle,
    vlan_id_step="0",
    vlan_id_count="1",
    vlan_tpid="0x8100",
    vlan_user_priority="0",
    vlan_user_priority_step="0",
    use_vpn_parameters="0",
    site_id="0",
)
if interface_3['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', interface_3)

ethernet_2_handle = interface_3['ethernet_handle']
interface_4 = ixiangpf.interface_config(
    protocol_name="{IPv4 2}",
    protocol_handle=ethernet_2_handle,
    ipv4_resolve_gateway="1",
    ipv4_manual_gateway_mac="00.00.00.00.01.01",
    ipv4_manual_gateway_mac_step="00.00.00.00.00.00",
    gateway="100.1.0.2",
    gateway_step="0.0.1.0",
    intf_ip_addr="100.1.0.1",
    intf_ip_addr_step="0.0.1.0",
    netmask="255.255.255.0",
)
if interface_4['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('interface_config', interface_4)

ipv4_2_handle = interface_4['ipv4_handle']


#############################
##  STARTING ALL PROTOCOLS ##
#############################
# pdb.set_trace()

start = ixiangpf.test_control(action='start_all_protocols')

if start['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('test_control', start)

print("\nSleeping for 10 seconds ... ")
time.sleep(10)

pdb.set_trace()

# enable sequence checking
traffic_config_result = ixiahlt.traffic_config(
    mode='create',
    emulation_src_handle=topology_1_handle,
    emulation_dst_handle=topology_2_handle,
    src_dest_mesh='one_to_one',
    route_mesh='one_to_one',
    bidirectional='1',
    name='Traffic_Item_1',
    circuit_endpoint_type='ipv4',
    track_by='endpoint_pair',
    frame_sequencing='enable',
    frame_sequencing_mode='rx_switched_path_fixed',
)
if traffic_config_result['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_config', traffic_config_result)

stream_id = traffic_config_result['stream_id']
print("\n===>Traffic Config Result ...\n")
pprint(traffic_config_result)

#
# Start traffic configured earlier
#

_result_ = ixiahlt.traffic_control(
    action='apply',
    packet_loss_duration_enable=0,
)
# Check status
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)
_result_ = ixiahlt.traffic_control(
    action='run'
)
# Check status
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

# pdb.set_trace()

# It takes time to apply & start traffic.  The time it takes depends on number of traffic items configured and
# the complexity of each traffic item.
# Below is ixNet low level api code to check the traffic -state to reach 'started' state.
start_time = time.time()
while str(ixiangpf.ixnet.getAttribute('/traffic', '-state')) != 'started':
    curr_time = time.time()
    if curr_time - start_time < 120:
        time.sleep(2)
    else:
        additional_info = 'Unexpected traffic -state after traffic_control action=run.  state = %s' % str(
            ixiangpf.ixnet.getAttribute('/traffic', '-state'))
        raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)

print("\nRun traffic for 10 seconds\n")
time.sleep(10)

# ######################
# stop phase of the test
# ######################
#
# Stop traffic started earlier
#
print('Stopping Traffic...')
_result_ = ixiahlt.traffic_control(
    action='stop'
)
# Check status
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_control', _result_)

start_time = time.time()
while str(ixiangpf.ixnet.getAttribute('/traffic', '-state')) != 'stopped':
    curr_time = time.time()
    if curr_time - start_time < 120:
        time.sleep(2)
    else:
        additional_info = 'Unexpected traffic -state after traffic_control action=stop.  state = %s' % str(
            ixiangpf.ixnet.getAttribute('/traffic', '-state'))
        raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)

print('Stopping all protocol(s) ...')

# pdb.set_trace()

_result_ = ixiahlt.test_control(action='stop_all_protocols')
# Check status
if _result_['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('ixiahlt::traffic_control', _result_)

print('\n\nCollecting traffic stats...\n\n')

# pdb.set_trace()

traffic_stats = ixiangpf.traffic_stats(
    mode='traffic_item',
)
if traffic_stats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_stats', traffic_stats)

print('\n\nIPv4 traffic item stats:\n')
'''
Traffic Item RX side stats counters:
traffic_stats['traffic_item'][stream_id]['rx'].keys()
dict_keys(['pkt_loss_duration', 'l1_bit_rate', 'loss_percent', 'total_pkts_bytes', 'first_tstamp', 'small_error', 'expected_pkts', 'reverse_error', 'total_pkt_rate', 'min_delay', 'loss_pkts', 'avg_delay', 'misdirected_rate', 'total_pkt_kbit_rate', 'misdirected_pkts', 'total_pkt_mbit_rate', 'total_pkt_byte_rate', 'total_pkt_bit_rate', 'last_tstamp', 'total_pkt_bytes', 'big_error', 'max_delay', 'total_pkts'])

Traffic Item TX side stats counters:
traffic_stats['traffic_item'][stream_id]['tx']
{'l1_bit_rate': '347678640.000', 'total_pkt_bit_rate': '270416720.000', 'total_pkt_byte_rate': '33802090.000', 'total_pkt_kbit_rate': '270416.720', 'total_pkt_mbit_rate': '270.417', 'total_pkt_rate': '482887.000', 'total_pkts': '17389126'}
'''

# pdb.set_trace()
t1_tx_total_pkts = traffic_stats['traffic_item'][stream_id]['tx']['total_pkts']
t1_rx_total_pkts = traffic_stats['traffic_item'][stream_id]['rx']['total_pkts']
t1_rx_loss_pkts = traffic_stats['traffic_item'][stream_id]['rx']['loss_pkts']

print("t1_tx_total_pkts = %s " % t1_tx_total_pkts)
print("t1_rx_total_pkts = %s " % t1_rx_total_pkts)
print("t1_rx_loss_pkts = %s " % t1_rx_loss_pkts)

print('\n\nTraffic Item Stats\n')
pprint(traffic_stats)

# need to make sure the waiting_for_stats is 0; if it's 1, need to call traffic_stats once more
# TK debug
print('Get Flow Stats:\n')

traffic_stats = ixiangpf.traffic_stats(
    mode='flow',
)
if traffic_stats['status'] != IxiaHlt.SUCCESS:
    ErrorHandler('traffic_stats', traffic_stats)

# pdb.set_trace()

print('\n\nIPv4 traffic flow stats:\n')
pprint(traffic_stats)

# get number of flows in the stat:
flow_count = len(traffic_stats["flow"].items())
print("==== flow count:  ", flow_count)

# iterate thru each flow stats and print out the total tx/rx pkt count and loss pkt count
for key, value in traffic_stats["flow"].items():
    # print("==== flow: {key} ====")
    # print(f"==== flow: , key, 1====")
    # print(f"\ttx total_pkts: {value['tx']['total_pkts']}")
    # print(f"\trx total_pkts: {value['rx']['total_pkts']}")
    # print(f"\trx loss_pkts: {value['rx']['loss_pkts']}")
    print("==== flow: ", key, " ====")
    print("\ttx total_pkts: ", value['tx']['total_pkts'])
    print("\trx total_pkts: ", value['rx']['total_pkts'])
    print("\trx loss_pkts: ", value['rx']['loss_pkts'])


# Below is example on how to retrieve 1st flow's rx total_pkts
print('\n---Flow 1 RX total_pkts: ',
      traffic_stats['flow']['1']['rx']['total_pkts'])

print("\n\nScript ended SUCCESSFULLY!")
