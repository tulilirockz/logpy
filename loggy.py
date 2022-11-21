#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from typing import Final, Mapping, Union, Dict, Optional
from pathlib import Path
import os
import sys
import logging
import configparser
from configparser import RawConfigParser


def _arg_parser() -> ArgumentParser:
    _parser: Final[ArgumentParser] = ArgumentParser(description="Logging for userspace programs", prog="Loggy")

    _parser.add_argument('message',
                         type=str,
                         nargs="+",
                         help="Message that will be logged to (FILE)")

    _parser.add_argument('-c', '--context',
                         type=str,
                         nargs="+",
                         help="Context for the message")

    _parser.add_argument('-l', '--level',
                         type=str,
                         default="INFO",
                         help="Logging level")

    _parser.add_argument('--log-file',
                         type=str,
                         help="The file where everything will be logged to")

    _parser.add_argument('--config-file',
                         type=str,
                         help="Path for the config file")
    return _parser


def gen_default_cfg() -> Dict:
    def_cfg: RawConfigParser = configparser.RawConfigParser()

    def_cfg["loggy"] = {}
    def_cfg["loggy"]["LOG_PATH"] = "\"\""
    def_cfg["loggy"]["LOG_FORMAT"] = '[%(asctime)s] [%(levelname)s] - %(msg)s'
    def_cfg["loggy"]["LOG_LEVEL"] = "CRITICAL"
    if os.name == "nt":
        APPDATA = os.environ["APPDATA"]
        def_cfg["loggy"]["LOG_PATH"] = f"{APPDATA}\\loggy\\loggy.log"
        del APPDATA
    elif os.name == "posix":
        def_cfg["loggy"]["LOG_PATH"] = f"{Path.home()}/.local/share/loggy/logfile.log"
    else:
        raise NotImplementedError("Operating system not supported")

    return def_cfg


def _gen_cfg_file(cfg_path: Path) -> Path:
    try:
        cfg_path.parents[0].mkdir(exist_ok=True)
        cfg_path.touch(exist_ok=True)
    except OSError:
        print("Error trying to create config folder/file at ", cfg_path, file=sys.stderr)
        raise

    default_cfg: RawConfigParser = gen_default_cfg()

    if os.stat(cfg_path).st_size == 0:
        try:
            with open(cfg_path, "w") as cfg_file:
                default_cfg.write(cfg_file)
                print("Wrote default config successfully to", cfg_path)
        except OSError:
            print("Error while trying to write config to", cfg_path, file=sys.stderr)
            raise
    return cfg_path


def transform_verbosity(verbosity: Final[Union[str, int]]) -> int:
    """Transforms logging verbosity levels from strings to valid integers"""
    LEVELS: Mapping[str, int] = {
        'NOTSET': 0, 'DEBUG': 10,
        'INFO': 20, 'WARNING': 30,
        'ERROR': 40, 'CRITICAL': 50
    }
    return LEVELS.get(verbosity.upper(), 50) if (type(verbosity) is str) else int(verbosity)


def main() -> int:
    ARGS: Final[Namespace] = _arg_parser().parse_args()
    CFG: ConfigParser = configparser.RawConfigParser()
    CFG.read(_gen_cfg_file(Path(ARGS.config_file)))

    LOG_PATH: Final[Path] = Path(ARGS.log_file) if ARGS.log_file else Path(CFG["loggy"]["log_path"])

    try:
        LOG_PATH.parents[0].mkdir(exist_ok=True)
        LOG_PATH.touch(exist_ok=True)
    except OSError:
        print("Error trying to create log folder/file at", log_path, file=sys.stderr)
        raise

    logging.basicConfig(filename=LOG_PATH, format=CFG["loggy"]["log_format"], level=logging.NOTSET)

    LOGGING_LEVELS: Mapping[str, int] = {
        'NOTSET': 0, 'DEBUG': 10,
        'INFO': 20, 'WARNING': 30,
        'ERROR': 40, 'CRITICAL': 50
    }
    if ARGS.level.upper() not in LOGGING_LEVELS:
        print(f"Level '{ARGS.level}' not found, valid levels are: " + " ".join(LOGGING_LEVELS) + ".")
        return -1

    finalstr: str = ""
    if ARGS.context:
        finalstr = " ".join(ARGS.context) + ': '
    finalstr += " ".join(ARGS.message)
    logging.log(msg=finalstr,
                level=transform_verbosity(ARGS.level))
    print(f"Successfully logged to logfile: '{finalstr}'", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
