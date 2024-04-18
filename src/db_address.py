import sqlite3
import mailsort.db_tools as tools
import mailsort.db_conf as conf

def lookByName(name_:str, table_:str ):
   return tools.fetchByString(
     name_,
     """
       SELECT * FROM 
         {0} 
       WHERE 
         name = ?
     """, 
     [
       table_
     ],
     conf.file_address
   )

def addWithName(
  name_:str,
  table_:list[str]
)->int:
  tools.lastWord(
    (name_,),
    """
      INSERT INTO {0}
        (name)
      VALUES (?);
    """,
    [
      table_
    ],
    conf.file_address
  )

def lookDomainTop(name_: str):
   return lookByName(
     name_,
     conf.table_domain_top
   )

def addDomainTop(name_: str)->int:
   data = lookDomainTop(name_)
   if len(data) > 0:
     return data[0][0]
   return addWithName(
     name_,
     conf.table_domain_top
   )

def lookDomainSecond(name_: str):
   return lookByName(
     name_,
     conf.table_domain_second
   )

def addDomainSecond(name_: str)->int:
   data = lookDomainSecond(name_)
   if len(data) > 0:
     return data[0][0]
   return addWithName(
     name_,
     conf.table_domain_second
   )

def lookDomainSub(name_: str):
   return lookByName(
     name_,
     conf.table_domain_sub
   )

def addDomainSub(name_: str)->int:
   data = lookDomainSub(name_)
   if len(data) > 0:
     return data[0][0]
   return addWithName(
     name_,
     conf.table_domain_sub
   )

def lookAlias(name_: str):
   return lookByName(
     name_,
     conf.table_alias
   )

def addAlias(name_: str)->int:
   data = lookAlias(name_)
   if len(data) > 0:
     return data[0][0]
   return addWithName(
     name_,
     conf.table_alias
   )

def lookDomain(top_: int, second_:int, sub_:int):
  return tools.fetchAll(
    (top_,second_,sub_),
    """
      SELECT * FROM 
        {0}
      WHERE 
        top = ?
      AND
        second = ?
      AND
        sub = ?
    """, 
    [
      conf.table_domain
    ],
    conf.file_address
  )

def addDomain(top_: int, second_:int, sub_:int)->int:
  data = lookDomain(top_, second_, sub_)
  if len(data) > 0:
     return data[0][0]
  return tools.lastWord(
    (top_,second_,sub_),
    """
      INSERT INTO domain
        (top, second, sub)
      VALUES (?, ?, ?);
    """,
    [
      conf.table_domain
    ],
    conf.file_address
  )

def lookEmail(alias_: int, domain_:int)->int:
  return tools.fetchAll(
    (domain_, alias_),
    """
      SELECT * FROM 
        {0}
      WHERE 
        domain = ?
      AND
        alias = ?
    """, 
    [
      conf.table_email_address
    ],
    conf.file_address
  )

def addEmail(alias_: int, domain_:int)->int:
  data = lookEmail(alias_, domain_)
  if len(data) > 0:
     return data[0][0]
  return tools.lastWord(
    (domain_, alias_),
    """
      INSERT INTO {0}
        (domain, alias)
      VALUES (?, ?);
    """,
    [
      conf.table_email_address
    ],
    conf.file_address
  )

def getDomain(id_:int):
  return tools.fetchById(
    id_,
    """
      SELECT 
        {0}.id,
        {1}.name,
        {2}.name,
        {3}.name 
      FROM {0}
      LEFT JOIN {1}
      ON {0}.sub = {1}.id
      LEFT JOIN {2}
      ON {0}.second = {2}.id
      LEFT JOIN {3}
      ON {0}.top = {3}.id
      WHERE 
        {0}.id = ?
    """, 
    [
      conf.table_domain,
      conf.table_domain_sub,
      conf.table_domain_second,
      conf.table_domain_top,
    ],
    conf.file_address
  )

def getEmail(id_:int):
  return tools.fetchById(
    id_,
    """
      SELECT 
        {0}.id,
        {1}.name,
        {3}.name,
        {4}.name,
        {5}.name
      FROM {0}
      LEFT JOIN {1}
      ON {0}.alias = {1}.id
      LEFT JOIN {2}
      ON {0}.domain = {2}.id
      LEFT JOIN {3}
      ON {2}.sub = {3}.id
      LEFT JOIN {4}
      ON {2}.second = {4}.id
      LEFT JOIN {5}
      ON {2}.top = {5}.id
      WHERE 
        {0}.id = ?
    """, 
    [
      conf.table_email_address,
      conf.table_alias,
      conf.table_domain,
      conf.table_domain_sub,
      conf.table_domain_second,
      conf.table_domain_top,
    ],
    conf.file_address
  )

def lookNamePart(name_: str):
   return lookByName(
     name_,
     conf.table_name_part
   )

def addNamePart(name_: str)->int:
   data = lookNamePart(name_)
   if len(data) > 0:
     return data[0][0]
   return addWithName(
     name_,
     conf.table_name_part
   )

def addName()->int:
  return tools.lastWord(
    (),
    """
      INSERT INTO {0}
      (id) VALUES (NULL);
    """,
    [
      conf.table_name
    ],
    conf.file_address
  )

def lookNameFull(name_:int, part_:int)->bool:
  return tools.fetchAll(
    (name_, part_),
    """
      SELECT * FROM {0}
      WHERE 
        name = ?
      AND 
        part = ?
    """,
    [
      conf.table_name_full
    ],
    conf.file_address
  )


def addNameFull(name_:int, part_:int):
  data = lookNameFull(name_, part_)
  if len(data) > 0:
     return data[0][0]
  tools.execute(
    (name_, part_),
    """
      INSERT INTO {0}
      (name,part) VALUES (?,?);
    """,
    [
      conf.table_name_full
    ],
    conf.file_address
  )

def getNameFull(id_:int)->tuple:
  return tools.fetchById(
    id_,
    """
      SELECT 
        {0}.id,
        {2}.name
      FROM {0}
      LEFT JOIN {1}
      ON {0}.id = {1}.name
      LEFT JOIN {2}
      ON {1}.part = {2}.id
      WHERE 
        {0}.id = ?
    """, 
    [
      conf.table_name,
      conf.table_name_full,
      conf.table_name_part
    ],
    conf.file_address
  )
