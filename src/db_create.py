import sqlite3
import mailsort.db_tools
import mailsort.db_conf




def create():
   tables = mailsort.db_tools.tables(
     mailsort.db_conf._file_address
   )
   con = sqlite3.connect(
     mailsort.db_conf._file_address
   )
   cur = con.cursor()
   if 'domain_top' not in tables:
       cur.execute("""
         CREATE TABLE domain_top( 
           id INTEGER PRIMARY KEY,
           name TEXT NOT NULL UNIQUE
         )
       """)
   if 'domain_second' not in tables:
       cur.execute("""
         CREATE TABLE domain_second( 
           id INTEGER PRIMARY KEY,
           name TEXT NOT NULL UNIQUE
         )
       """)
   if 'domain_sub' not in tables:
       cur.execute("""
         CREATE TABLE domain_sub( 
           id INTEGER PRIMARY KEY,
           name TEXT NOT NULL UNIQUE
         )
       """)
   if 'domain' not in tables:
       cur.execute("""
         CREATE TABLE domain( 
           id INTEGER PRIMARY KEY,
           top INTEGER, 
           second INTEGER, 
           sub INTEGER,
           FOREIGN KEY (top)
             REFERENCES domain_top(id),
           FOREIGN KEY (second)
             REFERENCES domain_second(id),
           FOREIGN KEY (sub)
             REFERENCES domain_sub(id)
         )
       """)
   if 'alias' not in tables:
       cur.execute("""
         CREATE TABLE alias( 
           id INTEGER PRIMARY KEY,
           name TEXT NOT NULL UNIQUE
         )
       """)
   if 'email_address' not in tables:
       cur.execute("""
         CREATE TABLE email_address( 
           id INTEGER PRIMARY KEY,
           domain INTEGER, 
           alias INTEGER, 
           FOREIGN KEY (domain)
             REFERENCES domain(id),
           FOREIGN KEY (alias)
             REFERENCES alias(id)
         )
       """)
   if 'name_part' not in tables:
       cur.execute("""
         CREATE TABLE name_part( 
           id INTEGER PRIMARY KEY,
           name TEXT NOT NULL UNIQUE
         )
       """)
   if 'name' not in tables:
       cur.execute("""
         CREATE TABLE name( 
           id INTEGER PRIMARY KEY
         )
       """)
   if 'name_full' not in tables:
       cur.execute("""
         CREATE TABLE name_full( 
           name INTEGER, 
           part INTEGER, 
           FOREIGN KEY (name)
             REFERENCES  name(id),
           FOREIGN KEY (part)
             REFERENCES name_part(id)
         )
       """)
   con.close()
   tables = mailsort.db_tools.tables(
     mailsort.db_conf._file_history
   )
   con = sqlite3.connect(
     mailsort.db_conf._file_history
   )
   cur = con.cursor()
   if 'filters' not in tables:
       cur.execute("""
         CREATE TABLE filters( 
           id INTEGER PRIMARY KEY,
           hash TEXT NOT NULL UNIQUE
         )
       """)
   if 'mails' not in tables:
       cur.execute("""
         CREATE TABLE mails( 
           id INTEGER PRIMARY KEY,
           uid TEXT NOT NULL UNIQUE
         )
       """)
   if 'mail_to_filter' not in tables:
       cur.execute("""
         CREATE TABLE mail_to_filter( 
           mail INTEGER, 
           filter INTEGER, 
           FOREIGN KEY (mail)
             REFERENCES  mails(id),
           FOREIGN KEY (filter)
             REFERENCES filters(id)
         )
       """)
   con.close()

