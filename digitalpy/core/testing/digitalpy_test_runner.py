from multiprocessing import Process
from digitalpy.core.main.DigitalPy import DigitalPy


def start_digitalpy_application(app: type[DigitalPy]):
    """Starts the DigitalPy application."""
    app().start(True)


def stop_digitalpy_application(app: Process):
    """Stops the DigitalPy application."""
    app.join(3)
    if app.is_alive():
        app.terminate()
        app.join()
