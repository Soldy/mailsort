import sqlite3
import mailsort.db_tools as tools
import mailsort.db_conf as conf


tr = tools.Transitor(conf.file_address)

def lookByName(name_:str, table_:str ):
   return tools.lookByName(
     name_,
     table_,
     conf.file_address
   )

def addWithName(
  name_:str,
  table_:list[str]
)->int:
  return tools.addWithName(
    name_,
    table_,
    conf.file_address
  )

def lookDomainTop(name_: str):
   return tr.lookByName(
     name_,
     conf.table_domain_top
   )

def addDomainTop(name_: str)->int:
   data = lookDomainTop(name_)
   if len(data) > 0:
     return data[0][0]
   return tr.addWithName(
     name_,
     conf.table_domain_top
   )

def lookDomainSecond(name_: str):
   return tr.lookByName(
     name_,
     conf.table_domain_second
   )

def addDomainSecond(name_: str)->int:
   data = lookDomainSecond(name_)
   if len(data) > 0:
     return data[0][0]
   return tr.addWithName(
     name_,
     conf.table_domain_second
   )

def lookDomainSub(name_: str):
   return tr.lookByName(
     name_,
     conf.table_domain_sub
   )

def addDomainSub(name_: str)->int:
   data = lookDomainSub(name_)
   if len(data) > 0:
     return data[0][0]
   return tr.addWithName(
     name_,
     conf.table_domain_sub
   )

def lookAlias(name_: str):
   return tr.lookByName(
     name_,
     conf.table_alias
   )

def addAlias(name_: str)->int:
   data = lookAlias(name_)
   if len(data) > 0:
     return data[0][0]
   return tr.addWithName(
     name_,
     conf.table_alias
   )

def lookDomain(top_: int, second_:int, sub_:int):
  return tr.fetchAll(
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
    ]
  )

def addDomain(top_: int, second_:int, sub_:int)->int:
  data = lookDomain(top_, second_, sub_)
  if len(data) > 0:
     return data[0][0]
  return tr.lastWord(
    (top_,second_,sub_),
    """
      INSERT INTO domain
        (top, second, sub)
      VALUES (?, ?, ?);
    """,
    [
      conf.table_domain
    ]
  )

def getDomain(id_:int):
  return tr.fetchById(
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
    ]
  )

def lookEmail(alias_: int, domain_:int)->int:
  return tr.fetchAll(
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
    ]
  )

def addEmail(alias_: int, domain_:int)->int:
  data = lookEmail(alias_, domain_)
  if len(data) > 0:
     return data[0][0]
  return tr.lastWord(
    (domain_, alias_),
    """
      INSERT INTO {0}
        (domain, alias)
      VALUES (?, ?);
    """,
    [
      conf.table_email_address
    ]
  )


def getEmail(id_:int):
  return tr.fetchById(
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
    ]
  )

def lookNamePart(name_: str):
   return tr.lookByName(
     name_,
     conf.table_name_part
   )

def addNamePart(name_: str)->int:
   data = lookNamePart(name_)
   if len(data) > 0:
     return data[0][0]
   return tr.addWithName(
     name_,
     conf.table_name_part
   )

def addName()->int:
  return tr.lastWord(
    (),
    """
      INSERT INTO {0}
      (id) VALUES (NULL);
    """,
    [
      conf.table_name
    ]
  )

def lookNameFull(name_:int, part_:int, serial_:int)->bool:
  return tr.fetchAll(
    (name_, part_, serial_),
    """
      SELECT * FROM {0}
      WHERE 
        name = ?
      AND 
        part = ?
      AND 
        serial = ?
    """,
    [
      conf.table_name_full
    ]
  )


def addNameFull(name_:int, part_:int, serial_:int):
  data = lookNameFull(name_, part_, serial_)
  if len(data) > 0:
     return
  tr.execute(
    (name_, part_, serial_),
    """
      INSERT INTO {0}
      (name,part,serial) VALUES (?,?,?);
    """,
    [
      conf.table_name_full
    ]
  )

def getNameFull(id_:int)->tuple:
  return tr.fetchById(
    id_,
    """
      SELECT
        {0}.id,
        GROUP_CONCAT({2}.name, " ") 
      FROM {0}
      LEFT JOIN {1}
      ON {1}.name = {0}.id
      LEFT JOIN {2}
      ON {1}.part = {2}.id
      WHERE {1}.name = ?
      ORDER BY {1}.serial ASC
    """, 
    [
      conf.table_name,
      conf.table_name_full,
      conf.table_name_part
    ]
  )

def lookAddress(name_:int, email_:int):
  return tr.fetchAll(
    (name_, email_),
    """
      SELECT * FROM {0}
      WHERE 
        name = ?
      AND 
        email = ?
    """,
    [
      conf.table_address
    ]
  )


def addAddress(name_:int, email_:int)->int:
  data = lookAddress(name_, email_)
  if len(data) > 0:
     return data[0][0]
  return tr.lastWord(
    (name_, email_),
    """
      INSERT INTO {0}
      (name,email) VALUES (?,?);
    """,
    [
      conf.table_address
    ]
  )

def getAddress(id_:int):
  return tr.fetchById(
    id_,
    """
      SELECT
        {0}.id,
        (
         SELECT
          GROUP_CONCAT({2}.name, " ") 
          FROM {1}
          LEFT JOIN {2}
          ON {1}.part = {2}.id
          WHERE {1}.name = {0}.name
          ORDER BY {1}.serial ASC
        ),
        {4}.name,
        {6}.name,
        {7}.name,
        {8}.name
      FROM {0}
      LEFT JOIN {3}
      ON {0}.email = {3}.id
      LEFT JOIN {4}
      ON {3}.alias = {4}.id
      LEFT JOIN {5}
      ON {3}.domain = {5}.id
      LEFT JOIN {6}
      ON {5}.sub = {6}.id
      LEFT JOIN {7}
      ON {5}.second = {7}.id
      LEFT JOIN {8}
      ON {5}.top = {8}.id
      WHERE {0}.id = ?
    """, 
    [
      conf.table_address,
      conf.table_name_full,
      conf.table_name_part,
      conf.table_email_address,
      conf.table_alias,
      conf.table_domain,
      conf.table_domain_sub,
      conf.table_domain_second,
      conf.table_domain_top,
    ]
  )
