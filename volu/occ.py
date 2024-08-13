from concurrent.futures import ThreadPoolExecutor
import queue
import threading

class IoTask:
    def execute(self):
        print("Executing I/O task")

class IoTaskPool:
    def __init__(self, max_workers=5):
        self.tasks = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.Lock()

    def add_task(self, task):
        with self.lock:
            self.tasks.put(task)
            self.executor.submit(self._worker)

    def _worker(self):
        while True:
            try:
                task = self.tasks.get(timeout=0.1)
                task.execute()
                self.tasks.task_done()
            except queue.Empty:
                break

# Usage
pool = IoTaskPool(max_workers=5)

# Adding tasks
task = IoTask()
pool.add_task(task)

# The worker will automatically execute the task
