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


# TODO: Exercise 5
# Seat Arrangement Problem
# Alice, Bob, Carol take 3 seats. But they have some requirements:
#   1. Alice can not sit near to Carol;
#   2. Bob can not sit right to Alice.
# Questions:
#   1. Is there any solution?
#   2. How many solutions in total?

# Now let us investigate the problem


def seat_arrangement():
    solver = Solver()
    # 1. First we need to modeling the problem
    # Let say:
    #   A_i means Alice takes seat Ai,
    #   B_i means Bob takes seat Bi,
    #   C_i means Carol takes seat Ci.
    # And since there are only 3 seats, so 1 <= i <= 3

    n_seat = 3
    a1, a2, a3 = Bools('a1 a2 a3')
    b1, b2, b3 = Bools('b1 b2 b3')
    c1, c2, c3 = Bools('c1 c2 c3')

    # alice must take a seat:
    alice_take_seat_1 = And(a1, Not(a2), Not(a3), Not(b1), Not(c1))
    alice_take_seat_2 = And(a2, Not(a1), Not(a3), Not(b2), Not(c2))
    alice_take_seat_3 = And(a3, Not(a1), Not(a2), Not(b3), Not(c3))
    solver.add(Or(alice_take_seat_1, alice_take_seat_2, alice_take_seat_3))

    # bob must take a seat:
    # raise Todo("Exercise 5-1: try to add constraints that indicate Bob must take a seat")
    bob_take_seat_1 = And(b1, Not(b2), Not(b3), Not(a1), Not(c1))
    bob_take_seat_2 = And(b2, Not(b1), Not(b3), Not(a2), Not(c2))
    bob_take_seat_3 = And(b3, Not(b1), Not(b2), Not(a3), Not(c3))
    solver.add(Or(bob_take_seat_1, bob_take_seat_2, bob_take_seat_3))

    # carol must take a seat:
    # raise Todo("Exercise 5-2: try to add constraints that indicate Carol must take a seat")
    carol_take_seat_1 = And(c1, Not(c2), Not(c3), Not(a1), Not(b1))
    carol_take_seat_2 = And(c2, Not(c1), Not(c3), Not(a2), Not(b2))
    carol_take_seat_3 = And(c3, Not(c1), Not(c2), Not(a3), Not(b3))
    solver.add(Or(carol_take_seat_1, carol_take_seat_2, carol_take_seat_3))

    # alice can not sit near to carol:
    alice_not_near_carol = And(Implies(a1, Not(c2)), Implies(a2, Not(Or(c1, c3))), Implies(a3, Not(c2)))
    solver.add(alice_not_near_carol)

    # 3. Bob can not sit right to Alice
    # raise Todo("Exercise 5-3: try to add constraints that indicate Bob can not sit right to Alice")
    bob_not_right_alice = And(Implies(b2, Not(a1)), Implies(b3, Not(a2)))
    solver.add(bob_not_right_alice)

    # Hint: here only one solution is printed, you may change this to
    # print all the solutions to check your implementation.
    solver.check()
    model = solver.model()
    # print(model)
    # fancy printing
    if model.evaluate(a1):
        print("Alice ", end='')
    if model.evaluate(b1):
        print("Bob ", end='')
    if model.evaluate(c1):
        print("Carol ", end='')
    if model.evaluate(a2):
        print("Alice ", end='')
    if model.evaluate(b2):
        print("Bob ", end='')
    if model.evaluate(c2):
        print("Carol ", end='')
    if model.evaluate(a3):
        print("Alice", end='')
    if model.evaluate(b3):
        print("Bob", end='')
    if model.evaluate(c3):
        print("Carol", end='')


if __name__ == '__main__':
    # seat_arrangement should have 1 solution
    seat_arrangement()