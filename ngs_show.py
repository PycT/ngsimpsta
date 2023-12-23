#!/usr/bin/python

import ngs_config
from ngs_db import NgsDB

records = []

with NgsDB() as db:
    query = """
        SELECT `IP_ADDRESS`, `STATUS`,  `RELEASE_DATE`, `REASON`, `REASON_DETAILS`
        FROM {}
        WHERE `STATUS` IN ('{}', '{}')
        ORDER BY `STATUS`;
    """.format(
        db.jailTableName,
        db.STATUS_BANNED,
        db.STATUS_TO_BE_BANNED
    )

    records = db.runQuery(query)

with open(ngs_config.infoFilePath, "w") as info:
    for record in records:
        info.write("{}, {}, until {}, reason: {}, {}\n".format(
            *record
        ))

