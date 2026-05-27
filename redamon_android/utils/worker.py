"""utils/worker.py — Thread-safe background task runner."""
import threading, queue
from kivy.clock import Clock


def run_tool(gen_fn, args=(), on_line=None, on_done=None):
    """
    Run a generator function in a daemon thread.
    Each yielded string is delivered to on_line() on the main thread.
    on_done() is called when the generator is exhausted.
    """
    q = queue.Queue()

    def _worker():
        try:
            for line in gen_fn(*args):
                q.put(('line', line))
        except Exception as exc:
            q.put(('line', f'[ERR] {exc}\n'))
        finally:
            q.put(('done', None))

    def _poll(dt):
        try:
            while True:
                kind, val = q.get_nowait()
                if kind == 'done':
                    if on_done:
                        on_done()
                    return
                if on_line:
                    on_line(val)
        except queue.Empty:
            pass
        Clock.schedule_once(_poll, 0.05)

    threading.Thread(target=_worker, daemon=True).start()
    Clock.schedule_once(_poll, 0.05)


def run_parallel(tasks, on_line=None, on_all_done=None):
    """
    Run multiple (gen_fn, args, label) tuples in parallel.
    on_line(label, line) called for each output line.
    on_all_done() called when ALL tasks finish.
    """
    remaining = [len(tasks)]
    lock = threading.Lock()

    def _done_one():
        with lock:
            remaining[0] -= 1
            if remaining[0] == 0 and on_all_done:
                Clock.schedule_once(lambda dt: on_all_done(), 0)

    for gen_fn, args, label in tasks:
        def _make(fn, a, lbl):
            def _line(l):
                if on_line:
                    on_line(lbl, l)
            run_tool(fn, a, on_line=_line, on_done=_done_one)
        _make(gen_fn, args, label)
