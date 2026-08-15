import os
import subprocess
import sys
import tempfile
import unittest
import venv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from relaypack import render_route


class RelaypackTests(unittest.TestCase):
    def test_known_route(self):
        self.assertEqual(
            render_route("alpha"),
            "route alpha -> https://api.example.test/v1",
        )

    def test_unknown_route(self):
        with self.assertRaises(KeyError):
            render_route("missing")


class PublishedWheelTests(unittest.TestCase):
    def test_installed_wheel_contains_and_uses_route_data(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            wheel_directory = temporary_path / "wheelhouse"
            wheel_directory.mkdir()

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "wheel",
                    "--no-deps",
                    "--no-build-isolation",
                    "--wheel-dir",
                    str(wheel_directory),
                    str(ROOT),
                ],
                cwd=temporary_path,
                check=True,
                capture_output=True,
                text=True,
            )

            wheels = list(wheel_directory.glob("relaypack_demo-*.whl"))
            self.assertEqual(len(wheels), 1)
            wheel = wheels[0]
            with zipfile.ZipFile(wheel) as archive:
                self.assertIn("relaypack/routes.json", archive.namelist())

            environment_directory = temporary_path / "installed"
            venv.EnvBuilder(with_pip=True).create(environment_directory)
            scripts_directory = environment_directory / (
                "Scripts" if os.name == "nt" else "bin"
            )
            python = scripts_directory / (
                "python.exe" if os.name == "nt" else "python"
            )
            subprocess.run(
                [
                    str(python),
                    "-m",
                    "pip",
                    "install",
                    "--no-deps",
                    "--no-index",
                    str(wheel),
                ],
                cwd=temporary_path,
                check=True,
                capture_output=True,
                text=True,
            )

            clean_environment = os.environ.copy()
            clean_environment.pop("PYTHONPATH", None)
            api = subprocess.run(
                [
                    str(python),
                    "-c",
                    "import relaypack; print(relaypack.render_route('alpha'))",
                ],
                cwd=temporary_path,
                env=clean_environment,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                api.stdout.strip(),
                "route alpha -> https://api.example.test/v1",
            )

            unknown_api = subprocess.run(
                [
                    str(python),
                    "-c",
                    "import relaypack; relaypack.render_route('missing')",
                ],
                cwd=temporary_path,
                env=clean_environment,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(unknown_api.returncode, 0)
            self.assertIn("KeyError: 'missing'", unknown_api.stderr)

            relaypack = scripts_directory / (
                "relaypack.exe" if os.name == "nt" else "relaypack"
            )
            cli = subprocess.run(
                [str(relaypack), "alpha"],
                cwd=temporary_path,
                env=clean_environment,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                cli.stdout.strip(),
                "route alpha -> https://api.example.test/v1",
            )

            unknown = subprocess.run(
                [str(relaypack), "missing"],
                cwd=temporary_path,
                env=clean_environment,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(unknown.returncode, 0)
            self.assertIn("unknown route: missing", unknown.stderr)


if __name__ == "__main__":
    unittest.main()
