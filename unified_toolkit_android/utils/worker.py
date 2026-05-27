"""
Background threading helper.
Runs a function in a separate thread, then calls callback(result) on the
Kivy main thread using Clock.schedule_once.
"""

import threading
from kivy.clock import Clock


def run_in_thread(func, *args, on_result=None, on_progress=None, **kwargs):
    """
    func       — the blocking function to run
    *args      — positional args to pass
    on_result  — callback(output_str) called on main thread when done
    on_progress— callback(line_str) called on main thread for each output line
                 (func must accept a progress_cb keyword arg)
    """
    def _thread_body():
        try:
            if on_progress:
                # func should call progress_cb(line) for each line
                output = func(*args, progress_cb=on_progress, **kwargs)
            else:
                output = func(*args, **kwargs)
        except Exception as e:
            output = f"[ERROR] {type(e).__name__}: {e}"

        if on_result:
            Clock.schedule_once(lambda dt: on_result(output), 0)

    t = threading.Thread(target=_thread_body, daemon=True)
    t.start()
    return t
