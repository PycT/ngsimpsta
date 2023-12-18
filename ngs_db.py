import sqlite3
import ngs_config


class NgsDB:
    def __enter__(self):
        self.connection = sqlite3.connect(ngs_config.dbPath)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS {} (ID integer primary key, URL, IP_ADDRESS, YEAR, MONTH, DAY, HOUR, MINUTE, AGENT, AGENT_FULL)
        """.format(ngs_config.tableName))

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


    def recordExists(self, record):
        query = "SELECT * FROM {} WHERE {}".format(ngs_config.tableName, self.prepareSelectString(record))
        result = self.cursor.execute(query)
        if result.fetchone() != None:
            return True
        return False


    def addRecord(self, record):
        cols, vals = self.prepareInsertString(record)
        query = "INSERT INTO {} ({}) VALUES ({})".format(ngs_config.tableName, cols, vals)
        self.cursor.execute(query)
        self.connection.commit()
        return True


    def __exit__(self, exceptionType, exceptionValue, traceBack):
        self.connection.close()
        return True