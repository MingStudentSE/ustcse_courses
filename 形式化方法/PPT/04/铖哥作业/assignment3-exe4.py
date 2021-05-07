"""Applications of SAT via Z3

In the previous part we've discussed how to obtain solutions and prove
the validity for propositions.
In this part, we will try to use Z3 to solve some practical problems.
Hints:
 You can reuse the `sat_all` function that you've implemented in exercise 1
 if you think necessary."""

from z3 import *


class Todo(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__()


# TODO: Exercise 4
# Circuit Layout
# Usually When EE-Engineers design a circuit layout, they will verify it to
# make sure that the layout will not only output a single electrical level
# since it's useless.
# Now let's investigate the Circuit Layout we provide you.
# According to the requirement, what we should do is to convert the circuit layout
# into a proposition expression, let's say 'F', and try to obtains the solutions
# for F and Not(F).
# And then make sure that both F and Not(F) can be satisfied.
# First we convert it into proposition
def circuit_layout():
    a, b, c, d = Bools('a b c d')
    # raise Todo("Exercise 4: try to convert the circuit layout into logical propositions and find solutions")
    F = Or(And(d, And(a, b)), And(And(a, b), Not(c)))
    def sat_all(props, f):
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

            solver.add(Not(And(block)))
        
        print("the given proposition: ", f)
        print("the number of solutions: ", len(result))


    sat_all([a, b, c, d], F)
    sat_all([a, b, c, d], Not(F))



if __name__ == '__main__':
    # circuit_layout should have 3 solutions for F and 13 solutions for Not(F)
    circuit_layout()




