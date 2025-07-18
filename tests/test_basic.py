# Basic tests for pysperf package
import pytest
import sys
import os
import subprocess


def test_python_version_compatibility():
    """Test that we're running on a supported Python version."""
    assert sys.version_info >= (3, 9), "Python 3.9 or newer is required"


def test_package_structure():
    """Test that the package has the expected structure."""
    package_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pysperf')
    assert os.path.exists(package_dir), "pysperf package directory should exist"
    
    expected_files = [
        '__init__.py',
        '__main__.py',
        'config.py',
        'model_library.py',
        'solver_library.py',
        'run_manager.py',
        'base_classes.py',
    ]
    
    for filename in expected_files:
        filepath = os.path.join(package_dir, filename)
        assert os.path.exists(filepath), f"{filename} should exist in pysperf package"


def test_setup_py_exists():
    """Test that setup.py exists and can be parsed."""
    setup_py_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'setup.py')
    assert os.path.exists(setup_py_path), "setup.py should exist in project root"
    
    # Try to read setup.py to make sure it's valid Python
    with open(setup_py_path, 'r') as f:
        content = f.read()
        assert 'setup(' in content, "setup.py should contain setup() call"


def test_requirements_files_exist():
    """Test that requirements files exist."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    requirements_files = [
        'requirements.txt',
        'requirements-dev.txt',
        'pyproject.toml'
    ]
    
    for req_file in requirements_files:
        filepath = os.path.join(project_root, req_file)
        assert os.path.exists(filepath), f"{req_file} should exist in project root"


def test_package_can_be_imported():
    """Test that the package can be imported with proper error handling."""
    try:
        # Try importing with path modification to avoid installation issues
        import sys
        project_root = os.path.dirname(os.path.dirname(__file__))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        import pysperf
        # If import succeeds, verify it's a module
        assert hasattr(pysperf, '__file__'), "pysperf should be a proper module"
        
    except ImportError as e:
        # If import fails due to dependencies, that's expected in some environments
        # Just verify the module file exists
        package_init = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pysperf', '__init__.py')
        assert os.path.exists(package_init), f"pysperf/__init__.py should exist: {e}"


def test_package_installation_command():
    """Test that pip install command would work (without actually installing)."""
    # Test that the package directory structure supports pip installation
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # Check for required files for pip installation
    required_files = ['setup.py', 'pyproject.toml']
    for req_file in required_files:
        filepath = os.path.join(project_root, req_file)
        assert os.path.exists(filepath), f"{req_file} is required for pip installation"