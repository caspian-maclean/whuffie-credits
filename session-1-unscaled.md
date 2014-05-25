Here's a demonstration session introducing the whuffie credits system. First, starting the program:

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
```
We're turning off scaling for the initial examples, as it's simpler without that feature:

	>>> disable_scaling()

You can give someone whuffie, and see that they have it:

	>>> credit(amount=3.5, by="you", subject="someone")
	>>> query(by="you", subject="someone")
	3.5

Give them some more, and see their whuffie has increased by that much:

	>>> credit(amount=0.3, by="you", subject="someone")
	>>> query(by="you", subject="someone")
	3.7999999999999998

Whuffie is subjective, so a spammer giving another person whuffie only increases their whuffie from the spammer's point of view, not from yours:

	>>> credit(amount=1000, by="spammer", subject="another")
	>>> query(by="spammer", subject="another")
	1000.0
	>>> query(by="you", subject="another")
	0.0

Whuffie is transitive, so if you give someone some whuffie, and they give that to a third person, the third person has that amount of whuffie from your point of view:

	>>> credit(amount=5, by="you", subject="second")
	>>> credit(amount=5, by="second", subject="third")
	>>> query(by="you", subject="third")
	5.0

But it's shared rather than transferred, so the intermediate person also still has it after they gave it to the third person:

	>>> query(by="you", subject="second")
	5.0

Giving part of their whuffie shares that much:

	>>> credit(amount=5, by="you",subject="B")
	>>> credit(amount=3, by="B",subject="C")
	>>> query(by="you", subject="C")
	3.0

Giving more whuffie than they got from you shares what they have:

	>>> credit(amount=5, by="you",subject="D")
	>>> credit(amount=7, by="D",subject="E")
	>>> query(by="you", subject="E")
	5.0

This session was run using v0.1.0 of the whuffie-credits program.