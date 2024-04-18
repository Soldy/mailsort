import sqlite3
import mailsort.db_tools as tools
import mailsort.db_conf as conf


def create():
   creator = tools.Creator(conf.file_address)
   creator.createNamed(
     conf.table_domain_top
   )
   creator.createNamed(
     conf.table_domain_second
   )
   creator.createNamed(
     conf.table_domain_sub
   )
   creator.create(
     """
         CREATE TABLE {0}( 
           id INTEGER PRIMARY KEY,
           top INTEGER, 
           second INTEGER, 
           sub INTEGER,
           FOREIGN KEY (top)
             REFERENCES {1}(id),
           FOREIGN KEY (second)
             REFERENCES {2}(id),
           FOREIGN KEY (sub)
             REFERENCES {3}(id)
         )
     """,
     [
       conf.table_domain,
       conf.table_domain_top,
       conf.table_domain_second,
       conf.table_domain_sub
     ]
   )
   creator.createNamed(
     conf.table_alias
   )
   creator.create(
     """
       CREATE TABLE {0}( 
         id INTEGER PRIMARY KEY,
         domain INTEGER, 
         alias INTEGER, 
         FOREIGN KEY (domain)
           REFERENCES {1}(id),
         FOREIGN KEY (alias)
           REFERENCES {2}(id)
       )
     """,
     [
       conf.table_email_address,
       conf.table_domain,
       conf.table_alias
     ]
   )
   creator.createNamed(
     conf.table_name_part
   )
   creator.create(
     """
         CREATE TABLE {0}( 
           id INTEGER PRIMARY KEY
         )
     """,
     [conf.table_name]

   )
   creator.create(
     """
       CREATE TABLE name_full( 
         name INTEGER, 
         part INTEGER, 
         FOREIGN KEY (name)
           REFERENCES  name(id),
         FOREIGN KEY (part)
           REFERENCES name_part(id)
       )
     """,
     [
       conf.table_name,
       conf.table_name_full,
       conf.table_name_part
     ]
   )
   creator.create(
     """
         CREATE TABLE {0}( 
           name INTEGER, 
           email INTEGER, 
           FOREIGN KEY (name)
             REFERENCES  {1}(id),
           FOREIGN KEY (email)
             REFERENCES {2}(id)
         )
       """,
     [
       conf.table_address,
       conf.table_name,
       conf.table_email_address

     ]
   )
   creator.close()


   creator = tools.Creator(conf.file_history)
   creator.create(
     """
       CREATE TABLE {0}( 
         id INTEGER PRIMARY KEY,
         hash TEXT NOT NULL UNIQUE
       )
     """,
     [
       conf.table_filter
     ]
   )
   creator.create(
     """
       CREATE TABLE {0}( 
         id INTEGER PRIMARY KEY,
         uid TEXT NOT NULL UNIQUE
       )
     """,
     [
       conf.table_mail
     ]
   )
   creator.create(
     """
       CREATE TABLE {0}( 
         mail INTEGER, 
         filter INTEGER, 
         FOREIGN KEY (mail)
           REFERENCES  {1}(id),
         FOREIGN KEY (filter)
           REFERENCES {2}(id)
       )
     """,
     [
       conf.table_mail_to_filter,
       conf.table_mail,
       conf.table_filter
     ]
   )
   creator.close()

