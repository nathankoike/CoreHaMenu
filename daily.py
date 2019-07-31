"""
Proj: CoreHaMenu

Auth: Nate Koike

Desc: run a function once per day
"""
# needed to grab date information
import datetime
# needed to wait for a fulll 24 hours
import time

""" call a function and get all the arguments passed to it in a tuple """
def start(fn, args):
    fn(args)
    day = datetime.date.today()

    # infinite loop
    while True:
        # see if the day changed
        if not day == datetime.date.today():
            day = datetime.date.today() # update the date

            # run the function once
            fn(args)

            # wait almost a day, the code will self correct to always be at a
            # new day in this way without taking too much time on the cpu by
            # constantly executing an operation
            time.sleep(86399)
