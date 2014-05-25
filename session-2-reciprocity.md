Session log - Reciprocity
This session shows how whuffie can encourage reciprocity, paying back help.

We're turning off scaling as before

	>>> whuffie_init()
	>>> disable_scaling()

You help someone, they appreciate that and the system keeps a record of it for them.

	>>> credit(12,"them", "you")

They see your whuffie's gone up, and can decide to do something for you in return.

	>>> query("them","you")
	12.0

If you like what they did, the system records that (when you tell it)

	>>> credit(11,"you","them")

So their whuffie has gone up.

	>>> query("you","them")
	11.0

You could then do something for them, and so on.

	>>> credit(13,"them", "you")
	>>> query("them","you")
	25.0
	>>> credit(14,"you","them")
	>>> query("you","them")
	25.0

That's a simple situation, the system hasn't been very useful yet. In the next example, you're paid back by a different person from the one you helped. First, you help a second person, and they give you whuffie for this.

	>>> credit(4,"second","you")

Next, the second person helps a third person, and gets whuffie from the third person.

	>>> credit(5,"third","second")

In this example, suppose the third person can't do anything really useful for the second person at the moment. So they see you now have whuffie, and help you.

	>>> query("third","you")
	4.0

Once you give them whuffie for this, it raises the second person's whuffie (according to you), encouraging you to continue the cycle by helping the second person again.

	>>> query("you","second")
	0.0
	>>> credit(3,"you","third")
	>>> query("you","second")
	3.0

So you help them and earn whuffie, and in the second cycle, your whuffie with the third person, who seems to have something useful for you, goes up to twice as much it was before

	>>> credit(4,"second","you")
	>>> query("third","you")
	5.0

It's already gone up a bit, but there's more this cycle.

	>>> credit(5,"third","second")
	>>> query("third","you")
	8.0
	>>> 

Your whuffie at the end of the cycle, encouraging more help from "third".


