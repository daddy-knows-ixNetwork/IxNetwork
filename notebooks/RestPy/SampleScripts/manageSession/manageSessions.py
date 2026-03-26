"""
manageSessions.py

   Connect to a Linux API server
      - View or delete open sessions

Supports IxNetwork API servers:
   - Windows, Windows Connection Mgr and Linux

Requirements
   - IxNetwork 8.50
   - Python 2.7 and 3+
   - pip install requests
   - pip install -U --no-cache-dir ixnetwork_restpy

Script development API doc:
   - The doc is located in your Python installation site-packages/ixnetwork_restpy/docs/index.html
   - On a web browser:
         - If installed in Windows: enter: file://c:/<path_to_ixnetwork_restpy>/docs/index.html
         - If installed in Linux: enter: file:///<path_to_ixnetwork_restpy>/docs/index.html
"""

import os, sys
# Import the RestPy module
from ixnetwork_restpy.testplatform.testplatform import TestPlatform

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
config=load_config('ixnetwork_config.yaml')

osPlatform = 'linux'

if len(sys.argv) > 1:
    # Command line input: windows, windowsConnectionMgr or linux
    osPlatform = sys.argv[1]

# Change API server values to use your setup
if osPlatform == 'windowsConnectionMgr':
    platform = 'windows'
    apiServerIp = config['session']['IpAddress']
    apiServerPort = 11009

# Change API server values to use your setup
if osPlatform == 'linux':
    platform = 'linux'
    apiServerIp = config['session']['IpAddress']
    apiServerPort = 443
    username = config['session']['UserName']
    password = config['session']['Password']

try:
    testPlatform = TestPlatform(apiServerIp, rest_port=apiServerPort, platform=platform)

    # Display debug loggings
    testPlatform.Trace = 'request_response'

    # authenticate with username and password
    testPlatform.Authenticate(config['session']['UserName'],config['session']['Password'])

    # Show all open sessions
    sessions = testPlatform.Sessions.find()
    if sessions:
        for session in sessions:
            print(session)
    else:
        print("No sessions", sessions)

    # Delete a particular session ID
    #testPlatform.Sessions.find(Id=11).remove()

    #testPlatform.Sessions.find(Id=1).remove()

except Exception as errMsg:
    print('\nrestPy.Exception:', errMsg)
