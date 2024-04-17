import sqlite3
import mailsort.db_tools


def lookFilter(hash_: str):
   con = sqlite3.connect(
     mailsort.db_conf._file_history
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT * FROM 
         filters 
       WHERE 
         hash = ?
     """, 
     (hash_,)
   )
   data = cur.fetchall()
   con.close()
   return data

def getFilter(id_:int):
   con = sqlite3.connect(
     mailsort.db_conf._file_history
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT * FROM 
         filters 
       WHERE 
         id = ?
     """, 
     (id_,)
   )
   data = cur.fetchall()
   con.close()
   return data[0]


def addFilter(hash_: str):
   data = lookFilter(hash_)
   if len(data) > 0:
      return data[0][0]
   con = sqlite3.connect(
     mailsort.db_conf._file_history
   )
   cur = con.cursor()
   cur.execute(
     """
       INSERT INTO filters(hash) 
         VALUES(?)
     """, 
     (hash_,)
   )
   con.commit()
   con.close()
   data = lookFilter(hash_)
   if len(data) > 0:
      return data[0][0]

def lookMail(uid_: str):
   con = sqlite3.connect(
     mailsort.db_conf._file_history
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT * FROM 
         mails 
       WHERE uid = ?
     """,
     (uid_,)
   )
   data = cur.fetchall()
   con.close()
   return data

def getMail(id_:int):
   con = sqlite3.connect(
     mailsort.db_conf._file_history
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT * FROM 
         mails 
       WHERE 
         id = ?
     """, 
     (id_,)
   )
   data = cur.fetchall()
   con.close()
   return data[0]

def addMail(uid_: str)->int:
   data = lookMail(uid_)
   if len(data) > 0:
      return data[0][0]
   con = sqlite3.connect(
     mailsort.db_conf._file_history
   )
   cur = con.cursor()
   cur.execute(
     """
       INSERT INTO mails 
         (uid)
       VALUES (?);
     """,
     (uid_,)
   )
   con.commit()
   con.close()
   data = lookMail(uid_)
   if len(data) > 0:
      return data[0][0]

def checkMailToFilter(mail_: str, filter_: str)->bool:
   con = sqlite3.connect(
     mailsort.db_conf._file_history
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT * FROM 
         mail_to_filter 
       WHERE 
         mail = ?
       AND
         filter = ?
     """, 
     (mail_,filter_)
   )
   data = cur.fetchall()
   con.close()
   if len(data) > 0:
       return True
   return False



def addMailToFilter(mail_: str, filter_: str):
   if checkMailToFilter(mail_, filter_):
       return

   con = sqlite3.connect(
     mailsort.db_conf._file_history
   )
   cur = con.cursor()
   cur.execute(
     """
       INSERT INTO mail_to_filter(mail, filter) 
         VALUES(?,?)
     """, 
     (mail_,filter_)
   )
   con.commit()
   con.close()

def listByFilter(hash_:str):
   con = sqlite3.connect(
     mailsort.db_conf._file_history
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT uid FROM 
         mails 
       LEFT JOIN mail_to_filter
       ON mails.id = mail_to_filter.mail
       LEFT JOIN filters
       ON filters.id = mail_to_filter.filter
       WHERE 
         filters.hash = ?
     """, 
     (hash_,)
   )
   data = cur.fetchall()
   con.close()
   return data[0]
