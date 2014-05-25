#!/usr/bin/python2.6
#
#Copyright (c) 2014 Caspian Maclean
#
#sections:
# ======= imports =======
# ======= classes =======
# ======= interface ====== 
# ======= compute =======
# ======= print =======
# ======= test =======

# remaining issue - if doing a debit or query with a non-existent node, something gets
# messed up so future stuff won't work. Maybe just the invalid debit record is left
# in the debit list. whuffie_init() fixes this as expected.

# ======= imports =======
from pulp import *

# ======= classes =======

class Credit:
  def __init__(self, amount, by, subject, id):
    self.amount=amount
    self.by=by
    self.subject=subject
    self.id=id

class Debit:
  def __init__(self, amount, by, subject, id, previous_credits):
    self.amount=amount
    self.by=by
    self.subject=subject
    self.id=id
    self.previous_credits=previous_credits


# ======= interface ====== 
def whuffie_init():
  global credits
  global debits
  global flow_layers
  global enable_scaling
  global subjective_scaling
  credits=[]
  debits=[]
  flow_layers={}
  enable_scaling=1
  subjective_scaling=1

def credit(amount, by, subject):
  global credits
  new_id=len(credits)
  credits.append(Credit(amount=amount, by=by,subject=subject, id=new_id))

def debit(amount, by, subject):
  global credits
  global debits
  new_id=len(debits)
  previous_credits=len(credits)
  debits.append(Debit(amount=amount, by=by,subject=subject, id=new_id,previous_credits=previous_credits))

def query(by, subject):
  global debits
  query_store(by,subject)
  result = compute_result_2()
  debits=debits[0:-1] # deleting the query transaction
  return result

def disable_scaling():
  global enable_scaling
  enable_scaling=0

# ======= compute =======

def nodes_before(credit_count):
  nodes=set([])
  for credit in credits[0:credit_count]:
    nodes.add(credit.by)
    nodes.add(credit.subject)
  return nodes

def compute_scale_factor_std(credit_count, by_node):
  #version 1, with fudge factor "fudge"
  scale_results={}
  s={}
  balance={}
  fudge=1.0/10000
  nodes=nodes_before(credit_count)
  for node in nodes:
    s[node]=LpVariable("node scale:"+str(node),0,1000000) #arbitrary upper limit. Fix?
  for node in nodes:
    balance[node] = - fudge * s[node] + fudge #incomplete, will be modified by credits
  for credit in credits[0:credit_count]:
    scaled_amount = credit.amount * s[credit.by]
    balance[credit.by] = balance[credit.by] - scaled_amount
    balance[credit.subject] = balance[credit.subject] + scaled_amount
  if subjective_scaling:
    balance[by_node] = s[by_node] - 1
  #scale_problem=
  scale_problem=LpProblem("scale problem", LpMinimize) #minimisation not needed here
  for node in nodes:
    scale_problem += balance[node] == 0, "balance:"+str(node)
  scale_problem.solve()
  for node in nodes:
    scale_results[node]=s[node].varValue
  #print "scale done"
  return scale_results

def compute_scale_factor_unscaled(credit_count):
  s={}
  for node in nodes_before(credit_count):
    s[node]=1.0
  return s

def compute_scale_factor(credit_count, by_node):
  if enable_scaling:
    return compute_scale_factor_std(credit_count, by_node)
  return compute_scale_factor_unscaled(credit_count)

def create_flow_layer(layer_number):
  global credits
  global debits
  global flow_layers
  balance={}
  flow={}
  debit=debits[layer_number]
  credit_count=debit.previous_credits
  layer_credits=credits[0:credit_count]
  #print layer_credits
  layer_nodes=nodes_before(credit_count)
  s=compute_scale_factor(credit_count, debit.by)
  for node in layer_nodes:
    balance[node] = 0 #incomplete equation
  for credit in layer_credits:
    flow[credit.id]=LpVariable("flow("+str(layer_number)+","+str(credit.id)+") by:"+str(credit.by)+", subject"+ str(credit.subject),0,1000000) #arbitrary upper limit. Fix?
    scaled_amount = flow[credit.id] * s[credit.by]
    balance[credit.by] = balance[credit.by] - scaled_amount
    balance[credit.subject] = balance[credit.subject] + scaled_amount
  #put in debit flow
  scaled_amount = debit.amount * s[debit.by]
  balance[debit.by] = balance[debit.by] + scaled_amount
  balance[debit.subject] = balance[debit.subject] - scaled_amount
  eqs=[]
  for b in balance.values():
    eqs.append(b == 0)
  flow_layers[layer_number]={"flow":flow, "equations":eqs}
  
