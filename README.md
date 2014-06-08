whuffie-credits
===============

System for keeping track of valuable contributions, inspired by Cory Doctorow's fictional whuffie

At the moment it's organised as a bunch of function calls that keep track of people's credit, e.g.

	>>> credit(12,"them", "you")
	>>> query("them","you")
	12.0

See the files session-* for examples to see how the system works when combining multiple credits and debits, and how it encourages repaying contributions.

To run the program, you need to get the PuLP library working (I found this took a bit of trial and error, and only
worked under python 2.6) and then it should run with python2.6 -i whuffie_credits.py
