#!/usr/bin/python

import subprocess
from ngs_db import NgsDB

banCommand = ["ufw", "deny", "from", ""]
unbanCommand = ["ufw", "delete", "deny", "from", ""]


with NgsDB() as db:

    selectToBeBannedQuery = """
        SELECT `IP_ADDRESS` FROM {}
        WHERE `STATUS` = '{}'
    """.format(
        db.jailTableName,
        db.STATUS_TO_BE_BANNED
    )

    bannedStr = ""

    toBeBanned = db.runQuery(selectToBeBannedQuery)
    print(toBeBanned)
    for felon in toBeBanned:
        banCommand[3] = felon[0]
        subprocess.run(banCommand)
        bannedStr += "'{}', ".format(felon[0])

    if len(bannedStr) > 0:
        updateQuery = """
            UPDATE {}
            SET `STATUS` = '{}'
            WHERE `STATUS` = '{}' AND `IP_ADDRESS` IN ({});
        """.format(
            db.jailTableName,
            db.STATUS_BANNED,
            db.STATUS_TO_BE_BANNED,
            bannedStr[:-2]
        )

        db.runQuery(updateQuery)

    selectToBeReleasedQuery = """
        SELECT `IP_ADDRESS` FROM {}
        WHERE `STATUS` = '{}'
    """.format(
        db.jailTableName,
        db.STATUS_TO_BE_RELEASED
    )

    releasedStr = ""

    toBeReleased = db.runQuery(selectToBeReleasedQuery)
    for felon in toBeReleased:
        unbanCommand[4] = felon[0]
        subprocess.run(unbanCommand)
        releasedStr += "'{}', ".format(felon[0])

    if len(releasedStr) > 0:
        updateQuery = """
            UPDATE {}
            SET `STATUS` = '{}'
            WHERE `STATUS` = '{}' AND `IP_ADDRESS` IN ({});
        """.format(
            db.jailTableName,
            db.STATUS_RELEASED,
            db.STATUS_TO_BE_RELEASED,
            releasedStr[:-2]
        )

        db.runQuery(updateQuery)
