"""
This file contains the functions for visualizing the results of the solutions
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as plta

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


def visualize_simulated_annealing(all_solutions=None, accepted_solutions=None, best_solutions=None, animation=False, save=False):
    """
    This function will maken a visualization of the process of the simulated annealing.

    Args:
        all_solutions(list): This is a list of the candidate solution at a given iteration
        accepted_solutions(list): This is a list of the latest accepted_solution at a given iteration
        best_solutions(list): This is a list of the best solution at a given iteration
        animation(bool): When True it will create an animation of the process, standart it is False
        save(bool): When True will save the animation
    
    Returns:
        An image of the process of the simulated annealing
        And maybe even a video
    """
    everything = []

    fig1, ax1 = plt.subplots()
    
    if type(best_solutions) == list:
        everything += best_solutions
        its = np.arange(len(best_solutions))
        best = ax1.plot(its, best_solutions, label="Best", mec="purple")

    if type(accepted_solutions) == list:
        everything += accepted_solutions
        its = np.arange(len(accepted_solutions))
        accepted = ax1.plot(its, accepted_solutions, label="Current", mec="orange")

    if type(all_solutions) == list:
        everything += all_solutions
        its = np.arange(len(all_solutions))
        all = ax1.plot(its, all_solutions, label="Candidate", mec="green")

    ax1.set(xlim=(-1, len(its) + 1), ylim=(min(everything) - 10, max(everything) + 10), xlabel="Iteration", ylabel="Total Penalty")
    ax1.legend()

    if animation == True:
        fig2, ax2 = plt.subplots()

        if type(best_solutions) == list:
            best2 = ax2.plot(its[0], best_solutions[0], label="Best: ", mec="purple")[0]

        if type(accepted_solutions) == list:
            accepted2 = ax2.plot(its[0], accepted_solutions[0], label="Current: ", mec="orange")[0]

        if type(all_solutions) == list:
            all2 = ax2.plot(its[0], all_solutions[0], label="Candidate: ", mec="green")[0]

        breathing_room = (max(everything) - min(everything))/10
        ax2.set(xlim=(-1, len(its) + 1), ylim=(min(everything) - breathing_room, max(everything) + breathing_room), xlabel="Iteration", ylabel="Total Penalty")
        ax2.legend()

        def update_animation(frame):
            if type(best_solutions) == list:
                nonlocal best2
                best2.set_xdata(its[:frame])
                best2.set_ydata(best_solutions[:frame])
                best2.set_label(f"Best: {best_solutions[frame]:.0f}")
            else:
                best2 = None
            
            if type(accepted_solutions) == list:
                nonlocal accepted2
                accepted2.set_xdata(its[:frame])
                accepted2.set_ydata(accepted_solutions[:frame])
                accepted2.set_label(f"Current: {accepted_solutions[frame]:.0f}")
            else:
                accepted2 = None

            if type(all_solutions) == list:
                nonlocal all2
                all2.set_xdata(its[:frame])
                all2.set_ydata(all_solutions[:frame])
                all2.set_label(f"Candidate: {all_solutions[frame]:.0f}")
            else:
                all2 = None

            ax2.set_xlabel(f"Iteration: {frame}")
            ax2.legend()
            update_frame = [all2, accepted2, best2]
            update_frame = filter(lambda n: type(n) != None, update_frame)
            return tuple(update_frame)

        interval = int(30000/len(its))
        ani = plta.FuncAnimation(fig=fig2, func=update_animation, frames=len(its), interval=interval)

        if save == True:
            ani.save(filename="Animation_of_s_a(s_a_does_not_stand_for_sexual_assault).gif", writer="pillow")

        return fig2, ani

    return fig1
