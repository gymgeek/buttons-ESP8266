from threading import Thread
import time, sys, glob, pygame

screen = None
myfont = None
height = 0
width = 0
fontsize = 0

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.toggle_fullscreen()
width = screen.get_width()
height = screen.get_height()
fontsize = int((width / 8) * 2.5)
myfont = pygame.font.SysFont(None, int(fontsize))

class StopWatchThread(Thread):
    def __init__(self, stopwatch_instance):
        Thread.__init__(self)
        self.stopwatch_instance = stopwatch_instance


    def run(self):

        start_time = self.stopwatch_instance.start_time
        while self.stopwatch_instance.stopwatch_running:
            currtime = time.time() - start_time


            milisec = int((currtime % 1) * 100)
            sec = int(currtime) % 60
            text = "00:" + ("0" + str(sec))[-2:] + ":" + ("0" + str(milisec))[-2:]
            screen.fill((0, 0, 0))
            label = myfont.render(text, False, (255, 255, 0))
            screen.blit(label, (int(fontsize / 4), int((height / 5))))
            pygame.display.flip()
            pygame.event.clear()







class StopWatch():

    def __init__(self):
        self.stopwatch_running = False
        self.start_time = 0







    def startStopWatch(self, usb_port=""):
        #Countdown
        countdown_start_time = time.time()
        countdown_from = 5
        while ((time.time() - countdown_start_time) < countdown_from):
            color_step = int(255/countdown_from)
            text = " " + str(countdown_from - int(time.time() - countdown_start_time))
            screen.fill((0, 0, 0))
            r = int(text)*color_step
            g = 255-int(text)*color_step
            label = myfont.render(text, False, (r, g, 0))
            screen.blit(label, (int(width / 3), int((height / 5))))
            pygame.display.flip()
            pygame.event.clear()
            time.sleep(0.05)


        self.stopwatch_thread = StopWatchThread(self)
        self.start_time = time.time()
        self.stopwatch_running = True
        self.stopwatch_thread.start()




    def stopStopWatch(self):
        self.stopwatch_running = False
        elapsed_time = time.time() - self.start_time
        return elapsed_time






if __name__ == "__main__":
    stopwatch = StopWatch()
    stopwatch.startStopWatch()
    time.sleep(5)
    stopwatch.stopStopWatch()
