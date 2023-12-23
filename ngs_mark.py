#!/usr/bin/python

from datetime import datetime, timedelta
from ngs_db import NgsDB
import ngs_config


now = datetime.now()

scanTimeBorder = now - timedelta(days=ngs_config.daysToLookBack)

releaseDate4Frequency = now + timedelta(days=ngs_config.frequencyBanDays)

releaseDate4SuspiciousUrl = now + timedelta(days=ngs_config.suspiciousURLsBanDays)

bigBanTime = now + timedelta(days=10000)


def isURLSuspicious(url):
    if url == "/":
        return False
    
    for prefix in ngs_config.allowedURLs:
        if url.startswith(prefix):
            return False
        
    return True


def markBadIPs():
    global banRecords, scanTimeBorder, releaseDate4Frequency, releaseDate4SuspiciousUrl

    with NgsDB() as db:
        
        frequencyPerMinBanQuery = """
        SELECT * FROM
            (SELECT `IP_ADDRESS`, COUNT(ID) as `FREQUENCY` FROM {}
                WHERE `DATE` >= '{}'
                GROUP BY `IP_ADDRESS`, `YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`
            )
            WHERE `FREQUENCY` > {};
        """.format(
                NgsDB.statsTableName,
                scanTimeBorder,
                ngs_config.allowedFrequencyPerMinute
            )


        selectUrlsQuery = """
            SELECT `IP_ADDRESS`, `URL` FROM {}
                WHERE `DATE` >= '{}'
        """.format(
                NgsDB.statsTableName,
                scanTimeBorder
            )

        frequencyFelons = db.runQuery(frequencyPerMinBanQuery)
        for felon in frequencyFelons:
            felonRecord = {}
            felonRecord["IP_ADDRESS"] = felon[0]
            felonRecord["STATUS"] = db.STATUS_TO_BE_BANNED
            if not db.recordExists(felonRecord, db.jailTableName):
                felonRecord["REASON"] = db.REASON_FREQUENCY
                felonRecord["REASON_DETAILS"] = "{}/min".format(felon[1])
                felonRecord["RELEASE_DATE"] = releaseDate4Frequency
                db.addRecord(felonRecord, db.jailTableName)

        if ngs_config.ban4SuspiciousURLs:
            urlsData = db.runQuery(selectUrlsQuery)
            urlTrespassers = {}
            for urlRecord in urlsData:
                url = urlRecord[1]
                ip = urlRecord[0]
                if isURLSuspicious(url):
                    if not ip in urlTrespassers:
                        urlTrespassers[ip] = {}
                        urlTrespassers[ip]["REASON_DETAILS"] = url
                        urlTrespassers[ip]["count"] = 1
                    else:
                        urlTrespassers[ip]["REASON_DETAILS"] += "; {}".format(url)
                        urlTrespassers[ip]["count"] += 1
                        if urlTrespassers[ip]["count"] > ngs_config.suspiciousURLsTolerance:
                            felonRecord = {}
                            felonRecord["IP_ADDRESS"] = ip
                            felonRecord["STATUS"] = db.STATUS_TO_BE_BANNED
                            if not db.recordExists(felonRecord, db.jailTableName):
                                felonRecord["REASON"] = db.REASON_WRONG_URLS
                                felonRecord["REASON_DETAILS"] = urlTrespassers[ip]["REASON_DETAILS"]
                                felonRecord["RELEASE_DATE"] = releaseDate4SuspiciousUrl
                                print("Adding record: {}".format(felonRecord))
                                db.addRecord(felonRecord, db.jailTableName) 


def processFelons():
    global bigBanTime, now

    with NgsDB() as db:
        countFrequencyFelonsQuery = """
            SELECT `IP_ADDRESS` FROM
                (SELECT `IP_ADDRESS`, COUNT(IP_ADDRESS) as `VIOLATIONS_COUNT`
                FROM jail 
                WHERE REASON = '{}'
                GROUP BY `IP_ADDRESS`)
            WHERE `VIOLATIONS_COUNT` > {}
        """.format(
            db.REASON_FREQUENCY,
            ngs_config.frequencyViolationsMaxTries
        )

        countUrlsFelonsQuery = """
            SELECT `IP_ADDRESS` FROM
                (SELECT `IP_ADDRESS`, COUNT(IP_ADDRESS) as `VIOLATIONS_COUNT`
                FROM jail 
                WHERE REASON = '{}'
                GROUP BY `IP_ADDRESS`)
            WHERE `VIOLATIONS_COUNT` > {}
        """.format(
            db.REASON_WRONG_URLS,
            ngs_config.suspiciousURLViolationsMaxTries
        )

        ipsInString = ""

        frequencyFelons = db.runQuery(countFrequencyFelonsQuery)
        urlFelons = db.runQuery(countUrlsFelonsQuery)
        for felon in (frequencyFelons + urlFelons):
            ipsInString += "'{}', ".format(felon[0])

        if len(ipsInString) > 0:

            bigBanQuery = """
                UPDATE {}
                SET `RELEASE_DATE` = '{}'
                WHERE `STATUS` IN ('{}', '{}') AND `IP_ADDRESS` IN ({});
            """.format(
                db.jailTableName,
                bigBanTime,
                db.STATUS_TO_BE_BANNED,
                db.STATUS_BANNED,
                ipsInString[:-2]
            )

            db.runQuery(bigBanQuery)
        

        releaseQuery = """
                UPDATE {}
                SET `STATUS` = '{}'
                WHERE `STATUS` IN ('{}', '{}') AND `RELEASE_DATE` < '{}';
            """.format(
                db.jailTableName,
                db.STATUS_TO_BE_RELEASED,
                db.STATUS_TO_BE_BANNED,
                db.STATUS_BANNED,
                now
            )

        db.runQuery(releaseQuery)


if __name__ == "__main__":
    markBadIPs()
    processFelons()
