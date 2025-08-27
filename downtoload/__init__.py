# Ensure tasks are registered with Huey
from . import tasks

"""
Huey must know about all the tasks before consumer starts, if not import tasks, then the decorator never runs
keeping it hear make sure that whenever downtoload package is imported, tasks is registered
"""