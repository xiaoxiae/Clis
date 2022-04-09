import gphoto2 as gp
import os
import sys
from time import sleep

def silence_others_wrapper(f):
    def inner(self, *args, **kwargs):
        if self.silence_others:
            os.dup2(self.save[0], 1)
            os.dup2(self.save[1], 2)
            # close the temporary fds
            os.close(self.null_fds[0])
            os.close(self.null_fds[1])

        result = f(self, *args, **kwargs)

        if self.silence_others:
            self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
            self.save = os.dup(1), os.dup(2)

            # put /dev/null fds on 1 and 2
            os.dup2(self.null_fds[0], 1)
            os.dup2(self.null_fds[1], 2)

        return result

    return inner


class Printer:
    """A class for script printing."""

    def silentPrint(self, *args, **kwargs):
        """A dummy function for suppressed printer class."""
        return

    def __init__(self, name: str = "", silence_others=False):
        self.name = name.strip().lower().capitalize()
        self.print_function = self.silentPrint if not name else print
        self.silence_others = silence_others

        if silence_others:
            self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
            self.save = os.dup(1), os.dup(2)

    @silence_others_wrapper
    def begin(self, *args, dots=True):
        self.print_function(f"{self.name} |", *args, end="", flush=True)

        if dots:
            self.print_function("...", end="", flush=True)

    @silence_others_wrapper
    def end(self, *args, **kwargs):
        self.print_function("", *args, **kwargs, flush=True)

    @silence_others_wrapper
    def mid(self, *args, dots=True):
        self.print_function("", *args, end="", flush=True)

        if dots:
            self.print_function("...", end="", flush=True)

    @silence_others_wrapper
    def full(self, *args, **kwargs):
        self.print_function(f"{self.name}:", *args, **kwargs, flush=True)


def initialize_camera(printer=Printer()):
    """Connect to the camera."""
    camera = gp.Camera()

    printer.begin("connecting to the camera")
    while True:
        try:
            camera.init()
        except gp.GPhoto2Error as ex:
            # this is not too pretty, but works...
            try:
                if ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                    sleep(2)
                    continue
                raise
            except KeyboardInterrupt:
                printer.end("interrupted by the user, quitting.")
                quit()
        break
    printer.end("connected.")

    return camera
