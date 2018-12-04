#Initial creation of lists from files
import pickledb


def main() :
  db = pickledb.load('stocks.fs',True)  
  lists = open('lists.txt','r')
  text = lists.read()
  tlist = text.split()
  for s in tlist :
    #db.lrem(s[:-4])
    print (s[:-4])  
    #stockcodes = open(s,'r')
    #stext = stockcodes.read()
    #slist = stext.split()







if __name__ == '__main__':
  main()
