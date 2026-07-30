"""Bootstrap acceptance tests using only the Python standard library."""

from __future__ import annotations

import contextlib
import io
import unittest

import geoprospect
from geoprospect.cli import main


class BootstrapTests(unittest.TestCase):
    """Verify the package can be imported and the minimal CLI can run."""

    def test_package_import_exposes_version(self) -> None:
        self.assertTrue(geoprospect.__version__)

    def test_status_command(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = main(["status"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().strip(), "Stage 0 active; Stage 1 blocked.")


if __name__ == "__main__":
    unittest.main()
