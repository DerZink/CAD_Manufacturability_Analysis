from timeit import default_timer as timer
import time
import uuid
from PySide2 import QtCore, QtGui
from PySide2.QtCore import Slot, Signal

# to be used for genrating part's id


def generateid():
    id_gen = str(uuid.uuid4())
    return id_gen


# to be used for genrating part's creation


def generatedate():
    return time.time()


def converdate(t):
    return str(time.ctime(t))


class QtWaitClass(QtCore.QObject):
    timeOutSignal = Signal()

    def __init__(self, maxTime):
        super().__init__()
        self.MaxTime = maxTime
        self.processStatus = True

        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.waitFunction)

    def waitFunction(self):
        self.startTime = timer()
        while self.processStatus == True:
            time.sleep(1)
            waitEnd = timer()
            if waitEnd - self.startTime > self.MaxTime:
                self.timeOutSignal.emit()
                self.processStatus = False
        self.thread.quit()

    @Slot(object)
    def statusSlot(self, status):
        self.processStatus = status
        self.thread.quit()


if __name__ == "__main__":
    for i in range(1):
        print(type(generateid()))
        # generateid()
