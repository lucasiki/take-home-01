from time import sleep
from threading import Thread
from datetime import timedelta
from time import time
from .minute_task import run_minute_task
from .hour_task import run_hour_task
import logging

def init_event_loop_thread(object):
    Thread(target=event_loop, args=[object], daemon=True).start()
    
def event_loop(object):
    time_dilatation = 0
    while True:
        time_before = time()
        event_loop_body(object, object.TIME_STEP+time_dilatation)
        logging.info(object.DATETIME.strftime('%m/%d/%Y %H:%M:%S'))
        time_dilatation = 0
        time_after = time()
        time_dilatation = time_after - time_before
        sleep(1)
        
def event_loop_body(object, increment=0, test=False):
    if not object.PAUSE:
        object.time_before = object.DATETIME
        object.DATETIME += timedelta(seconds=increment)
        if not test:
            run_minute_task(object.time_before, object.DATETIME, object)
            run_hour_task(object.time_before, object.DATETIME, object)
    