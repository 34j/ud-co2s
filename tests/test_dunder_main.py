import subprocess
import sys


def test_can_run_as_python_module():
    """Run the CLI as a Python module."""
    result = subprocess.run(
        [sys.executable, "-m", "ud_co2s", "--help"],  # noqa S603,S607
        check=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert b"ud-co2s [OPTIONS]" in result.stdout
