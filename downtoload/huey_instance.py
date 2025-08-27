from huey import SqliteHuey
huey = SqliteHuey(filename='huey.sqlite3')

"""
creats a huey instance, backend by SQLite (job ququq database)
keeps the track of background jobs

Running command
python -m huey.bin.huey_consumer -v downtoload.huey_instance.huey
it create and looks for huey.sqlite3 for tasks to run
"""