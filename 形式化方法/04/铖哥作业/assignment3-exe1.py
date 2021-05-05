"""Z3 is an SMT solver.
In this lecture, we'll discuss
the basis usage of Z3 through some working example, the
primary goal is to introduce how to use Z3 to solve
the satisfiability problems we've discussed in the past
several lectures.
We must emphasize that Z3 is just one of the many such SMT
solvers, and by introducing Z3, we hope you will have a
general understanding of what such solvers look like, and
what they can do."""


from z3 import *


class Todo(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__()


########################################
# Basic propositional logic

# In Z3, we can declare two propositions just as booleans, this
# is rather natural, for propositions can have values true or false.
# To declare two propositions P and Q:
P = Bool('P')
Q = Bool('Q')
# or, we can use a more compact shorthand:
P, Q = Bools('P Q')

# We can build propositions by writing Lisp-style abstract
# syntax trees, for example, the disjunction:
# P \/ Q
# can be encoded as the following AST:
F = Or(P, Q)

# Note that the connective '\/' is called 'Or' in Z3, we'll see
# several other in the next.

# The simplest usage for Z3 is to feed the proposition to Z3
# directly, to check the satisfiability, this can be done by
# calling the # 'solve()' function:
solve(F)

# Simply speaking, the "solve()" function will create an instance
# of solver, check the satisfiability of the proposition, and
# output a model in which that proposition is satisfiable.

# For the above call, the Z3 will output something like this:
# [P=True, Q=False]
# which is a model with assignments to proposition P and Q that
# makes the proposition F satisfiable. Obviously, this is just
# one of several possible models.

# Same as disjunction, the conjunction
# P /\ ~Q
# can be encoded as the following AST
F = And(P, Not(Q))

# Note that we use Not(Q) to encode ~Q

# Then we use solve to find a model that satisfy the proposition
solve(F)

###########################################################
# Now you have know the basic usage of using z3 to find the solution that
# will satisfy a proposition.
#
# TODO: Exercise 1-1
# Try to find solution that satisfies proposition: (P /\ Q) \/ R
# raise Todo("Exercise 1-1: try to find solution that satisfies proposition: (P /\\ Q) \\/ R")
P, Q, R = Bools('P Q R')
solve(Or(And(P, Q), R))

# TODO: Exercise 1-2
# Try to find solution that satisfies proposition: P \/ (Q \/ R)
# raise Todo("Exercise 1-2: try to find solution that satisfies proposition: P \\/ (Q \\/ R")
P, Q, R = Bools('P Q R')
solve(Or(P, Or(Q, R)))


###########################################################
# In Exercise 1-1 you've see the basic usage of z3 for describing propositions.
# Like And, Or, Not. Also how to use the solve method to get the solution.

# But keep in mind that not all propositions are satisfiable, consider:
# F = P /\ ~P
P = Bool('P')
F = And(P, Not(P))
solve(F)

# Z3 will output:
# "no solution"
# which indicates that the proposition F is not satisfiable, that
# is, the proposition F cannot be true for any possible values
# of P.

# TODO: Exercise 1-3
# Consider proposition (P \/ Q) /\ (Q /\ R) /\ (P /\ ~R). Complete below code,
# Z3 will show you that no solution can satisfy it.
# raise Todo("Exercise 1-3: try to solve proposition: (P \\/ Q) /\\ (Q /\\ R) /\\ (P /\\ ~R)")
P, Q, R = Bools('P Q R')
solve(And(Or(P, Q), And(Or(Q, R), Or(P, Not(R)))))


# TODO: Exercise 1-4
# Try to solve proposition
# (P /\ ~S /\ R) /\ (R /\ ( ~P \/ (S /\ ~Q)))
# raise Todo("Exercise 1-4: try to solve proposition: (P /\\ ~S /\\ R) /\\ (R /\\ ( ~P \\/ (S /\\ ~Q)))")
P, Q, R, S = Bools('P Q R S')
solve(And(And(P, Not(S), R), And(R, Or(Not(P), And(S, Not(Q))))))


###########################################################
# You may notice that some problems in Exercise 1 has more than one solutions
# that satisfy it, but the solve method only provider you 1 solution.
# To Get another solution that can satisfy it. What you need to do is add
# constraints to solver to get different solutions as below example.

# Consider again our first example, in exercise 1:
# P \/ Q
# By default, Z3 only outputs the one row in
# the truth table:
"""
  P    Q     P\/Q
  t    t     t
  t    f     t
  f    t     t
  f    f     f
"""
# After all, we're asking Z3 about the satisfiability of the proposition,
# so one row of evidence is enough.

# What if we want Z3 to output all the assignment of propositions
# that make the proposition satisfiable, not just the first one.
# For the above example, we want the all first 3 rows.

# Here is the trick: when we get an answer, we negate the
# answer, make a conjunction with the original proposition,
# then check the satisfiability again. For the above example:
P, Q = Bools('P Q')
F = Or(P, Q)
solve(F)


# Z3 outputs:
# [P=True, Q=False]

# we want to build this:
F = And(F, Not(And(P, Not(Q))))
solve(F)
# Z3 output this:
# [P = False, Q = True]

# continue the building process:
F = And(F, Not(And(Not(P), Q)))
solve(F)
# Z3 output this:
# [P = True, Q = True]

# continue the building process:
F = And(F, Not(And(P, Q)))
solve(F)
# Z3 output this:
# "no solution"

# In fact, what we Add to F can be treated as constraints, by add negation of
# each solution given by solve method, we can get a new solution which is
# different from solutions we get before. We doing this until no new solution
# can be found, aka. "no solution" by solve, that means we get all solutions.


# TODO: Exercise 1-5
# Now you have know how to add constraint to solver to get different solutions
# from z3. Try to get **all solutions** that satisfy the proposition in
# Exercise 1-1: (P /\ Q) \/ R
# raise Todo("Exercise 1-5: try to get all solutions of proposition: (P /\\ Q) \\/ R")
P, Q, R = Bools('P Q R')
F = Or(And(P, Q), R)
solve(F)

F = And(F, Not(And(Not(R), Q, P)))
solve(F)

F = And(F, Not(And(R, Q, P)))
solve(F)

F = And(F, Not(And(R, Not(Q), Not(P))))
solve(F)

F = And(F, Not(And(R, Not(Q), P)))
solve(F)

F = And(F, Not(And(R, Q, Not(P))))
solve(F)

# We can automate the above process, for this, we should expose
# more internal capability of Z3. Consider our first example again:
# P /\ Q

# To create a new SMT solver:
solver = Solver()

P, Q = Bools('P Q')
F = Or(P, Q)
# add the proposition F into the solver:
solver.add(F)
# you can add more propositions into the solver, and the solver
# will try to check the conjunction of these propositions.

# To check whether or not the current solver is satisfiable:
print(solver.check())
# meanwhile, also store other results, say, the concrete values
# for the propositions, etc..

# To get the model:
print(solver.model())
# this is effective, only if the solver is "sat". To be specific,
# the model contains all the values for propositions (a map):
model = solver.model()
print(model[P], model[Q])

# To wrap these together, we have this code:
solver = Solver()
# to add the proposition F again:
P, Q = Bools('P Q')
props = [P, Q]
F = Or(P, Q)
solver.add(F)
print(solver.check())
print(solver.model())


# TODO: Exercise 1-6
# Now it's your turn, let's wrap all these facility into a nice function:
# Read and understand the code, then complete the lost part.

def sat_all(props, f):
    """Get all solutions of given proposition set props that satisfy f

    Arguments:
        props {BoolRef} -- Proposition list
        f {Boolref} -- logical express that consist of props
    """
    solver = Solver()
    solver.add(f)
    result = []
    while solver.check() == sat:
        m = solver.model()
        result.append(m)
        block = []
        for prop in props:
            prop_is_true = m.eval(prop, model_completion=True)

            if prop_is_true:
                new_prop = prop
            else:
                new_prop = Not(prop)

            block.append(new_prop)

        # raise Todo("Exercise 1-6: try to complete the lost part in the function of `set_all`")
        # f = And(f, Not(And(block)))
        solver.add(Not(And(block)))

    print("the given proposition: ", f)
    print("the number of solutions: ", len(result))

    def print_model(m):
        print(sorted([(d, m[d]) for d in m], key=lambda x: str(x[0])))

    for m in result:
        print_model(m)


# If you complete the function. Try to use it for below props.
sat_all([P, Q], Or(P, Q))
sat_all([P], Implies(P, P))
R = Bool('R')
sat_all([P, Q, R], Or(P, Q, R))
# Well done, you've complete exercise 1. Remember to save it for later hands in.