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

def algo_list(flags):
	for algo in sorted(services.Service.get_supported_algos(), key=attrgetter("name")):
		print(algo.name)

def print_help(flags):
	flags.parser.print_help()

def main(args):
	# TODO: Arg parsing is ugly, redo that
	parser = argparse.ArgumentParser(prog=args[0])
	parser.set_defaults(handler=print_help, parser=parser)
	subparsers = parser.add_subparsers(help='sub-command help')

	parser_crack = subparsers.add_parser('crack', help='crack help')
	parser_crack.add_argument('-f', '--file', action='store_true', help='Indicates that ARG is a file storing hashes, one per')
	parser_crack.add_argument('-a', '--algo', required=True, action='store', help='Algorithm used to generate the hash')
	parser_crack.add_argument('ARG', help='Either the file or the hash to be cracked')
	parser_crack.set_defaults(handler=crack, parser=parser_crack)

	parser_algo = subparsers.add_parser('algo', help='crack help')
	parser_algo.set_defaults(handler=print_help, parser=parser_algo)

	algo_subparsers = parser_algo.add_subparsers(help='sub-commanh help')
	parser_algo_list = algo_subparsers.add_parser('list', help='list all available algorithms')
	parser_algo_list.set_defaults(handler=algo_list, parser=parser_algo_list)

	args = parser.parse_args(args[1:])
	args.handler(args)

if __name__ == "__main__":
    main(sys.argv)


