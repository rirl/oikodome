#!/usr/bin/env python3
"""kios CLI entrypoint.

Small, testable CLI wrapper for the KIOS MVP.
"""

import argparse
import logging
from typing import List, Optional
__version__ = "v2"

logger = logging.getLogger(__name__)

def main(argv: Optional[List[str]] = None) -> int:
    """Main entrypoint for the kios CLI.

    Returns an exit code integer.
    """
    parser = argparse.ArgumentParser(prog="kios")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    args = parser.parse_args(argv)

    if args.version:
        # Use print for version output so it is easily captured by shells/packagers
        print("KIOS MVP v2")
        return 0
    logger.info("kios started with no actionable arguments")
    # TODO: implement actual CLI commands here
    return 0
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    raise SystemExit(main())
