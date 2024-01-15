from uuid import UUID
from sched import scheduler
from time import sleep


# run this in a thread to keep scheduler going throughout lifetime of app
def schedule_runner(schedular_inst: scheduler):
    """Runs the scheduler.

    Args:
        schedular_inst (scheduler): Instance of scheduler.
    """
    while True:
        if schedular_inst.queue:
            schedular_inst.run()
        sleep(0.1)


# use this function to translate an item id str to uuid
def id_str_to_uuid(item_id: str) -> UUID:
    """_summary_

    Args:
        item_id (str): The item id.

    Returns:
        UUID: The item id as a UUID.
    """
    return UUID(item_id)
