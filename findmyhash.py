#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from operator import attrgetter

import findmyhash
from findmyhash import services
from findmyhash.cracker import Cracker
from findmyhash.algo import Algo

# TODO: redo the google search if not found

def crack(flags):
	to_crack = None
	if flags.file is True:
		to_crack = open(flags.ARG, "r", encoding="utf-8")
	else:
		to_crack = [flags.ARG]

	try:
		c = Cracker(to_crack)
		c.crack(Algo(flags.algo.lower()))
	finally:
		try:
			to_crack.close()
		except AttributeError:
			pass

def algo_list():
	for algo in sorted(services.Service.get_supported_algos(), key=attrgetter("name")):
		print(algo.name)

def algo(flags):
	if flags.COMMAND == "list":
		algo_list()

def main(args):
	# TODO: Arg parsing is ugly, redo that
	parser = argparse.ArgumentParser(prog=args[0])
	subparsers = parser.add_subparsers(help='sub-command help')

	parser_crack = subparsers.add_parser('crack', help='crack help')
	parser_crack.add_argument('-f', '--file', action='store_true', help='Indicates that ARG is a file storing hashes, one per')
	parser_crack.add_argument('-a', '--algo', required=True, action='store', help='Algorithm used to generate the hash')
	parser_crack.add_argument('ARG', help='Either the file or the hash to be cracked')
	parser_crack.set_defaults(func=crack)

	parser_algo = subparsers.add_parser('algo', help='crack help')
	parser_algo.add_argument('COMMAND', help='command to execute', choices=["list"])
	parser_algo.set_defaults(func=algo)

	args = parser.parse_args(args[1:])
	args.func(args)

if __name__ == "__main__":
    main(sys.argv)


