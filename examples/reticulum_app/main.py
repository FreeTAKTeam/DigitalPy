"""
Main module for a DigitalPy application.

This script defines the main class for a DigitalPy application,
which serves as the entry point for the application.
"""

from digitalpy.core.main.DigitalPy import DigitalPy


class DigitalPyApp(DigitalPy):
    """
    Main class for the DigitalPy application.

    This class inherits from DigitalPy and initializes the application
    with the required configuration and setup.
    """

    def __init__(self):
        """
        Initialize the DigitalPyApp instance.

        This constructor initializes the base DigitalPy class and
        configures the application by calling the _initialize_app_configuration method.
        """
        super().__init__()
        self._initialize_app_configuration()

if __name__ == "__main__":
    # Entry point for the DigitalPy application.
    #
    # This block ensures that the application starts only when executed as a script.
    DigitalPyApp().start()
