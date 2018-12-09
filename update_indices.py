#This program updates and stores the index values and the constituent stock values

import re
import requests
import pickledb
import datetime
import time

#Returns a stock price, given an ASX stock code
def getStockprice(code):
  url = 'https://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes=' + code
  r=requests.get(url,allow_redirects = True)
  open(code+'.html','wb').write(r.content)
  f = open(code + '.html','r')
  text = f.read()
  match = re.search(r'(<td class=\"last\">)(\d+\.\d+)',text)
  if match : 
    codeprice = float(match.group(2))
  else :
    codeprice = 0
  return codeprice

def calculateIndices() :
  datestr = str(datetime.date.today())
  db = pickledb.load('./data/stock.fs',True)
  f = open('./data/lists.txt','r')
  indfilelist = f.read().split()
  for indfile in indfilelist :
    print('processing... ' + indfile + '')
    dictname = indfile[:-4] + datestr
    db.dcreate(dictname)
    g = open('./data/' + indfile, 'r')
    codes = g.read().split()
    indextotal = 0
    for c in codes :
      codekey  = datestr + c
      price = getStockprice(c)
      db.dadd(dictname, (codekey, str(price)))
      indextotal += price
    db.set(indfile[:-11] + datestr, str(indextotal))
  db.dump()
  return



def main() :
  interval = 3600 #seconds in an hour
  nowtime = round(time.time()) - interval
  while True :
    while round(time.time()) < round(nowtime + interval) :
      for i in range(interval//5) :
        time.sleep(5)
    calculateIndices()
    print('finished processing at ' + str(datetime.datetime.now()))  
    print('sleeping. interrupt with ctrl-c')
    nowtime = round(time.time())




  
if __name__ == '__main__':
  main()