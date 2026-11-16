import matplotlib.pyplot as plt

import greedy_constructive_heuristic as gch
import simulated_annealing_meta_heuristic as sam
import result_functions as rf

[orders, machines, setups] = gch.import_data("September")

[orders1, machines1] = gch.greedy_constructive(orders, machines, setups)

orders2, all, accepted, best = sam.simulated_annealing(orders1, machines1, setups, 5000, 5000, 50)

# gantt = rf.make_gantt_chart(orders2)
# print(orders2)
# print(order2_score)

img_sa = rf.visualize_simulated_annealing(accepted_solutions=accepted, best_solutions=best, animation=True, save=True)
plt.show()