Session 2 - scaling

Rather than have everyone have to measure out the whuffie they give on the same scale, each person can use their own and have the system automatically rescale.
The way the scaling works, the whuffie each person's given out is scaled to match the total they received, though with a few complications.
Example: you give someone 30 credits, they give out a total of 3, so those 3 credits are scaled up by a factor of 10

	>>> whuffie_init()
	>>> credit(30,"you","them")
	>>> credit(1,"them","A")
	>>> credit(2,"them","B")
	>>> query("you","A")
	9.9997000000000007
	>>> query("you","B")
	19.999400000000001
	>>> 

This shows a few of the complications: the credit given by node "you" was not scaled down to zero for a few reasons: a "fudge factor" prevents any scaling factor from going down as low as zero, and the node doing the query is not scaled at all (partly so "you" can read the result in your own scale). Also the results were not exact, mainly due to the fudge factor, but also due to rounding errors.

This session was run using v0.2.0 of the whuffie-credits program.

