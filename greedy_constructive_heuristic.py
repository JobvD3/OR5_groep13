"""
This file contains the nessesery functions for the greedy constructive rule
"""

import numpy as np
import pandas as pd


def import_data(month : str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]|None:
    """
    Imports the data of the requested month and adds essential columns
    """
    if month.lower() == "september":
        orders = pd.read_excel("PaintShop - September 2026.xlsx", sheet_name=0)
        machines = pd.read_excel("PaintShop - September 2026.xlsx", sheet_name=1)
        setups = pd.read_excel("PaintShop - September 2026.xlsx", sheet_name=2)
    else:
        print("nope")
        return

    #Voegt een column toe voor de start tijd
    orders["Start"] = [0.0 for i in range(len(orders))] 

    #Voegt een column toe voor de eind tijd
    orders["End"] = [0.0 for i in range(len(orders))] 

    #Voegt een column toe voor de opgelopen penalty van een order
    orders["Penalty_order"] = [0.0 for i in range(len(orders))]

    #Voegt een column toe om aan te geven dat de order klaar is
    orders["Done"] = [False for i in range(len(orders))] 

    #Voegt een column toe die aangeft welke machine het heeft gedaan
    orders["Machine"] = ["None" for i in range(len(orders))] 

    #Sorteert de dataframe op kleur en oppervlakte
    orders = orders.sort_values(by = ["Colour", "Surface"]) 

    #Voegt een column toe die aangeeft welke kleur de machine is
    machines["Colour"] = ["None" for i in range(len(machines))] 

    #Voegt een column toe voor de totale tijd dat de machine heeft gewerkt
    machines["Total_time"] = [0.0 for i in range(len(machines))] 

    #Sorteert de machines op snelheid
    machines = machines.sort_values(by = ["Speed"]).reset_index(drop=True) 

    for i in setups["To colour"].unique():
        #Voegt de setups toe van geen kleur naar een kleur
        setups.loc[len(setups)] = ["None", i, 0] 
        #Voegt de setups toe van dezelfde kleur naar dezelfde kleur
        setups.loc[len(setups)] = [i, i, 0] 
    return orders, machines, setups

def choose_machine(machines : pd.DataFrame) -> str:
    """
    Chooses the first availible machine, if multiple machines are availible at the same time,
    pick the fastest one of them.

    returns the choosen machine as a string
    """
    machine = machines.sort_values(by = ["Total_time", "Speed"],
                                    ascending = [True, False]).Machine.iloc[0]
    return machine

def setup_time_machine(machines, setups, machine) -> list:
    """
    Makes a dictionary where the keys are the colours a machine could change to and where the
    values are the setup times of the colours.

    The dictionary is sorted by the setup time in ascending order

    Returns a dictionary
    """
    df_setup_time = setups[setups["From colour"] == machines.Colour[machines.Machine == machine].iloc[0]].copy()
    df_setup_time = df_setup_time.sort_values("Setup time")
    #print(df_setup_time)
    key = list(df_setup_time["To colour"])
    value = list(df_setup_time["Setup time"])
    setup_time = dict(zip(key, value))
    return setup_time

def choose_order(orders : pd.DataFrame, machines : pd.DataFrame, setups : pd.DataFrame,
                  machine : str) -> pd.Series:
    """
    Chooses the order with the lowest potential penalty, if multiple orders have the lowest 
    potential penalty, then choose the order with the highest penalty per time unit, if 
    multiple orders have the highest penalty per time unit, then choose the one with the lowest
    deadline, if there are multiple with the lowest deadline choose the one with the lowest
    setup time.

    Returns the choosen order
    """

    df = orders.loc[orders.Done == False].copy()
    setup_time = setup_time_machine(machines, setups, machine)
    #print(setup_time)
    df_machine = machines.loc[machines.Machine == machine].copy()

    for row in df.iterrows():
        order = row[1]
        time_colour_change = setup_time[order.Colour]
        order.Start = df_machine.Total_time.iloc[0] + time_colour_change
        order.End = order.Start + order.Surface/df_machine.Speed.iloc[0]
        if order.End > order.Deadline:
            order.Penalty_order = (order.End - order.Deadline)*order.Penalty
        else:
            order.Penalty_order = 0
        df.loc[df.Order == order.Order] = list(order)

    df = df.sort_values(by = ["Penalty_order", "Penalty", "Deadline"], ascending = [False, False, True])
    choices = df.loc[df.Penalty_order == df.Penalty_order.iloc[0]]
    if len(choices) > 1:
        choices = choices.loc[choices.Penalty == choices.Penalty.iloc[0]]
        if len(choices) > 1:
            choices = choices.loc[choices.Deadline == choices.Deadline.iloc[0]]
            if len(choices) > 1:
                for colour in list(setup_time.keys):
                    choice = choices.loc[choices.Colour == colour]
                    if len(choice > 0):
                        choice = choice.Order.iloc[0]
            else:
                choice = choices.Order.iloc[0]
        else:
            choice = choices.Order.iloc[0]
    else:
        choice = choices.Order.iloc[0]

    choices.loc[choices.Order == choice, "Machine"] = machine
    choices.loc[choices.Order == choice, "Done"] = True
    for row in choices.iterrows():
        s_choice = row[1]
    return s_choice

def update_plan(orders : pd.DataFrame, machines : pd.DataFrame, s_choice : pd.Series) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Updates the orders and machines
    """
    df_orders = orders.copy()
    df_machines = machines.copy()

    df_orders.loc[df_orders.Order == s_choice.Order] = list(s_choice)
    df_machines.loc[df_machines.Machine == s_choice.Machine, "Total_time"] = s_choice.End
    df_machines.loc[df_machines.Machine == s_choice.Machine, "Colour"] = s_choice.Colour
    return df_orders, df_machines 

def greedy_constructive(orders : pd.DataFrame, machines : pd.DataFrame, setups : pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df_orders = orders.copy()
    df_machines = machines.copy()

    while len(df_orders[df_orders.Done == False]) > 0:
        machine = choose_machine(df_machines)
        s_choice = choose_order(df_orders, df_machines, setups, machine)
        [df_orders, df_machines] = update_plan(df_orders, df_machines, s_choice)
    plan_orders = df_orders.sort_values(by = ["Machine", "Start"])
    plan_machines = df_machines.sort_values("Machine")
    return plan_orders, plan_machines

[a, b, c] = import_data("September")
[plan, plan_machines] = greedy_constructive(a, b, c)
print(plan_machines)
print(plan)
print(c)