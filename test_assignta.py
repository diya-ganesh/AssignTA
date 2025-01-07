"""
test_assignta.py: Unit tests for the functions defined in assignta.py.
                  The tests ensure each objective function correctly calculates penalties for a TA assignment solution.
Author: Diya Ganesh
"""

import pytest
import numpy as np
import assignta

# Load the test data and convert to numpy arrays
test_data1 = np.loadtxt("tests/test1.csv", delimiter=",")
test_data2 = np.loadtxt("tests/test2.csv", delimiter=",")
test_data3 = np.loadtxt("tests/test3.csv", delimiter=",")

# Expected evaluation scores
eval_scores = np.array([
    [37, 41, 23],  # Overallocation
    [8, 5, 2],     # Conflicts
    [1, 0, 7],     # Undersupport
    [53, 58, 43],  # Unwilling
    [15, 19, 10]   # Unpreferred
])

# Unit tests for each objective function
def test_overallocation():
    """ Test overallocation objective function. """
    for i, test_data in enumerate([test_data1, test_data2, test_data3]):
        result = assignta.overallocation(test_data)
        expected = eval_scores[0, i]
        assert result == expected, f"Expected overallocation penalty {expected}, got {result}"

def test_conflicts():
    """ Test conflicts objective function. """
    for i, test_data in enumerate([test_data1, test_data2, test_data3]):
        result = assignta.conflicts(test_data)
        expected = eval_scores[1, i]
        assert result == expected, f"Expected conflicts penalty {expected}, got {result}"

def test_undersupport():
    """ Test undersupport objective function. """
    for i, test_data in enumerate([test_data1, test_data2, test_data3]):
        result = assignta.undersupport(test_data)
        expected = eval_scores[2, i]
        assert result == expected, f"Expected undersupport penalty {expected}, got {result}"

def test_unwilling():
    """ Test unwilling objective function. """
    for i, test_data in enumerate([test_data1, test_data2, test_data3]):
        result = assignta.unwilling(test_data)
        expected = eval_scores[3, i]
        assert result == expected, f"Expected unwilling penalty {expected}, got {result}"

def test_unpreferred():
    """ Test unpreferred objective function. """
    for i, test_data in enumerate([test_data1, test_data2, test_data3]):
        result = assignta.unpreferred(test_data)
        expected = eval_scores[4, i]
        assert result == expected, f"Expected unpreferred penalty {expected}, got {result}"

# Run the tests
if __name__ == "__main__":
    pytest.main()
