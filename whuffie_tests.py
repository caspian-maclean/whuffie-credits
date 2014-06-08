from whuffie_credits import *
from random import random, randrange

def test_big(m=5,n=5):
  whuffie_init()
  for i in range(n-1):
    credit(amount = 10.0, by=i, subject=i+1)
  credit(amount = 10.0, by=n-1, subject=0)
  for i in range(m):
    a=randrange(n)
    b=randrange(n)
    print i, a,b
    debit(1,a,b)
    a=randrange(n)
    b=randrange(n)
    credit(1,a,b)
  a=randrange(n)
  b=randrange(n)
  print "last", a, b, query(a,b)
    
def test_big2(m=5,n=5):
  whuffie_init()
  for i in range(n-1):
    credit(amount = 10.0, by=i, subject=i+1)
  credit(amount = 10.0, by=n-1, subject=0)
  for i in range(m):
    a=randrange(n)
    b=randrange(n)
    whuffie=query(a,b)
    print i, a, b, whuffie
    debit(whuffie/2,a,b)
    a=randrange(n)
    b=randrange(n)
    credit(1,a,b)
  a=randrange(n)
  b=randrange(n)
  print "last", a,b ,query(a,b)
    
def test_big3(m,n,o):
  whuffie_init()
  for i in range(n-1):
    credit(amount = 10.0, by=i, subject=i+1)
  credit(amount = 10.0, by=n-1, subject=0)
  for i in range(m):
    a=randrange(n)
    b=randrange(n)
    whuffie=query(a,b)
    print i, a, b, whuffie
    debit(whuffie/2,a,b)
    for j in range(o):
      a=randrange(n)
      b=randrange(n)
      credit(1,a,b)
  a=randrange(n)
  b=randrange(n)
  print "last", a,b ,query(a,b)
    