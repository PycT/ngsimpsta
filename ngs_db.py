import sqlite3
import ngs_config


class NgsDB:

    STATUS_TO_BE_BANNED = "to be banned"
    STATUS_TO_BE_RELEASED = "to be released"
    STATUS_BANNED = "banned"
    STATUS_RELEASED = "released"
    REASON_FREQUENCY = "Too frequent requests"
    REASON_WRONG_URLS = "Suspicious activity"
    statsTableName = "statistics"
    jailTableName = "jail"

    def __enter__(self):
        self.connection = sqlite3.connect(ngs_config.dbPath)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS {} (ID integer primary key, URL, IP_ADDRESS, DATE, YEAR, MONTH, DAY, HOUR, MINUTE, AGENT, AGENT_FULL)
        """.format(self.statsTableName))

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS {} (ID integer primary key, IP_ADDRESS, STATUS, RELEASE_DATE, REASON, REASON_DETAILS)
        """.format(self.jailTableName))

        return self


    def prepareSelectString(self, record):
        selectString = ""
        for key in record:
            selectString += "{}='{}' AND ".format(key, str(record[key]).replace("'", "`"))
        
        return selectString[:-5]


    def prepareInsertString(self, record):
        columnsString = ""
        valuesString = ""
        for key in record:
            columnsString += "{}, ".format(key)
            valuesString += "'{}', ".format(str(record[key]).replace("'", "`"))
        
        return columnsString[:-2], valuesString[:-2]


    def recordExists(self, record, table):
        query = "SELECT * FROM {} WHERE {}".format(table, self.prepareSelectString(record))
        result = self.cursor.execute(query)
        if result.fetchone() != None:
            return True
        return False


    def runQuery(self, query):
        result = self.cursor.execute(query)
        self.connection.commit()
        return result.fetchall()


    def addRecord(self, record, table):
        cols, vals = self.prepareInsertString(record)
        query = "INSERT INTO {} ({}) VALUES ({})".format(table, cols, vals)
        self.cursor.execute(query)
        self.connection.commit()
        return True


    def __exit__(self, exceptionType, exceptionValue, traceBack):
        self.connection.close()
        return True