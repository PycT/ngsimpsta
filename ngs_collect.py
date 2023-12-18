#!python

from datetime import datetime
import ngs_config
from ngs_db import NgsDB

badIPs = []

try:
    with open(ngs_config.badIPsFileName, "r") as badIPsFile:
            for line in badIPsFile:
                badIPs.append(line.split(" ")[0])
except:
    with open(ngs_config.badIPsFileName, "w") as badIPsFile:
        pass

with NgsDB() as db:
    with open(ngs_config.path, "r") as logfile:
        for line in logfile:
            record = {}
            info = line.split(" ")
            
            if len(info) < 12:
                if info[0] not in badIPs:
                    badIPs.append(info[0])
                    with open(ngs_config.badIPsFileName, "a") as badIPsFile:
                        badIPsFile.write(line)
            else:
                timeInfo = datetime.strptime(info[3][1:],"%d/%b/%Y:%H:%M:%S")
                record["URL"] = info[6]
                record["IP_ADDRESS"] = info[0]
                record["YEAR"] = timeInfo.year
                record["MONTH"] = timeInfo.month
                record["DAY"] = timeInfo.day
                record["HOUR"] = timeInfo.hour
                record["MINUTE"] = timeInfo.minute
                record["AGENT"] = info[11][1:].replace("\"","")
                if not db.recordExists(record):
                    record["AGENT_FULL"] = " ".join(info[11:])[1:-2]
                    db.addRecord(record)

