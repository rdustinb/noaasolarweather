from datetime import datetime
from tzlocal import get_localzone

def getTimestamp():
    myLocalTimezone = get_localzone()
    myTimestamp = datetime.now(myLocalTimezone).strftime("%H:%M:%S %Z %Y-%m-%d")
    return myTimestamp
