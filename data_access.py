
import pymysql.cursors

def getConnection(pw) :
  connection=pymysql.connect(host='localhost',
               user='root',
               password=pw,
               db = 'stock_history',
               charset = 'utf8mb4',
               cursorclass=pymysql.cursors.DictCursor)
  return connection

def dropIndexTable(conn) :
  sql = 'DROP TABLE IF EXISTS stockindexes;'
  try:
    with conn.cursor() as cursor :
      cursor.execute(sql)
  except Exception as ex :
    print('Problem occurred dropping table')
    print(ex)
  return

def getAllTradeDatesToDate(conn,year):
  yeartable = 'year' +year
  lastyeartable = 'year' +str(int(year) - 1)

  sql = ('(SELECT DISTINCT trade_date ' +'FROM ' + lastyeartable + ' ' +
         'ORDER BY trade_date DESC) ' +
         'UNION ' +
         '(SELECT DISTINCT trade_date ' + 'FROM ' + yeartable + ' ' +
         'ORDER BY trade_date DESC);')
  try:
    with conn.cursor() as cursor :
      cursor.execute(sql)
  except Exception as ex :
    print('Problem retrieving list of all trade dates')
    print(ex)
  return cursor.fetchall()


def getIndexTotalsByDate(conn,tradedate):
  yeartable = 'year' + tradedate[:4]
  sql =('SELECT stockindexes.index_code as indexcode, SUM(' + yeartable + '.close) as total ' +
        'FROM ' + yeartable + ', stockindexes '+
        'WHERE ' + yeartable + '.stock_code = stockindexes.stock_code ' +
        'AND ' + yeartable + '.trade_date = ' + tradedate + ' ' +
        'GROUP BY stockindexes.index_code;')
  
  try:
    with conn.cursor() as cursor:
      cursor.execute(sql)
  except Exception as ex :
    print('Problem getting index totals by date')
    print(ex)
  return cursor.fetchall()

def getRecordCountByDate(conn,tradedate) :
  pass  


def createIndexTable(conn) :
  sql = ( 'CREATE TABLE IF NOT EXISTS stockindexes (index_code VARCHAR(30), stock_code VARCHAR(10));')
  try:
    with conn.cursor() as cursor:
      cursor.execute(sql)
  except Exception as ex:
    print('Problem ocurred creating stockindexes table')
    print(ex)
  return

def replaceIndexRecord(conn, entry) :
  sql = ('REPLACE INTO stockindexes (index_code, stock_code) VALUES (%s,%s);')
  try:
    with conn.cursor() as cursor:
      cursor.execute(sql, entry)
      conn.commit()
  except Exception as ex:
    print('Failed to add record for ' + entry[0] +' ' + entry[1])
    print(ex)
  return

def getPricesByIndexByDate(conn,indexcode,tradedate) :
  yeartable = 'year' + tradedate[:4]
  sql = ('SELECT close ' +
         'FROM ' + yeartable + ' ' +
         'WHERE trade_date = ' + tradedate + ' ' +
         'AND stock_code IN ' +
         '(SELECT stock_code FROM stockindexes ' + 
         'WHERE index_code = ' + '\'' + indexcode + '\');')

  try:
    with conn.cursor() as cursor :
      cursor.execute(sql)
  except Exception as ex :
    print('Problem occurred getting stock prices for ' + indexcode + ' ' + tradedate)
    print(ex)
  return cursor.fetchall()
#**************************************************************************************
def getPriceByDate(conn,stockcode,tdate) :
  year = tdate[:4]
  yeartable = 'year' + year
  lastyeartable = 'year' +str(int(year) - 1)
  sql=('SELECT trade_date, close ' + 
       'FROM ' + yeartable + ' '
       'WHERE trade_date <= ' + tdate + ' ' +
       'AND close > 0 ' +
       'AND stock_code = \'' + stockcode + '\' ' +
       'UNION ' + 
       '(SELECT trade_date, close ' + 
        'FROM ' + lastyeartable + ' ' +
        'WHERE trade_date <= ' + tdate + ' '+ 
        'AND close > 0 ' +
        'AND stock_code = \'' + stockcode + '\')' +
        'ORDER BY trade_date DESC LIMIT 1;')
  try:
    with conn.cursor() as cursor:
      cursor.execute(sql)
  except Exception as ex :
    print("Problem getting stock price by date")
    print(ex)
  return cursor.fetchall()

def getIndexCodes(conn) :
  sql = 'SELECT DISTINCT index_code FROM stockindexes;'
  try:
    with conn.cursor() as cursor :
      cursor.execute(sql)
  except Exception as ex :
    print("Problem getting Index Codes")
    print(ex)
  return cursor.fetchall()

def getIndexStockCodes(conn, indexcode) :
  sql = ('SELECT stock_code FROM stockindexes ' +
         'WHERE index_code = \'' + indexcode + '\';')
  try:
    with conn.cursor() as cursor:
      cursor.execute(sql)
  except Exception as ex :
    print('Problem getting stock codes for index ' + indexcode)
    print(ex)
  return cursor.fetchall()

#***************************************************************************
def tests() :
  print('starting tests')
  pw = input('Password for MySql database:')
  conn = getConnection(pw)
  try:
    print('dropping table stockindexes')
    proceed = input('Proceed? [YN]')
    if proceed.upper() == 'Y' :
      dropIndexTable(conn)
      print('table dropped')

    print('creating table stockindexes')
    proceed = input('Proceed? [YN]')
    if proceed.upper() == 'Y' :
      createIndexTable(conn)
      print('table created')

    print('adding test record')
    proceed = input('Proceed? [YN]')
    if proceed.upper() == 'Y' :
      replaceIndexRecord(conn, ['XXX','XXX'])
      print('record added')
    
  finally:
    conn.close()

def tests1():
  pw = input('Password for MySql database:')
  conn = getConnection(pw)
  try:
    for record in getIndexTotalsByDate(conn, '20181231'):
      print(record['total'])

    print('getting stock prices for agtech_stocks for 20180108')
    for record in getPricesByIndexByDate(conn, 'agtech_stocks', '20180108') :
      print(record['close'])
  finally:
    conn.close()

    return

  
if __name__ == '__main__' :
      tests1()