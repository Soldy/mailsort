import sqlite3
import mailsort.db_tools


def lookDomainTop(name_: str):
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT * FROM 
         domain_top 
       WHERE 
         name = ?
     """, 
     (name_,)
   )
   data = cur.fetchall()
   con.close()
   return data

def addDomainTop(name_: str)->int:
   data = lookDomainTop(name_)
   if len(data) > 0:
      return data[0][0]
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       INSERT INTO domain_top
         (name)
       VALUES (?);
     """,
     (name_,)
   )
   con.commit()
   con.close()
   data = lookDomainTop(name_)
   return data[0][0]

def lookDomainSecond(name_: str):
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT * FROM 
         domain_second 
       WHERE 
         name = ?
     """, 
     (name_,)
   )
   data = cur.fetchall()
   con.close()
   return data

def addDomainSecond(name_: str)->int:
   data = lookDomainSecond(name_)
   if len(data) > 0:
      return data[0][0]
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       INSERT INTO domain_second
         (name)
       VALUES (?);
     """,
     (name_,)
   )
   con.commit()
   con.close()
   data = lookDomainSecond(name_)
   return data[0][0]

def lookDomainSub(name_: str):
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT * FROM 
         domain_sub 
       WHERE 
         name = ?
     """, 
     (name_,)
   )
   data = cur.fetchall()
   con.close()
   return data

def addDomainSub(name_: str)->int:
   data = lookDomainSub(name_)
   if len(data) > 0:
      return data[0][0]
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       INSERT INTO domain_sub
         (name)
       VALUES (?);
     """,
     (name_,)
   )
   con.commit()
   con.close()
   data = lookDomainSub(name_)
   return data[0][0]

def lookAlias(name_: str):
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT * FROM 
         alias 
       WHERE 
         name = ?
     """, 
     (name_,)
   )
   data = cur.fetchall()
   con.close()
   return data

def addAlias(name_: str)->int:
   data = lookAlias(name_)
   if len(data) > 0:
      return data[0][0]
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       INSERT INTO alias
         (name)
       VALUES (?);
     """,
     (name_,)
   )
   con.commit()
   con.close()
   data = lookAlias(name_)
   return data[0][0]

def lookDomain(top_: int, second_:int, sub:int):
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT * FROM 
         domain 
       WHERE 
         top = ?
       AND
         second = ?
       AND
         sub = ?
     """, 
     (top_,second_,sub_)
   )
   data = cur.fetchall()
   con.close()
   return data

def addDomain(top_: int, second_:int, sub:int)->int:
   data = lookAlias(name_)
   if len(data) > 0:
      return data[0][0]
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       INSERT INTO domain
         (top, second, sub)
       VALUES (?, ?, ?);
     """,
     (top_,second_,sub_)
   )
   con.commit()
   con.close()
   data = lookAlias(name_)
   return data[0][0]

def lookEmail(top_: int, second_:int, sub:int):
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT * FROM 
         email_address 
       WHERE 
         domain = ?
       AND
         alias = ?
     """, 
     (domain, alias)
   )
   data = cur.fetchall()
   con.close()
   return data

def addEmail(top_: int, second_:int, sub:int)->int:
   data = lookAlias(name_)
   if len(data) > 0:
      return data[0][0]
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       INSERT INTO email_address
         (domain, alias)
       VALUES (?, ?);
     """,
     (domain, alias)
   )
   con.commit()
   con.close()
   data = lookAlias(name_)
   return data[0][0]

def getDomain(id_:int):
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT domain.id, domain_sub.name, domain_second.name, domain_top.name FROM 
         domain
       LEFT JOIN domain_sub
       ON domain.sub = domain_sub.id
       LEFT JOIN domain_second
       ON domain.second = domain_second.id
       LEFT JOIN domain_top
       ON domain.top = domain_top.id
       WHERE 
         domain.id = ?
     """, 
     (id_,)
   )
   data = cur.fetchall()
   con.close()
   return data

def getEmail(id_:int):
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   cur.execute(
     """
       SELECT 
         email_address.id,
         alias.name,
         domain_sub.name,
         domain_second.name,
         domain_top.name
       FROM email_address
       LEFT JOIN alias
       ON email_address.alias = alias.id
       LEFT JOIN domain
       ON email_address.domain = domain.id
       LEFT JOIN domain_sub
       ON domain.sub = domain_sub.id
       LEFT JOIN domain_second
       ON domain.second = domain_second.id
       LEFT JOIN domain_top
       ON domain.top = domain_top.id
       WHERE 
         email_address.id = ?
     """, 
     (id_,)
   )
   data = cur.fetchall()
   con.close()
   return data
