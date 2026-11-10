"""
Here you will find the functions for simulated annealing
"""

import numpy as np
import pandas as pd
import greedy_constructive_heuristic as gch

def calculate_plan(orders : pd.DataFrame, machines : pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    This function will update the columns of the orders and machines

    Args:
        orderds(pandas.DataFrame): The dataframe with information about the orders
        machines(pandas.DataFrame): The dataframe with information about the machines
    
    Returns:
        A recalculated orders plan
        A recalculated machines dataframe
    """

    df_o = orders.sort_values(["Machine", "Start"], ascending=[True, True]).copy()
    df_m = machines.copy()

    for machine in df_m["Macchine"]:
        speed = df_m["Speed"].loc[df_m["Macchine"] == machine]

        start = [0]
        end = []
        penalty = []
        df_om = df_o.loc[df_o["Machine"] == machine]
        for i in df_om[1:]:
            duration = i[1]/speed
            end.append(start[-1] + duration)
            start.append(end[-1])
            if end[-1]
