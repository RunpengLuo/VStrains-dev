#!/usr/bin/env python3

import argparse
import sys
import os
import platform
import numpy
import logging
import time
from datetime import date

from utils import (
    vsAware_SPAdes
)

__author__ = "Runpeng Luo"
__copyright__ = ""
__credits__ = ["Runpeng Luo", "Yu Lin"]
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Runpeng Luo"
__email__ = ""
__status__ = ""


def run(args, logger):
    numpy.seterr(all="raise")
    RUNNER = {
        "spades": vsAware_SPAdes.run,
    }
    RUNNER[args.assembler](args, logger)


def main():
    parser = argparse.ArgumentParser(
        prog="vsAware",
        description="""Construct full-length viral strains under de novo approach 
        from contigs and assembly graph, currently supports SPAdes""",
    )

    parser.add_argument(
        "-a",
        "--assembler",
        dest="assembler",
        type=str,
        required=True,
        choices=["spades"],
        help="name of the assembler used. [spades]",
    )

    parser.add_argument(
        "-g",
        "--graph",
        dest="gfa_file",
        type=str,
        required=True,
        help="path to the assembly graph, (.gfa format)",
    )

    parser.add_argument(
        "-p",
        "--path",
        dest="path_file",
        type=str,
        required=False,
        help="contig file from SPAdes (.paths format), only required for SPAdes. e.g., contigs.paths",
    )

    parser.add_argument(
        "-mc",
        "--minimum_coverage",
        dest="min_cov",
        default=None,
        type=int,
        help=(
            "minimum node coverage cutoff, also apply to filter the low-coverage strain [default: auto]"
        ),
    )

    parser.add_argument(
        "-ml",
        "--minimum_contig_length",
        dest="min_len",
        default=None,
        type=int,
        help=("minimum initial contig length for strains [default: 250]"),
    )

    parser.add_argument(
        "-r",
        "--reference_fa",
        dest="ref_file",
        type=str,
        help=argparse.SUPPRESS,
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        dest="output_dir",
        default="acc/",
        type=str,
        help="path to the output directory [default: acc/]",
    )

    parser.add_argument(
        "-d",
        "--dev_mode",
        dest="dev",
        action="store_true",
        default=False,
        help=argparse.SUPPRESS,
    )

    args = parser.parse_args()

    # parsing arguments, sanity check
    if (not args.gfa_file) or (not os.path.exists(args.gfa_file)):
        print("\nPath to the assembly graph is required, (.gfa format)")
        print("Please ensure the path is correct")
        print("\nExiting...\n")
        sys.exit(1)

    args.assembler = args.assembler.lower()

    if args.assembler.lower() == "spades":
        if (not args.path_file) or (not os.path.exists(args.path_file)):
            print(
                "\nPath to Contig file from SPAdes (.paths format) is required for SPAdes assmbler option. e.g., contigs.paths"
            )
            print("\nExiting...\n")
            sys.exit(1)
    else:
        print("\nPlease make sure to provide the correct assembler type (SPAdes).")
        print("\nExiting...\n")
        sys.exit(1)

    if args.min_len != None:
        if args.min_len < 0:
            print(
                "\nPlease make sure to provide the correct option (invalid value for min_len or min_cov)."
            )
            print("\nExiting...\n")
            sys.exit(1)
    else:
        args.min_len = 250

    if args.min_cov != None:
        if args.min_cov < 0:
            print(
                "\nPlease make sure to provide the correct option (invalid value for min_len or min_cov)."
            )
            print("\nExiting...\n")
            sys.exit(1)

    if args.output_dir[-1] == "/":
        args.output_dir = args.output_dir[:-1]

    # initialize output directory
    os.makedirs(args.output_dir, exist_ok=True)
    try:
        os.makedirs(args.output_dir + "/gfa/")
        os.makedirs(args.output_dir + "/tmp/")
        os.makedirs(args.output_dir + "/paf/")
    except OSError as _:
        print("\nCurrent output directory is not empty")
        print("Please empty/re-create the output directory: " + str(args.output_dir))
        print("\nExiting...\n")
        sys.exit(1)

    if os.path.exists(args.output_dir + "/vsaware.log"):
        os.remove(args.output + "/vsaware.log")

    # Setup logger
    # -----------------------
    logger = logging.getLogger("VSAware %s" % __version__)
    logger.setLevel(logging.DEBUG if args.dev else logging.INFO)

    consoleHeader = logging.StreamHandler()
    consoleHeader.setLevel(logging.INFO)
    consoleHeader.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(consoleHeader)

    fileHandler = logging.FileHandler(args.output_dir + "/vsaware.log")
    fileHandler.setLevel(logging.DEBUG if args.dev else logging.INFO)
    fileHandler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(fileHandler)

    logger.info("Welcome to vsAware!")
    logger.info(
        "vsAware is a strain-aware assembly tools, which constructs full-length "
    )
    logger.info("virus strain with aid from de Bruijn assembly graph and contigs.")
    logger.info("")
    logger.info("System information:")
    try:
        logger.info("  VSAware version: " + str(__version__).strip())
        logger.info("  Python version: " + ".".join(map(str, sys.version_info[0:3])))
        logger.info("  OS: " + platform.platform())
    except Exception:
        logger.info("  Problem occurred when getting system information")

    logger.info("")
    start_time = time.time()

    logger.info("Input arguments:")
    logger.info("Assembly type: " + args.assembler)
    logger.info("Assembly graph file: " + args.gfa_file)
    if args.assembler == 'spades':
        logger.info("Contig paths file: " + args.path_file)
    logger.info("Output directory: " + os.path.abspath(args.output_dir))
    if args.dev:
        logger.info("*DEBUG MODE is turned ON")
    logger.info("\n\n")
    logger.info(
        "======= vsAware pipeline started. Log can be found here: "
        + os.path.abspath(args.output_dir)
        + "/vsaware.log\n"
    )

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    consoleHeader.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # all good
    run(args, logger)

    elapsed = time.time() - start_time

    consoleHeader.setFormatter(logging.Formatter("%(message)s"))
    fileHandler.setFormatter(logging.Formatter("%(message)s"))

    logger.info("")
    logger.info(
        "Result is stored in {0}/strain.fasta".format(os.path.abspath(args.output_dir))
    )
    logger.info("Finished: {0}".format(date.today().strftime("%B %d, %Y")))
    logger.info("Elapsed time: {0}".format(elapsed))
    logger.info("Exiting...")
    logger.removeHandler(fileHandler)
    logger.removeHandler(consoleHeader)

    return 0


if __name__ == "__main__":
    main()
