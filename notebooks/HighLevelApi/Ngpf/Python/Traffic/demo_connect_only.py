
from pprint import pprint
import os
import sys
import time
import pdb

import yaml
def load_config(config_file_path):
    with open(config_file_path, 'r') as file:
        try:
            # Use safe_load to safely parse the YAML content
            config_data = yaml.safe_load(file)
            return config_data
        except yaml.YAMLError as exc:
            print(exc)
            return None

os.chdir(os.path.dirname(os.path.abspath(__file__)))
config=load_config('ixnetwork_config_chassis_88_116.yaml')

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
ixnetwork_tcl_server = config['session']['IpAddress']

#chassis_ip = "10.36.88.17" # Chassis 11.10
#port_list = ['1/5', '1/6']  # The ports from 88.110
chassis_ip = config['portMap'][0]['IpAddress']
port_list = [
             str(config['portMap'][0]['CardId'])+'/'+str(config['portMap'][0]['PortId']),
             str(config['portMap'][1]['CardId'])+'/'+str(config['portMap'][1]['PortId'])
            ]
cfgErrors = 0


##########################################
##  CONNECT AND PRINT CONNECTION RESULT ##
##########################################

connect_result = ixiangpf.connect(
    ixnetwork_tcl_server=ixnetwork_tcl_server,
    close_server_on_disconnect=0,
    device=chassis_ip,
    port_list=port_list,
    break_locks=1,
    reset=1,
    user_name=config['session']['UserName'],
    user_password=config['session']['Password']
)

if connect_result['status'] != '1':
    ErrorHandler('connect', connect_result)

pprint(connect_result)

ports = connect_result['vport_list'].split()

# Enable Debug and Log
ixiahlt.ixiatcl._eval("set ::ixia::debug 3")
ixiahlt.ixiatcl._eval("set ::ixia::debug_file_name ./ixnetwork_hlt_log.txt")

#result = ixiahlt.interface_config( # SY 03/18/26
for _ in range(3):
    try:
        result = ixiangpf.traffic_stats()
        if result['status'] != '1':
            ErrorHandler('traffic_stats', result)
        else:
            pprint(result)
    except Exception as e:
        pprint(e)
    time.sleep(3)
