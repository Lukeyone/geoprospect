"""Command-line entry point for GeoProspect Stage 0."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from geoprospect import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build the minimal Stage 0 command-line parser."""
    parser = argparse.ArgumentParser(
        prog="geoprospect",
        description="GeoProspect Stage 0 feasibility-audit tooling.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser(
        "status",
        help="Print the current authorised project stage.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the GeoProspect command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "status":
        print("Stage 0 active; Stage 1 blocked.")
        return 0

    parser.print_help()
    return 0
