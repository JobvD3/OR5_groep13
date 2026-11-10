"""
Here you will find the functions for simulated annealing
"""

import numpy as np
import pandas as pd

def get_setup_time(colour1 : str, colour2 : str, setups : pd.DataFrame) -> float|int:
    """
    This function will give you the time that it takes to switch a machine from colour1 to colour 2

    Args:
        colour1(str): Is the present colour
        colour2(str): Is the colour you want to change to
        setups(pandas.DataFrame): Is the dataframe with the information of the setups
    
    Returns:
        The time that it takes to switch from colour1 to colour2
    """
    colour = setups.loc[((setups["From colour"] == colour1) & (setups["To colour"] == colour2)), "Setup time"].iloc[0]

    return colour

def calculate_plan(orders : pd.DataFrame, machines : pd.DataFrame, setups : pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    This function will update the columns of the orders and machines

    Args:
        orderds(pandas.DataFrame): The dataframe with information about the orders
        machines(pandas.DataFrame): The dataframe with information about the machines
        setups(pandas.DataFrame): The dataframe with the information of the setups
    
    Returns:
        A recalculated orders plan
        A recalculated machines dataframe
    """

    df_o = orders.sort_values(["Machine", "Start"], ascending=[True, True]).copy()
    df_m = machines.copy()

    for machine in df_m["Machine"]:
        speed = df_m.loc[df_m["Machine"] == machine, "Speed"].iloc[0]

        duration = []
        setup_time = []
        start = [0]
        end = []
        penalty = []
        
        df_om = df_o.loc[df_o["Machine"] == machine]
        previous_color = df_om["Colour"].iloc[0]
        for row in df_om.iterrows():
            order = row[1]
            
            duration.append(order["Surface"]/speed)
            setup_time.append(get_setup_time(previous_color, order["Colour"], setups))
            end.append(start[-1] + duration[-1])
            start[-1] += setup_time[-1]
            start.append(end[-1])
            if end[-1] > order["Deadline"]:
                penalty.append((end[-1] - order["Deadline"])*order["Penalty"])
            else:
                penalty.append(0)

            previous_color = order.Colour

        df_o.loc[df_o["Machine"] == machine, "Duration"] = duration
        df_o.loc[df_o["Machine"] == machine, "Setup_time"] = setup_time
        df_o.loc[df_o["Machine"] == machine, "Start"] = start[:-1]
        df_o.loc[df_o["Machine"] == machine, "End"] = end
        df_o.loc[df_o["Machine"] == machine, "Penalty_order"] = penalty

        df_m.loc[df_m["Machine"] == machine, "Total_time"] = end[-1]
        df_m.loc[df_m["Machine"] == machine, "Colour"] = order["Colour"]

    return df_o, sum(df_o["Penalty_order"]), df_m


def switch_rows(rowA : int, rowB : int, dataframe : pd.DataFrame) -> pd.DataFrame:
    """
    This function will switch two rows of a dataframe

    Args:
        rowA(int): Is the position of rowA 
        rowB(int): Is the position of rowB
        dataframe(pandas.DataFrame): Is the dataframe where the rows will be switched

    Returns:
        The dataframe with the switched rows
    """
    df = dataframe.copy()

    rng = np.random.default_rng(seed=42)

    rowa = df.iloc[rowA]
    rowb = df.iloc[rowB]

    df.iloc[rowA] = rowb
    df.iloc[rowB] = rowa

    rows = [rowA, rowB]
    for i in rows:
        if i - 1 >= 0 and i + 1 < len(df):
            machine1 = df.iloc[i - 1, -1]
            machine2 = df.iloc[i + 1, -1]
        elif i - 1 >= 0:
            machine1 = df.iloc[i - 1, -1]
            machine2 = machine1
        else:
            machine2 = df.iloc[i + 1, -1]
            machine1 = machine2

        if (machine1 == machine2) or (len(df.loc[df["Machine"] == machine1]) < len(df.loc[df["Machine"] == machine2])):
            df.iloc[i, -1] = machine1
        elif (len(df.loc[df["Machine"] == machine1]) > len(df.loc[df["Machine"] == machine2])):
            df.iloc[i, -1] = machine2
        elif rng.random() > 0.5:
            df.iloc[i, -1] = machine1
        else:
            df.iloc[i, -1] = machine2

    return df


def simulated_annealing(orders : pd.DataFrame, machines : pd.DataFrame, setups : pd.DataFrame, initial_q=1000, max_iterations=1000000, nmr_it_q=1000, alpha=0.9) -> pd.DataFrame:
    """
    This function will perform a simulated annealing over the selected dataframe

    Args:
        order(pandas.DataFrame): This is the dataframe with the information of the orders
        machines(pandas.DataFrame): This is the dataframe with the information of the machines
        setups(pandas.DataFrame): This is the dataframe with the information of the setups
        initial_q(int): The initial heat of the model standard is 1000
        max_iterations(int): The maximum number of iterations of the model standard is 1000000
        nmr_it_q(int): The number of iterations before q gets lowered
        alpha(float): The factor with which q will be reduced needs to be smaller than 1 standard is 0.9

    Returns:
        Hopefully an improved solution...
    """
    df = orders.copy()
    df = df.sort_values(["Machine", "Start"], ascending=[True, True])

    rng = np.random.default_rng(seed=42)

    q = initial_q

    best = [df, sum(df["Penalty_order"])]
    current = best

    it = 0
    while it <= max_iterations:
        new_current = False
        while new_current == False:
            random_list = np.arange(len(df))
            rng.shuffle(random_list)

            i_it = 0
            for i in random_list[:-1]:
                i_it += 1
                for j in random_list[i_it + 1:]:
                    new_o = switch_rows(i,j,current[0])
                    new = calculate_plan(new_o, machines, setups)[:-1]
                    
                    it += 1
                    if it%nmr_it_q == 0:
                        q = q*alpha
                    
                    if new[1] <= current[1]:
                        current = new
                        new_current = True
                        if current[1] <= best[1]:
                            best = current
                        break

                if new_current == True:
                    break

    return best

