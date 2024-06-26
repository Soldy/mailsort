import sqlite3
import mailsort.db_tools as tools
import mailsort.db_conf as conf


tr = tools.Transitor(conf.file_history)

def lookFilter(hash_: str):
   return tr.fetchByString(
     hash_,
     """
       SELECT * FROM 
         {0} 
       WHERE 
         hash = ?
     """, 
     [
       conf.table_filter
     ]
   )

def getFilter(id_:int):
   return tr.getById(
     id_,
     conf.table_filter
   )


def addFilter(hash_: str):
   data = lookFilter(hash_)
   if len(data) > 0:
      return data[0][0]
   tr.execute(
     (hash_,),
     """
       INSERT INTO {0}(hash) 
         VALUES(?)
     """, 
     [
       conf.table_filter,
     ]
   )
   data = lookFilter(hash_)
   return data[0][0]

def lookMail(uid_: str):
   return tr.fetchByString(
     uid_,
     """
       SELECT * FROM 
         {0} 
       WHERE 
         uid = ?
     """, 
     [
       conf.table_mail
     ]
   )

def getMail(id_:int):
   return tr.getById(
     id_,
     conf.table_mail
   )

def addMail(uid_: str)->int:
   data = lookMail(uid_)
   if len(data) > 0:
      return data[0][0]
   tr.execute(
     (uid_,),
     """
       INSERT INTO {0} 
         (uid)
       VALUES (?);
     """, 
     [
       conf.table_mail,
     ]
   )
   data = lookMail(uid_)
   return data[0][0]

def checkMailToFilter(mail_: str, filter_: str)->bool:
   data = tr.fetchAll(
     (mail_,filter_),
     """
       SELECT * FROM 
         mail_to_filter 
       WHERE 
         mail = ?
       AND
         filter = ?
     """, 
     [
       conf.table_mail_to_filter
     ]
   )
   if len(data) > 0:
       return True
   return False


def addMailToFilter(mail_: int, filter_: int):
   if checkMailToFilter(mail_, filter_):
       return
   tr.execute(
     (mail_,filter_),
     """
       INSERT INTO mail_to_filter
         (mail, filter) 
       VALUES
         (?,?)
     """, 
     [
       conf.table_mail_to_filter,
     ]
   )

def listByFilter(hash_:str):
   return tr.fetchByString(
     hash_,
     """
       SELECT 
         {0}.id,
         uid 
       FROM 
         {0} 
       LEFT JOIN {1}
       ON {0}.id = {1}.mail
       LEFT JOIN {2}
       ON {2}.id = {1}.filter
       WHERE 
         {2}.hash = ?
     """, 
     [
       conf.table_mail,
       conf.table_mail_to_filter,
       conf.table_filter
     ]
   )
