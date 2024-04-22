#!/usr/bin/python3
import sys
import time
import pytest
import mailsort.tools as email
import mailsort.db_create
import mailsort.db_history
import mailsort.db_address

_tops = [ 'au', 'com', 'cx', 'de', 'diy', 'info', 'net', 'org' ]
_seconds = [ 'cnn', 'example', 'yt', 'github' ]
_subs = [ 'www', 'mail', 'mx' ]
_aliases = [ 'amy', 'kathy', 'keya', 'xiza' ]

_namepart_one = [ 'alen', 'amy', 'elizabeth', 'john', 'tracy' ]

_namepart_two = [  'cage', 'olsen', 'smith', 'wick' ]


def test_create():
  try:
    mailsort.db_create.create()
  except Error:
    pytest.fail(Error)

def test_already_created():
  try:
    mailsort.db_create.create()
  except Error:
    pytest.fail(Error)

def test_addfliter():
  for i in range(10):
    assert(
      mailsort.db_history.addFilter('test'+str(i))
    ) == i+1

def test_addmail():
  for i in range(10):
    assert(
      mailsort.db_history.addMail('test'+str(i))
    ) == i+1

def test_lookmail():
  for i in range(10):
    name = 'test'+str(i)
    assert(
      mailsort.db_history.lookMail(name)
    ) == [(i+1, name)]

def test_checkMailToFilter():
  for a in range(10):
    for b in range(10):
      assert(
        mailsort.db_history.checkMailToFilter(a,b)
      ) == False

def test_addMailToFilter():
  for a in range(10):
    for b in range(10):
      assert(
        mailsort.db_history.addMailToFilter(a,b)
      ) == None

def test_checkMailToFilter_after_create():
  for a in range(10):
    for b in range(10):
      assert(
        mailsort.db_history.checkMailToFilter(a,b)
      ) == True

def test_addDomainTop():
  global _tops
  for i in range(len(_tops)):
    assert(
      mailsort.db_address.addDomainTop(_tops[i])
    ) == i+1

def test_addDomainSecond():
  global _seconds
  for i in range(len(_seconds)):
    assert(
      mailsort.db_address.addDomainSecond(_seconds[i])
    ) == i+1

def test_addDomainSub():
  global _subs
  for i in range(len(_subs)):
    assert(
      mailsort.db_address.addDomainSub(_subs[i])
    ) == i+1

def test_addDomain():
  global _tops
  global _seconds
  global _subs
  for a in range(len(_tops)):
    for b in range(len(_seconds)):
      for c in range(len(_subs)):
        assert(
          mailsort.db_address.addDomain(a, b, c)
        ) == (a*len(_seconds)*len(_subs))+(b*len(_subs))+(c+1)

def test_addAlias():
  global _aliases
  for i in range(len(_aliases)):
    assert(
      mailsort.db_address.addAlias(_aliases[i])
    ) == i+1

def test_addNamePart_one():
  global _namepart_one
  for i in range(len(_namepart_one)):
    assert(
      mailsort.db_address.addNamePart(_namepart_one[i])
    ) == i+1

def test_addNamePart_two():
  global _namepart_one
  global _namepart_two
  for i in range(len(_namepart_two)):
    assert(
      mailsort.db_address.addNamePart(_namepart_two[i])
    ) == len(_namepart_one)+i+1

def test_addName():
  global _namepart_one
  global _namepart_two
  for a in range(len(_namepart_one)):
    for b in range(len(_namepart_two)):
      _id = mailsort.db_address.addName()
      mailsort.db_address.addNameFull(_id,a,1)
      mailsort.db_address.addNameFull(_id,b,2)
  