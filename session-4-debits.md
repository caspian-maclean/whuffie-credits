# Session log - Debits

If a favour is repaid, the whuffie can be cancelled with the debit function. Sometimes this can help prevent the same favour being repaid over and over again, totalling an unfair amount of repayment. Debiting has drawbacks, so you wouldn't always want to do it, or you might only debit a small amount.

Direct example:

	>>> whuffie_init()
	>>> credit(10,"you","them")
	>>> query("you","them")
	10.0
	>>> debit(10,"you","them")
	>>> query("you","them")
	-0.0

You could have just remembered that you'd repaid "them" though.

Indirect example, cancelling the whuffie from you shared by X and Y. First give the whuffie:

	>>> credit(10,"you","X")
	>>> credit(10,"X","Y")
	>>> query("you","Y")
	10.0
	>>> query("you","X")
	10.0
	>>> query("you","X")
	10.0
	>>> 

Then cancel it with a debit:

	>>> debit(10,"you","Y")
	>>> query("you","Y")
	-0.0
	>>> query("you","X")
	-0.0

It also cancelled Y's whuffie from X

	>>> query("X","Y")
	-0.0
	>>> 

Otherwise both "you" and "X" might repay "Y". In this example it might not be so bad, but in a long chain of you, A,B,C,D,E,F...Y it could be more unfair than people would tolerate.

Partial cancellation example

	>>> credit(10,"you","A")
	>>> query("you","A")
	10.0
	>>> debit(2,"you","A")
	>>> query("you","A")
	8.0
	>>> 

The next scenario's easier to show with scaling turned off. Also it has a lot of people so we'll reset the system first:

	>>> whuffie_init()
	>>> disable_scaling()
	>>> 

M helps a lot of people

	>>> credit(1,"A","M")
	>>> credit(1,"B","M")
	>>> credit(1,"C","M")
	>>> credit(1,"D","M")
	>>> credit(1,"E","M")

and is helped by a lot of people


	>>> credit(1,"M","V")
	>>> credit(1,"M","W")
	>>> credit(1,"M","X")
	>>> credit(1,"M","Y")
	>>> credit(1,"M","Z")

All the people who helped M now have credit with people helped by M, e.g.

	>>> query("A","V")
	1.0
	>>> query("A","Z")
	1.0
	>>> query("C","Z")
	1.0
	>>> 

"A" might help Z an amount they thought proportionate, then B,C,D,E might also do so, giving a total of 5 times as much help as they thought proportionate, and not having helped V,W,X, or Y at all.

So to solve this, "A" and "Z" agree to a debit when A repays Z

	>>> debit(1,"A","Z")
	>>> 

In this case it fully cancelled all credit from A, and all credit to Z. There is some other credit that is not cancelled.

	>>> query("A","V")
	-0.0
	>>> query("A","Z")
	0.0
	>>> query("C","Z")
	0.0
	>>> query("C","V")
	1.0
	>>> 

If you'd wanted to only partially cancel it, that's an option too, e.g. if B then helps Y

	>>> debit(0.3,"B","Y")
	>>> query("B","V")
	0.69999999999999996
	>>> query("B","Y")
	0.69999999999999996
	>>> query("C","Y")
	0.69999999999999996
	>>> query("C","V")
	1.0
	>>> 

Finally, one of the drawbacks. Where there haven't been any debits, the system allows more opportunity of indirect payback. e.g. if E helps V and gets whuffie for it, then E has whuffie from everyone who had given whuffie to V previously.

	>>> query("D","E")
	0.0
	>>> query("M","E")
	-0.0
	>>> query("V","E")
	-0.0
	>>> credit(1,"V","E")
	>>> query("D","E")
	1.0
	>>> query("M","E")
	1.0
	>>> query("V","E")
	1.0
	>>> 

Any of them might then repay E.

But if Z gives whuffie to A for help received, since all Z's whuffie from others was cancelled, there's only direct whuffie to repay A.

	>>> credit(1,"Z","A")
	>>> query("D","A")
	0.0
	>>> query("M","A")
	0.0
	>>> query("Z","A")
	1.0
	>>> 

It's not so bad if the whuffie was only partially cancelled, as in the case of B and Y, but there's still a reduction of indirect whuffie available.

	>>> credit(1,"Y","B")
	>>> query("D","B")
	0.69999999999999996
	>>> query("M","B")
	0.69999999999999996
	>>> query("Y","B")
	1.0
	>>> 

This session was run using v0.2.0 of the whuffie-credits program.

