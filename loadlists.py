#Initial creation of lists from files
import pickledb


def main() :
  db = pickledb.load('stocks.fs',True)  
  lists = open('lists.txt','r')
  text = lists.read()
  tlist = text.split()
  for s in tlist :
    try :
      db.lrem(s[:-4])
    except KeyError :
      print('Tried removing non-existent list '+ s[:-4])

    #s[:-4] is the filename without the extension  
    db.lcreate(s[:-4])
    stockcodes = open(s,'r')
    stext = stockcodes.read()
    slist = stext.split()
    for t in slist :
      db.ladd(s[:-4], t)
  
  db.dump()
  return








if __name__ == '__main__':
  main()
