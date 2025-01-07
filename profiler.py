"""
profiler.py
A profiler class that demonstrates the use of decorators to support code profiling
DS3500: Advanced Programming with Data (Prof. Rachlin)
"""
from collections import defaultdict
import time



def profile(f):
    """ Convenience function to make decorator tags simpler:
        e.g. @profile instead of @Profiler.profile """
    return Profiler.profile(f)

class Profiler:
    """ A code profiling class.  Keeps track of function calls and running time. """

    calls = defaultdict(int)  # default = 0
    time = defaultdict(float)  # default = 0.0

    @staticmethod
    def _add(function_name, sec):
        """ Add 1 call and <sec> time to named function tracking """
        Profiler.calls[function_name] += 1
        Profiler.time[function_name] += sec

    @staticmethod
    def profile(f):
        """ The profiling decorator """
        def wrapper(*args, **kwargs):
            function_name = str(f).split()[1]
            start = time.time_ns()
            val = f(*args, **kwargs)
            sec = (time.time_ns() - start) / 10**9
            Profiler._add(function_name, sec)
            return val
        return wrapper

    @staticmethod
    def report():
        """ Summarize # calls, total runtime, and time/call for each function """
        report_str = ""
        report_str += "Function              Calls     TotSec   Sec/Call"
        for name, num in Profiler.calls.items():
            sec = Profiler.time[name]
            report_str += f'\n{name:20s} {num:6d} {sec:10.3f} {sec / num:10.3f}'

        return report_str
