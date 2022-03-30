import sys
import time

class Spinner:

    def __init__(self, initial=False):
        self.showing = initial

    @staticmethod
    def spinning_cursor():
        while True:
            for cursor in '|/-\\':
                yield cursor

    def show(self):
        spinner = self.spinning_cursor()
        while self.showing:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.2)
            sys.stdout.write('\b')
    
    def stop(self):
        self.showing=False

spinner = Spinner(True)
spinner.show()
spinner.stop()