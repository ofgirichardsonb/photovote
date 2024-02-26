from aiomisc import entrypoint
from memphis import Memphis

from workers.MemphisWorker import MemphisWorker
from workers.eventstore.Worker import Worker
import threading

memphis: Memphis = Memphis()


def start_worker(worker: MemphisWorker):
    with entrypoint(worker) as loop:
        loop.run_forever()


if __name__ == "__main__":
    # create additional workers here. only the aggregate name argument is different
    election_worker = Worker('Election', memphis)
    # create and start additional aggregate worker threads here
    t1 = threading.Thread(target=start_worker(election_worker), daemon=True)
    t1.start()
    # will block forever, ensure all executable code has been put into a thread
    t1.join()
    # join any remaining threads here
