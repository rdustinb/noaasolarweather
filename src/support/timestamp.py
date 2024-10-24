from datetime import datetime
from dateutil import tz
from tzlocal import get_localzone

def getTimestamp():
    myLocalTimezone = get_localzone()
    myTimestamp = datetime.now(myLocalTimezone).strftime("%H:%M:%S %Z %Y-%m-%d")
    return myTimestamp

def convertTimestamps(theseTimestamps):
    newTimestamps = list()
    for thisTimestamp in theseTimestamps:
        newTimestamps.append(str(datetime.fromisoformat(thisTimestamp).astimezone(get_localzone())))
    return newTimestamps
