import gphoto2 as gp
from time import sleep

class Printer:
    """A class for script printing."""

    def silentPrint(self, *args, **kwargs):
        """A dummy function for suppressed printer class."""
        return

    def __init__(self, name: str = ""):
        self.name = name.strip().lower().capitalize()
        self.print_function = self.silentPrint if not name else print

    def begin(self, *args):
        self.print_function(f"{self.name}:", *args, end="", flush=True)
        self.print_function("...", end="", flush=True)

    def end(self, *args, **kwargs):
        self.print_function("", *args, **kwargs, flush=True)

    def mid(self, *args):
        self.print_function("", *args, end="", flush=True)
        self.print_function("...", end="", flush=True)

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
