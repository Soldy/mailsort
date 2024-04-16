import sqlite3

def tables(file_:str)->list[str]:
   out = []
   con = sqlite3.connect(file_)
   cur = con.cursor()
   for i in cur.execute(
     """
       SELECT name FROM sqlite_schema 
         WHERE type = 'table'
         AND name NOT LIKE 'sqlite_%'
         ORDER BY 1;
     """
   ):
       out.append(i[0])
   con.close()
   return out
