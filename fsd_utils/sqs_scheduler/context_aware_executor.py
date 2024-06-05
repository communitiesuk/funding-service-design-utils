from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context


class ContextAwareExecutor:
    """This Executor copy current flask application context and then inherit the
    flask application context for each executor thread then those threads will
    have the ability to use flask resources with its own flask context."""

    def __init__(self, max_workers, thread_name_prefix, flask_app):
        """Initialize Threadpool executor and ContextAwareExecutor :max_workers
        number of workers for the thread pool :thread_name_prefix prefix of the
        thread pool name :flask_app original flask application context."""
        self.executor = ThreadPoolExecutor(
            max_workers=max_workers, thread_name_prefix=thread_name_prefix
        )
        self.flask_app = flask_app

    def queue_size(self):
        """Get queue size of the Thread pool."""
        return self.executor._work_queue.qsize()

    def submit(self, fn, *args, **kwargs):
        """Submit executor to the thread pool."""
        ctx = copy_context()
        future = self.executor.submit(ctx.run, self.wrap_function(fn), *args, **kwargs)
        return future

    def wrap_function(self, fn):
        """Wrap the function with copied application context."""

        def wrapped(*args, **kwargs):
            with self.flask_app.app_context():
                return fn(*args, **kwargs)

        return wrapped
