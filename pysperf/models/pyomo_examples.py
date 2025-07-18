"""Example models imported from the Pyomo GDP examples library."""

import os
import logging
from os.path import join, normpath

from pysperf.model_library_registration import register_model

"""Example models imported from the Pyomo GDP examples library."""

import os
import logging
from os.path import join, normpath

from pysperf.model_library_registration import register_model

"""Example models imported from the Pyomo GDP examples library."""

# Initialize module-level variables
EXAMPLES_AVAILABLE = False


def _initialize_and_register_models():
    """Initialize Pyomo examples and register models with comprehensive error handling."""
    global EXAMPLES_AVAILABLE

    try:
        import os
        from os.path import join, normpath

        from pysperf.model_library_registration import register_model
        from pyutilib.misc import import_file
        from pyomo.common.fileutils import PYOMO_ROOT_DIR

        pyomo_gdp_examples_path = normpath(join(PYOMO_ROOT_DIR, 'examples', 'gdp'))
        EXAMPLES_AVAILABLE = os.path.exists(pyomo_gdp_examples_path)

        def _check_example_file_exists(*path):
            """Check if the example file exists in the Pyomo GDP examples directory."""
            if not EXAMPLES_AVAILABLE:
                return False
            full_path = join(pyomo_gdp_examples_path, *path)
            return os.path.exists(full_path)

        def _build_from_gdp_examples(build_name, *path):
            """Build model from GDP examples with error handling."""
            if not EXAMPLES_AVAILABLE:
                raise RuntimeError("Pyomo GDP examples are not available")

            if not _check_example_file_exists(*path):
                raise FileNotFoundError(f"Example file not found: {join(*path)}")

            model_module = import_file(join(pyomo_gdp_examples_path, *path))
            return getattr(model_module, build_name)

        def _safe_register_model(name, build_name, path_parts, **kwargs):
            """Safely register a model only if the example file exists."""
            if not EXAMPLES_AVAILABLE:
                return

            if not _check_example_file_exists(*path_parts):
                return

            try:
                build_function = _build_from_gdp_examples(build_name, *path_parts)
                register_model(name=name, build_function=build_function, **kwargs)
            except Exception:
                pass  # Silently ignore failures

        # Only register models if all dependencies are available and examples exist
        if EXAMPLES_AVAILABLE:
            _safe_register_model(
                name="8PP",
                build_name='build_eight_process_flowsheet',
                path_parts=('eight_process', 'eight_proc_model.py'),
                convex=True, bigM=100, opt_value=68.01)

            _safe_register_model(
                name="9PP",
                build_name='build_model',
                path_parts=('nine_process', 'small_process.py'),
                bigM=1e8, opt_value=-36.62)

            _safe_register_model(
                name="9PPnex",
                build_name='build_nonexclusive_model',
                path_parts=('nine_process', 'small_process.py'),
                bigM=1e8, opt_value=-88.22)

            _safe_register_model(
                name="CLAY",
                build_name='build_constrained_layout_model',
                path_parts=('constrained_layout', 'cons_layout_model.py'),
                convex=True, bigM=500, opt_value=41573)

            _safe_register_model(
                name="BS",
                build_name='build_gdp_model',
                path_parts=('small_lit', 'basic_step.py'),
                convex=True, bigM=100, opt_value=2.99)

            _safe_register_model(
                name="LeeEx1",
                build_name='build_model',
                path_parts=('small_lit', 'ex1_Lee.py'),
                convex=True, bigM=100, opt_value=1.17)

            _safe_register_model(
                name="Ex633",
                build_name='build_simple_nonconvex_gdp',
                path_parts=('small_lit', 'ex_633_trespalacios.py'),
                bigM=100, opt_value=4.46)

            _safe_register_model(
                name="HENS_ncvx",
                build_name='build_gdp_model',
                path_parts=('small_lit', 'nonconvex_HEN.py'),
                bigM=100000, opt_value=114385)

            _safe_register_model(
                name="strip8",
                build_name='build_rect_strip_packing_model',
                path_parts=('strip_packing', 'strip_packing_8rect.py'),
                bigM=None, opt_value=11)

            _safe_register_model(
                name="strip4",
                build_name='build_rect_strip_packing_model',
                path_parts=('strip_packing', 'strip_packing_concrete.py'),
                bigM=None, opt_value=11)

            _safe_register_model(
                name="rxn2",
                build_name='build_model',
                path_parts=('two_rxn_lee', 'two_rxn_model.py'),
                bigM=100, opt_value=1.01)

            _safe_register_model(
                name="stickies",
                build_name='build_model',
                path_parts=('stickies.py',),
                bigM=None, opt_value=110.3)

    except (ImportError, ModuleNotFoundError):
        # If we can't import the required modules, silently skip registering these models
        EXAMPLES_AVAILABLE = False
    except Exception:
        # For any other unexpected errors, silently skip
        EXAMPLES_AVAILABLE = False


# Try to initialize and register models when the module is imported
_initialize_and_register_models()
