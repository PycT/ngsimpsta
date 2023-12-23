#!/usr/bin/python

from datetime import datetime
import ngs_config
from ngs_db import NgsDB

with NgsDB() as db:
    with open(ngs_config.nginxLogPath, "r") as logfile:
        for line in logfile:
            record = {}
            info = line.split(" ")
            
            if len(info) < 12:
                info = info + ["", ""]

            timeInfo = datetime.strptime(info[3][1:],"%d/%b/%Y:%H:%M:%S")
            record["URL"] = info[6]
            record["IP_ADDRESS"] = info[0]
            record["DATE"] = timeInfo
            record["YEAR"] = timeInfo.year
            record["MONTH"] = "{:02d}".format(timeInfo.month)
            record["DAY"] = "{:02d}".format(timeInfo.day)
            record["HOUR"] = "{:02d}".format(timeInfo.hour)
            record["MINUTE"] = "{:02d}".format(timeInfo.minute)
            record["AGENT"] = info[11][1:].replace("\"","")
            if not db.recordExists(record, NgsDB.statsTableName):
                record["AGENT_FULL"] = " ".join(info[11:])[1:-2]
                db.addRecord(record, NgsDB.statsTableName)
