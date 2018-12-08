import sys
import pickledb



def main() :
  db = pickledb.load('stock.fs', True)
  args = sys.argv[1:]

  if not args :
    for k in db.getall() :
      ##Added test so that the dictionaries of individual stocks and values does not print.  
      if not 'stocks' in k:
        print(k[:-10] + ' ' + k[-10:] +  ' ' + str(db.get(k)))
  else :
      for index in args :
        for k in db.getall() :
          if k[:-10] == index :
            print(k[:-10] + ' ' + k[-10:] + ' ' + db.get(k))
      

  db.dump()  

if __name__ == '__main__':
  main()