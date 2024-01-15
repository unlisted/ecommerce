from threading import Thread
from common.global_sched import Schedular
from common.utils import schedule_runner

if __name__ == "__main__":
    # start the scheduler
    t = Thread(target=schedule_runner, args=[Schedular])
    t.start()
    t.join()