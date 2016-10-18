from ledMatrix import LedMatrix
from threading import Thread
import time, sys, glob, serial


class StopWatchThread(Thread):
    def __init__(self, stopwatch_instance):
        Thread.__init__(self)
        self.stopwatch_instance = stopwatch_instance
        self.ledMatrix = self.stopwatch_instance.ledMatrix

    def run(self):

        start_time = self.stopwatch_instance.start_time
        while self.stopwatch_instance.stopwatch_running:
            elapsed_time = str(round(time.time() - start_time, 2))
            self.ledMatrix.writeToMatrix(elapsed_time)
            self.ledMatrix.sendMatrixDataToPanel()





class StopWatch():

    def __init__(self):
        self.stopwatch_running = False
        self.start_time = None
        self.ledMatrix = LedMatrix()


    def find_serial_device(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result[0]



    def startStopWatch(self, usb_port=""):
        if usb_port == "":
            usb_port = self.find_serial_device()

        self.ledMatrix.openPort(usb_port)


        #Countdown
        countdown_start_time = time.time()
        countdown_from = 5
        while ((time.time() - countdown_start_time) < countdown_from):
            self.ledMatrix.writeToMatrix(" " + str(countdown_from - int(time.time() - countdown_start_time)))
            self.ledMatrix.sendMatrixDataToPanel()
            time.sleep(0.05)


        self.stopwatch_thread = StopWatchThread(self)
        self.start_time = time.time()
        self.stopwatch_running = True
        self.stopwatch_thread.start()


    def fill_display(self):
        for i, row in enumerate(self.ledMatrix.matrix):
            for j in range(len(row)):
                row[j] = 1

        self.ledMatrix.sendMatrixDataToPanel()

    def clear_display(self):
        self.ledMatrix.initializeMatrix()
        self.ledMatrix.sendMatrixDataToPanel()


    def stopStopWatch(self):
        self.stopwatch_running = False
        elapsed_time = time.time() - self.start_time

        for i in range(20):
            self.fill_display()
            time.sleep(0.03)
            self.clear_display()
            time.sleep(0.03)


        for i in range(10):
            self.ledMatrix.writeToMatrix(str(elapsed_time))
            self.ledMatrix.sendMatrixDataToPanel()
            time.sleep(0.2)
            self.ledMatrix.writeToMatrix(str(elapsed_time))
            self.invert(self.ledMatrix.matrix)
            self.ledMatrix.sendMatrixDataToPanel()
            time.sleep(0.2)


        self.ledMatrix.closePort()
        return elapsed_time

    def invert(self, matrix):
        for row in matrix:
            for i, value in enumerate(row):
                row[i] = (value + 1) % 2





if __name__ == "__main__":
    stopwatch = StopWatch()
    stopwatch.startStopWatch()
    time.sleep(5)
    stopwatch.stopStopWatch()