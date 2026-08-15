import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WheelTests(unittest.TestCase):
    def test_installed_console_command_loads_packaged_routes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            wheel_directory = temporary_path / "wheel"
            virtual_environment = temporary_path / "venv"
            outside_checkout = temporary_path / "outside-checkout"
            wheel_directory.mkdir()
            outside_checkout.mkdir()

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "wheel",
                    str(ROOT),
                    "--no-deps",
                    "--no-build-isolation",
                    "--wheel-dir",
                    str(wheel_directory),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            wheel = next(wheel_directory.glob("relaypack_demo-*.whl"))

            subprocess.run(
                [sys.executable, "-m", "venv", str(virtual_environment)],
                check=True,
                capture_output=True,
                text=True,
            )
            scripts_directory = virtual_environment / (
                "Scripts" if os.name == "nt" else "bin"
            )
            virtual_python = scripts_directory / (
                "python.exe" if os.name == "nt" else "python"
            )
            relaypack = scripts_directory / (
                "relaypack.exe" if os.name == "nt" else "relaypack"
            )
            subprocess.run(
                [str(virtual_python), "-m", "pip", "install", "--no-deps", str(wheel)],
                check=True,
                capture_output=True,
                text=True,
            )

            completed = subprocess.run(
                [str(relaypack), "alpha"],
                cwd=outside_checkout,
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(
                completed.stdout,
                "route alpha -> https://api.example.test/v1\n",
            )


if __name__ == "__main__":
    unittest.main()
