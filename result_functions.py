"""
This file contains the functions for visualizing the results of the solutions
"""

import pandas as pd
import matplotlib.pyplot as plt

def make_gantt_chart(solution : pd.DataFrame):
    """
    This function will create a Gantt Chart based on the given solution

    Args:
        solution(pandas.DataFrame): This is a dataframe which contains the current solution
    
    Returns:
        A Gantt-Chart to visualize the solution
    """
    df = solution.copy()

    y_heigt = 10
    place_machine = {}
    for machine in df["Machine"].unique():
        place_machine[machine] = y_heigt
        y_heigt += 11

    fig, gnt = plt.subplots()

    gnt.set_title("Gantt-Chart of order sequence")
    gnt.set_xlabel("Time")
    gnt.set_ylabel("Machine")
    
    gnt.set_yticks(list(place_machine.values()))
    gnt.set_yticklabels(list(place_machine.keys()))

    for i in df.iterrows():
        row = i[1]
        if row["Setup_time"] > 0:
            start = row["Start"] - row["Setup_time"]
            gnt.broken_barh([(start, row["Setup_time"])], (place_machine[row["Machine"]] - 5, 10), facecolor="gray", edgecolor="k")

        gnt.broken_barh([(row["Start"], row["Duration"])], (place_machine[row["Machine"]] - 5, 10), facecolor=row["Colour"].lower(), edgecolor="k")
        gnt.text(x=row["Start"] + row["Duration"]/2, y=place_machine[row["Machine"]], s=row["Order"], ha="center", va="center", size="xx-small")

    fig.set_figheight(1)
    fig.set_figwidth(10)
    plt.show()
    return fig