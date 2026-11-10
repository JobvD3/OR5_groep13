import greedy_constructive_heuristic as gch
import simulated_annealing_meta_heuristic as sam

[orders, machines, setups] = gch.import_data("September")

[orders1, machines1] = gch.greedy_constructive(orders, machines, setups)

[orders2, order2_score] = sam.simulated_annealing(orders1, machines1, setups, 1000, 1000, 100)

print(orders2)
print(order2_score)