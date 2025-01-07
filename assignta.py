"""
assignta.py: Optimizing the allocation of TAs to lab sections in order to minimize different penalties such as
             overallocation, conflicts, undersupport, unwilling assignments, and unpreferred assignments.
             Uses objective functions to determine penalties and agents to randomly modify solutions to reduce penalties
Author: Diya Ganesh
"""

import random as rnd
import pandas as pd
import numpy as np
import copy
import csv
from evo import Evo
import profiler

tas_df = pd.read_csv("tas.csv")
sections_df = pd.read_csv("sections.csv")

# OBJECTIVE FUNCTIONS
def overallocation(solution):
    """ Find overallocation penalty (assigned sections - maximum requested sections)."""
    max_assigned = tas_df['max_assigned'].to_numpy()
    actual_assigned = solution.sum(axis=1)
    overallocation_penalty = int(np.maximum(0, actual_assigned - max_assigned).sum())
    return overallocation_penalty

def conflicts(solution):
    """ Find the number of TAs with time conflicts (assigning TAs to labs meeting at the same time)."""
    section_times = sections_df['daytime'].to_numpy()
    conflict_count = 0
    for ta_assignments in solution:
        assigned_sections = np.where(ta_assignments == 1)[0]
        assigned_times = section_times[assigned_sections]
        if len(assigned_times) != len(np.unique(assigned_times)):
            conflict_count += 1
    return conflict_count

def undersupport(solution):
    """ Find the total undersupport penalty (min required TAs - allotted TAs) across all sections."""
    min_ta = sections_df['min_ta'].to_numpy()
    assigned_counts = solution.sum(axis=0)
    undersupport_penalty = int(np.maximum(0, min_ta - assigned_counts).sum())
    return undersupport_penalty

def unwilling(solution):
    """ Find the number of times a TA to is allocated to a section they are unwilling to."""
    preferences = tas_df.iloc[:, 3:].to_numpy()
    unwilling_penalty = int(np.sum(solution * (preferences == 'U')))
    return unwilling_penalty

def unpreferred(solution):
    """ Find the number of times a TA to is allocated to a section where they said “willing” but not “preferred”."""
    preferences = tas_df.iloc[:, 3:].to_numpy()
    unpreferred_penalty = int(np.sum(solution * (preferences == 'W')))
    return unpreferred_penalty

# AGENTS
@profiler.profile
def random_agent(solution):
    """
    Agent that randomly modifies the current solution.
    Returns a new solution where a TA is randomly assigned or unassigned to the section.
    """
    new_solution = copy.deepcopy(solution)[0]
    ta_idx = rnd.randint(0, new_solution.shape[0] - 1)
    section_idx = rnd.randint(0, new_solution.shape[1] - 1)
    new_solution[ta_idx, section_idx] = 1 - new_solution[ta_idx, section_idx]
    return new_solution

@profiler.profile
def overallocation_agent(solution):
    """
    Agent that tries to minimize overallocation by reducing assignments for overallocated TAs.
    Returns a new solution where a randomly overallocated TA is removed from a random one of their sections
    """
    new_solution = copy.deepcopy(solution)[0]
    max_assigned = tas_df['max_assigned'].to_numpy()
    actual_assigned = new_solution.sum(axis=1)
    overallocated_tas = np.where(actual_assigned > max_assigned)[0]

    if len(overallocated_tas) > 0:
        ta_idx = rnd.choice(overallocated_tas)
        ta_max = tas_df['max_assigned'][ta_idx]
        assigned_sections = np.where(new_solution[ta_idx] == 1)[0]
        if len(assigned_sections) > ta_max:
            section_idx = rnd.choice(assigned_sections)
            new_solution[ta_idx, section_idx] = 0
    return new_solution

@profiler.profile
def conflict_agent(solution):
    """
    Agent that tries to minimize conflicts by unassigning TAs from a random one of their conflicting sections.
    Returns a new solution where a TAs is randomly unassigned from one of their conflicting sections.
    """
    new_solution = copy.deepcopy(solution)[0]
    section_times = sections_df['daytime'].to_numpy()
    for ta_idx, ta_assignments in enumerate(new_solution):
        assigned_sections = np.where(ta_assignments == 1)[0]
        assigned_times = section_times[assigned_sections]
        time_counts = {}
        for time in assigned_times:
            if time in time_counts:
                time_counts[time] += 1
            else:
                time_counts[time] = 1
        conflicting_sections = [assigned_sections[i] for i, time in enumerate(assigned_times) if time_counts[time] > 1]
        if len(conflicting_sections) > 0:
            section_to_unassign = rnd.choice(conflicting_sections)
            new_solution[ta_idx, section_to_unassign] = 0
    return new_solution

@profiler.profile
def undersupport_agent(solution):
    """
    Agent that tries to minimize undersupport by assigning TAs to undersupported sections.
    Returns a new solution where an available TA is assigned to the randomly chosen undersupported section.
    """
    new_solution = copy.deepcopy(solution)[0]
    min_ta = sections_df['min_ta'].to_numpy()
    assigned_counts = new_solution.sum(axis=0)
    undersupported_sections = np.where(assigned_counts < min_ta)[0]

    if len(undersupported_sections) > 0:
        section_idx = rnd.choice(undersupported_sections)
        available_tas = np.where(new_solution[:, section_idx] == 0)[0]
        if len(available_tas) > 0:
            ta_idx = rnd.choice(available_tas)
            new_solution[ta_idx, section_idx] = 1  # Assign TA to the section
    return new_solution