def create_capacity_limit_equations():
  global capacity_limits
  flow_remaining={}
  for credit in credits:
    #create equation_constraint flow_remaining[credit.id] = credit.amount #incomplete, will be modified by credits
    flow_remaining[credit.id] = credit.amount
    # it will be constrained > 0 as solving time.
  for flow_id, flow_layer in flow_layers.items():
    for credit in credits[0:debits[flow_id].previous_credits]:
      flow_remaining[credit.id] = flow_remaining[credit.id] - flow_layer["flow"][credit.id]
  eqs=[]
  for credit in credits:
    eqs.append(flow_remaining[credit.id] >= 0)
  capacity_limits=eqs
  return eqs

def query_store(by, subject):
  global q_result
  amount=LpVariable("query result about:"+str(subject)+" by:"+str(by),0,1000000) #arbitrary upper limit. Fix?
  debit(amount, by, subject)
  q_result=amount



def compute_result_from_equations():
  problem=LpProblem("computed credit",LpMaximize)
  problem+=q_result
  for eq in capacity_limits:
    problem += eq
  for flow_id, flow_layer in flow_layers.items():
    for eq in flow_layer["equations"]:
      problem += eq
  #print "calling solver from compute_result_from_equations"
  #print problem
  problem.solve()
  #print "result:",q_result.varValue

def compute_result_2():
  for i in range(len(debits)):
    create_flow_layer(i)
  create_capacity_limit_equations()
  compute_result_from_equations()
  return q_result.varValue

# ======= print =======
def print_hello():
  print "hello"

def print_credits():
  print credits
  for credit in credits:
    print "credit [", credit.id, "] :", credit.amount, "by:", credit.by,"to", credit.subject

def print_scale_factor_list(s):
  for k, v in s.items():
    print "s:",k, "=", v

# ======= test =======

def test1():
  print_hello()
  whuffie_init()
  credit(1.0,"A","B")
  #credit(1.0,"B","A")
  query("A","B")
  create_flow_layer(0)
  create_capacity_limit_equations()
  compute_result()
  scl=compute_scale_factor(len(credits))
  print scl
  print_scale_factor_list(scl)



# more testing

def test2_crash():
  print_hello()
  whuffie_init()
  credit(1.0,"A","B")
  credit(2.0,"B","C")
  credit(1.0,"C","A")
  debit(0.5,"C","A")
  credit(1.0,"B","D")
  credit(1.0,"D","A")
  debit(0.2,"D","A")
  query("A","B")
  print_credits()
  scl=compute_scale_factor(len(credits))
  print scl
  print_scale_factor_list(scl)
  print nodes_before(2)
  print nodes_before(3)
  create_flow_layer(0)
  create_flow_layer(1)
  create_flow_layer(2)
  print create_capacity_limit_equations()
  compute_result()

def test3():
  print_hello()
  whuffie_init()
  credit(1.0,"A","B")
  credit(1.0,"B","A")
  credit(0.1,"B","C")
  r=query("A","C")

  print "result of query:", r

  scl=compute_scale_factor(len(credits))
  print scl
  print_scale_factor_list(scl)

def test4():
  print_hello()
  whuffie_init()
  credit(1.0,"A","B")
  credit(2.0,"B","C")
  credit(1.0,"C","A")
  debit(0.5,"C","A")
  credit(1.0,"B","D")
  credit(1.0,"D","A")
  debit(0.2,"D","A")
  r=query("A","B")
  print "result of query:", r
  print_credits()
  scl=compute_scale_factor(len(credits))
  print scl
  print_scale_factor_list(scl)
  print nodes_before(2)
  print nodes_before(3)

def test_min_crash():
  whuffie_init()
  credit(amount=1.0, by="A", subject="B")
  debit(amount=0.0, by="A", subject="B")
  r=query(by="A",subject="B")
  print "result of query:", r
  #works now, after making sure all variable names used at once are different.
  #query creates a new variable with the same name each time - is this a problem?

#test_min_crash()
#test3()
def test_interactive():
  print_hello()
  print "Available functions:"
  print
  print "whuffie_init()"
  print "credit(amount, by, subject)"
  print "debit(amount, by, subject)"
  print "query(by, subject)"
  print
  print "Running whuffie_init() now, run it again later to reset things"
  print "Running debit or query to nonexistent nodes may corrupt lists,"
  print "use whuffie_init to fix"

  whuffie_init()

test_interactive()
