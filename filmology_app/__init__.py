import os

# Expose the example package under the ``filmology_app`` name so that tests can
# import it without needing to modify ``PYTHONPATH``.
_example_pkg = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', 'examples', 'filmology_app')
)
if os.path.isdir(_example_pkg) and _example_pkg not in __path__:
    __path__.append(_example_pkg)
