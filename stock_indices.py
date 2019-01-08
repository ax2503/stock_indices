
import data_access as da

def loadIndexes(conn) :
  with open('data/lists.txt','r') as fs :
    text = fs.read()
    for filename in text.split():
      with open('data/' + filename,'r') as indexfile:
        stockcodes = indexfile.read()
        for stockcode in stockcodes.split():
          da.replaceIndexRecord(conn, [filename[:-4], stockcode])

  return

def main() :
  pw = input('Password for MySql Database: ')
  conn = da.getConnection(pw)
  try:
    da.dropIndexTable(conn)
    da.createIndexTable(conn)
    loadIndexes(conn)
  finally:
      conn.close()

if __name__ == '__main__' :
    main()

