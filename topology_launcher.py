from topology import timer_thread

class TopologyLauncher:
    timerThread = None
    def __init__(self):
        None

    def startTimerThread(self):
        if self.timerThread is None:
            self.timerThread = timer_thread.TimerThread()

        self.timerThread.start()

    def stopTimerThread(self):
        print('<TSN switch> Thread: TimerThread interrupted <TSN switch>')
        if self.timerThread is not None and self.timerThread.is_alive():
            self.timerThread.stop()
