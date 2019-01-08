

import datetime
import dateutil
import data_access as da
import sys

def reformat(cdate) :
  cdate = str(cdate)
  cdate = cdate[:4] + cdate[5:7] + cdate[8:]
  return cdate



def main() :  

  tday = datetime.date.today()
  year = str(tday)[:4]
  pw = input('Password for database:')
  conn = da.getConnection(pw)
  try:
    #Get all trading days for this calendar year and last calendar year
    alldates = da.getAllTradeDatesToDate(conn,year)
    tradedates = []
    for td in alldates:
      tradedates.append(reformat(td['trade_date']))
    tradedates.sort()
    lastdate = tradedates[len(tradedates)-1]
    lastweek = tradedates[len(tradedates)-1-5]
    lastmonth = tradedates[len(tradedates)-1-20]
    lastyear = tradedates[len(tradedates)-1-250]

    #Get a list of the index_codes

    for icode in da.getIndexCodes(conn) :
      for scode in da.getIndexStockCodes(conn, icode['index_code'] ) :
        currentprice = []
        for price in da.getPriceByDate(conn, scode['stock_code'],lastdate) :
          currentprice.append(float(price['close']))

        wkprice = []
        for price in da.getPriceByDate(conn, scode['stock_code'], lastweek) :
          wkprice.append(price['close'])

        mthprice = []
        for price in da.getPriceByDate(conn,scode['stock_code'], lastmonth) :
          mthprice.append(price['close'])

        yrprice = []
        for price in da.getPriceByDate(conn,scode['stock_code'], lastyear) :
          yrprice.append(price['close'])
          print(scode['stock_code'],price)
        
        
        




    
    
   

   


  finally:
    conn.close()












if __name__ == '__main__' :
  main()