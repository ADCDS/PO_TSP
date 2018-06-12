"""
    This is an implementation of a cplex model that solves de Traveling Salesman Problem
    using LazyConstraintCallback to add loops constraints

"""

from docplex.mp.model import Model
import numpy as np
import utils
import sys

from cplex.callbacks import LazyConstraintCallback


class Callback(LazyConstraintCallback):
    def __call__(self):

        if not self.is_unbounded_node():
            # Find loops inside the solution
            loops = utils.find_loops_linear(self.get_values(), self.row_count)

            if len(loops) > 1:
                # Foreach loop found, add a restriction to eliminate it
                for j in range(len(loops)):
                    loop = loops[j]

                    # Expressions for the loop and reverse loop
                    expr = [None] * len(loop)
                    expr_rev = [None] * len(loop)

                    # We need the variables names (?)
                    for i, e in enumerate(loop):
                        if i < (len(loop) - 1):
                            expr[i] = 'E_' + str(e) + '_' + str(loop[i + 1])
                            expr_rev[i] = 'E_' + str(loop[i + 1]) + '_' + str(e)
                    expr[i] = 'E_' + str(e) + '_' + str(loop[0])
                    expr_rev[i] = 'E_' + str(loop[0]) + '_' + str(e)

                    # I don't know why the fuck this have to be this way, but this add the constraint
                    # sp = SparsePair(ind=expr, val=[1] * len(expr))
                    # sp_rev = SparsePair(ind=expr_rev, val=)

                    self.add(constraint=[expr, [1] * len(loop)], sense="LE", rhs=len(loop) - 1)
                    self.add(constraint=[expr_rev, [1] * len(loop)], sense="LE", rhs=len(loop) - 1)
        else:
            print("Unbounded node")

def distance(X, Y):
    a = np.array((X['x'], X['y'], 1))
    b = np.array((Y['x'], Y['y'], 1))
    # print('{} <= {} '.format(np.linalg.norm(a - b), antenna['r']))
    return np.linalg.norm(a - b)


mdl = Model()
mdl.parameters.mip.display.set(5)
mdl.set_log_output(sys.stdout)
# mdl.parameters.threads.set(16)

data = utils.read_instances()
row_count = data.shape[0]

distances = [[distance(data.iloc[i], data.iloc[j]) for j in range(row_count)] for i in range(row_count)]
edges = [[mdl.binary_var('E_' + str(i) + '_' + str(j)) for j in range(row_count)] for i in range(row_count)]

# Self loop restriction
for i in range(row_count):
    mdl.add(edges[i][i] == 0)

# Column restriction
for i in range(row_count):
    column_restriction = 0
    for j in range(row_count):
        column_restriction += edges[i][j]
    mdl.add(column_restriction == 1)

# Row restriction
for i in range(row_count):
    row_restriction = 0
    for j in range(row_count):
        row_restriction += edges[j][i]
    mdl.add(row_restriction == 1)

# Objective function
obj = 0
for i in range(row_count):
    for j in range(row_count):
        obj += edges[i][j] * distances[i][j]

mdl.minimize(obj)

# Add callback
cb = mdl.register_callback(Callback)

# Add attributes to Callback object, so i can access them inside de Callback
cb.row_count = row_count

slv = mdl.solve()

# Draw the graph
utils.draw_graph(data, edges)