@profiler.profile
def unwilling_agent(solution):
    """
    Agent that tries to minimize the number of times a TA is assigned to a section they are unwilling to support.
    Returns a new solution where a TA is unassigned from a random section they are unwilling to support.
    """
    new_solution = copy.deepcopy(solution)[0]
    preferences = tas_df.iloc[:, 3:].to_numpy()
    unwilling_assignments = np.where((new_solution == 1) & (preferences == 'U'))

    if len(unwilling_assignments[0]) > 0:
        idx = rnd.randint(0, len(unwilling_assignments[0]) - 1)
        ta_idx, section_idx = unwilling_assignments[0][idx], unwilling_assignments[1][idx]
        new_solution[ta_idx, section_idx] = 0
    return new_solution

# CLASS INSTANCE CREATION
def initialize_evo(initial_solution):
    """ Create an instance of the Evo class and add an initial solution"""
    evo = Evo()

    # add objective functions
    evo.add_fitness_criteria("overallocation", overallocation)
    evo.add_fitness_criteria("conflicts", conflicts)
    evo.add_fitness_criteria("undersupport", undersupport)
    evo.add_fitness_criteria("unwilling", unwilling)
    evo.add_fitness_criteria("unpreferred", unpreferred)

    # add agents
    evo.add_agent("random agent", random_agent)
    evo.add_agent("overallocation minimizer", overallocation_agent)
    evo.add_agent("conflicts minimizer", conflict_agent)
    evo.add_agent("undersupport minimizer", undersupport_agent)
    evo.add_agent("unwilling minimizer", unwilling_agent)

    # add initial solution to evo
    evo.add_solution(initial_solution)

    return evo

@profiler.profile
def run_evolve(evo, time_in_sec):
    """ Run the evolve method of an Evo instance for a certain amount of time in seconds"""
    evo.evolve(time_limit=time_in_sec)

# WRITE FILES
def create_summary_table(filename, evo):
    """ Creates a summary table in comma-delimited value file where each row is one non-dominated
    Pareto-optimal solution and each column is the score for one objective."""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["groupname", "overallocation", "conflicts", "undersupport", "unwilling", "unpreferred"]
        writer.writerow(field)
        for solution in evo.pop.keys():
            groupname = 'AssignTA'
            overallocation_score = solution[0][1]
            conflicts_score = solution[1][1]
            undersupport_score = solution[2][1]
            unwilling_score = solution[3][1]
            unpreferred_score = solution[4][1]
            writer.writerow([groupname, overallocation_score, conflicts_score,
                             undersupport_score, unwilling_score, unpreferred_score])

def create_best_solution_txt(filename, evo):
    """ Creates a txt file with the best solution, with its objective function scores, which sections
        each TA is assigned to and which TAs are assigned to each section
        NOTE: Justification has been written directly in the file to prevent clutter in code file
    """
    best_solution = evo.get_best_solution()

    with open(filename, "w") as file:
        # Scores for each objective function
        file.write("Objective function scores:\n")
        for obj, score in best_solution[0]:
            file.write(f"{obj}: {score}\n")
        file.write("\n")

        # List of sections for each TA
        file.write("Sections for each TA:\n")
        for i, row in enumerate(evo.pop[best_solution[0]]):
            sections = np.where(row == 1)[0] + 1
            file.write(f"TA{i + 1}: Sections {list(sections)}\n")
        file.write("\n")

        # List of TAs for each section
        file.write("TAs for each section:\n")
        num_sections = evo.pop[best_solution[0]].shape[1]
        for j in range(num_sections):
            tas = np.where(evo.pop[best_solution[0]][:, j] == 1)[0] + 1
            file.write(f"Section {j + 1}: TA {list(tas)}\n")

def main():
    # initialize evo using test 1 as the initial case
    # I used all three tests as potential initial cases, and they returned the same nds's and best solution
    # Thus, I felt it unnecessary to create a new initial case
    initial_solution = np.loadtxt("/Users/Diya/Downloads/ds3500/hw5/test1.csv", delimiter=",")
    evo = initialize_evo(initial_solution)

    # run the Evo instance to evolve solutions
    run_evolve(evo, 299.99)

    # create summary table of all non-denominated solutions
    create_summary_table('/Users/Diya/Downloads/ds3500/hw5/summary_table.csv', evo)

    # show best solution
    best_solution = evo.get_best_solution()
    print(f"Minimized objectives: {best_solution[0]}")
    print(f"Solution average: {best_solution[1]}")
    print(f"Solution matrix:\n{evo.pop[best_solution[0]]}")

    # add the best solution to txt file
    create_best_solution_txt("/Users/Diya/Downloads/ds3500/hw5/best_solution.txt", evo)

if __name__ == '__main__':
    main()
    # return runtimes
    with open("/Users/Diya/Downloads/ds3500/hw5/profiling_report.txt", "w") as file:
        file.write(profiler.Profiler.report())
