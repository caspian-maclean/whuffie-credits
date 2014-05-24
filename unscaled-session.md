

```
$ python2.6 -i whuffie-credits.py 
hello
Available functions:

whuffie_init()
credit(amount, by, subject)
debit(amount, by, subject)
query(by, subject)

Running whuffie_init() now, run it again later to reset things
Running debit or query to nonexistent nodes may corrupt lists,
use whuffie_init to fix
>>> disable_scaling()
>>> 
>>> credit(amount=3.5, by="you", subject="someone")
>>> query(by="you", subject="someone")
3.5
>>> 
>>> credit(amount=0.3, by="you", subject="someone")
>>> query(by="you", subject="someone")
3.7999999999999998
>>> 
>>> credit(amount=1000, by="spammer", subject="another")
>>> query(by="spammer", subject="another")
1000.0
>>> query(by="you", subject="another")
0.0
>>> 
>>> credit(amount=5, by="you", subject="second")
>>> credit(amount=5, by="second", subject="third")
>>> query(by="you", subject="third")
5.0
>>> 
>>> query(by="you", subject="second")
5.0
>>> 
>>> credit(amount=5, by="you",subject="B")
>>> credit(amount=3, by="B",subject="C")
>>> query(by="you", subject="C")
3.0
>>> 
>>> credit(amount=5, by="you",subject="D")
>>> credit(amount=7, by="D",subject="E")
>>> query(by="you", subject="E")
5.0
>>> 
```

This session was run using v0.1.0 of the whuffie-credits program