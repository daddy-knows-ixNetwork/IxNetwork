"""

"""

# Import the RestPy module
from ixnetwork_restpy import SessionAssistant

# For linux and connection_manager only. Set to True to leave the session alive for debugging.
debugMode = False
chassisIps = (
    '10.36.88.110',
    '10.36.88.51',
    '10.36.88.113'
)

for chassisIp in chassisIps:
    try:
        # LogLevel: none, info, warning, request, request_response, all
        session = SessionAssistant(
            IpAddress=chassisIp,
            RestPort=None,
            UserName='admin',
            Password='admin',
            SessionName=None,
            SessionId=None,
            ApiKey=None,
            ClearConfig=True,
            LogLevel='none',
            LogFilename='none')

        buildNumber = session.Ixnetwork.Globals.BuildNumber
        print(f"The build number for the chassis {chassisIp} is {buildNumber}.")

        if debugMode == False:
            # For Linux and Windows Connection Manager only
            session.Session.remove()

    except Exception as errMsg:
        print(errMsg)
        session.Session.remove()
