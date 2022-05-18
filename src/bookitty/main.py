#!/usr/bin/env python3
from argparse import ArgumentParser
from os import name
from types import SimpleNamespace
from pathlib import Path
import logging

# TODO: Add config file support
# TODO: Make this an installable package
# TODO: Make logs readable by the script itself (through an argument or smth)
# TODO: Less confusing code (idk functions for setting up config files[...])

def _arg_Parser() -> ArgumentParser:
	_parser = ArgumentParser(description="Logging for userspace programs", prog="Bookitty")

	_parser.add_argument('message',
						type=str,
						metavar="MESSAGE",
						nargs="+",
						help="Message that will be logged to (FILE)")

	_parser.add_argument('-c','--context',
						type=str,
						metavar="CONTX",
						nargs="+",
						help="Context for the message")

	_parser.add_argument('-l', '--level',
						type=str,
						metavar="LEVEL",
						default="INFO",
						help="Logging level")

	_parser.add_argument('--log-file',
						type=str,
						metavar="LOG_FILE",
						default=f"{Path.home()}/.local/state/bookitty/logfile.log" if name == 'posix' else f"{Path.home()}\\.bookitty\\logfile.log",
						help="The file where everything will be logged to")

	_parser.add_argument('--config-file',
						type=str,
						metavar="CONF_FILE",
						default=f"{Path.home()}/.config/bookitty/bookitty.conf" if name == 'posix' else f"{Path.home()}\\.bookitty\\bookitty.conf",
						)

	return _parser

def _parse_args(args: SimpleNamespace):
	# Setup config/log files
	log_file_path = Path(args.log_file)
	log_file_path.parents[0].mkdir(exist_ok=True)
	log_file_path.touch(exist_ok=True)

	conf_file_path = Path(args.config_file)
	conf_file_path.parents[0].mkdir(exist_ok=True)
	conf_file_path.touch(exist_ok=True)

	FORMAT="[%(asctime)s] [%(levelname)s] - %(msg)s"
	logging.basicConfig(filename=log_file_path, format=FORMAT)

	# Handle logging iteself
	LEVELS = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
	args.level = args.level.upper()

	if args.level in LEVELS:
		finalstr = ""
		if args.context != None:
			finalstr = " ".join(args.context) + ': '
		finalstr += " ".join(args.message)
		logging.log(msg=finalstr,
					level=(LEVELS.index(args.level) * 10))
	else:
		print(f"Level '{args.level}' not found, valid levels are: " + ", ".join(LEVELS) + ".")
		exit(1)
		

def main() -> None:
	args = _arg_Parser().parse_args()
	_parse_args(args)


if __name__ == "__main__":
	main()