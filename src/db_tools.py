import sqlite3
#  con.set_trace_callback(print)

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

class Creator:
  def __init__(self, file_name:str):
    self._tables = tables(
      file_name
    )
    self._con = sqlite3.connect(
      file_name
    )
    self._cur = self._con.cursor()
  def create(self, sql, table:list[str]):
    if table[0] in self._tables:
      return
    self._cur.execute(
      sql.format(*table)
    )
  def createNamed(self, table:str):
    self.create(
      """
        CREATE TABLE {0} ( 
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL UNIQUE
        )
      """,
      [table]
    )
  def close(self):
      self._con.close()

def execute(
  values_:tuple,
  sql_:str,
  table_:list[str],
  file_:str

):
  con = sqlite3.connect(
    file_
  )
  cur = con.cursor()
  cur.execute(
    sql_.format(*table_),
    values_
  )
  con.commit()
  con.close()

def lastWord(
  values_:tuple,
  sql_:str,
  table_:list[str],
  file_:str
)->int:
  con = sqlite3.connect(
    file_
  )
  cur = con.cursor()
  cur.execute(
    sql_.format(*table_),
    values_
  )
  out = cur.lastrowid
  con.commit()
  con.close()
  return out


  
def fetchAll(
  values_:tuple,
  sql_:str,
  table_:list[str],
  file_:str
):
  con = sqlite3.connect(
    file_
  )
  cur = con.cursor()
  cur.execute(
    sql_.format(*table_),
    values_
  )
  data = cur.fetchall()
  con.close()
  return data

def fetchByString(
  string_:str,
  sql_:str,
  table_:list[str],
  file_:str
):
  con = sqlite3.connect(
    file_
  )
  cur = con.cursor()
  cur.execute(
    sql_.format(*table_),
    (string_,)
  )
  data = cur.fetchall()
  con.close()
  return data

def fetchById(
  id_:int,
  sql_:str,
  table_:list[str],
  file_:str
):
  con = sqlite3.connect(
    file_
  )
  cur = con.cursor()
  cur.execute(
    sql_.format(*table_),
    (id_,)
  )
  data = cur.fetchall()
  con.close()
  return data


def getById(
  id_:int,
  table_:str,
  file_:str
):
   return fetchById(
     id_,
     """
       SELECT * FROM 
         {0} 
       WHERE 
        id = ?
     """, 
     [table],
     file_
   )

