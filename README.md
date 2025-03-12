# AssignTA

**This project participated in a competitive class environment where students aimed to create the best Teaching Assistant (TA) assignment solutions within 5 minutes. Out of 155 participants, I was one of the 6 winners.**

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Examples](#examples)
- [Contributors](#contributors)

## Introduction

AssignTA is a Python-based application designed to address the complex resource allocation problem of assigning Teaching Assistants (TAs) to lab sections. Developed as part of an evolutionary computing homework project, the system employs an evolutionary algorithm to optimize TA assignments. 

The project fulfills several goals:
- **Intelligent Decision-Support:** Automates and optimizes the TA allocation process, saving hours of manual effort.
- **Optimization Objectives:** Balances factors like TA availability, preferences, time conflicts, and lab requirements.
- **Practical Implementation:** Based on real data from Northeastern University's Khoury College DS2000: Intro to Programming with Data.

This solution aims to minimize penalties for:
1. **Overallocation:** Ensuring TAs are not assigned to more labs than they can handle.
2. **Time Conflicts:** Preventing scheduling overlaps for TAs.
3. **Undersupport:** Meeting the minimum TA requirements for each section.
4. **Unwilling Assignments:** Avoiding assignments TAs explicitly prefer not to handle.
5. **Unpreferred Assignments:** Maximizing assignments to sections TAs prefer.

## Features

- **Evolutionary Algorithm:** Uses intelligent agents to generate and optimize solutions.
- **Customizable Objectives:** Balances multiple conflicting goals.
- **CSV-Based Input:** Supports real-world TA and section data.
- **Fast Execution:** Generates solutions within a 5-minute runtime.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/diya-ganesh/AssignTA.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd AssignTA
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare Input Files:**
   - `tas.csv`: Lists TAs, their preferences, and availability.
   - `sections.csv`: Details lab sections, including required and maximum TAs.

2. **Run the Main Script:**
   ```bash
   python assignta.py
   ```
3. **Analyze Results:**
   - Outputs optimized TA assignments with scores for each objective.

## Documentation

- **`assignta.py`**: Main script for running the algorithm.
- **`evo.py`**: Framework for evolutionary computation.
- **`test_assignta.py`**: Unit tests that ensure the correctness of the algorithm's objectives.

## Contributors

- **Diya Ganesh**: Developer and competition winner.

---

For more information, see the [project repository](https://github.com/diya-ganesh/AssignTA).
