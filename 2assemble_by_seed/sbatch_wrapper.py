#!/usr/bin/env python


import os
import sys


counter = 0

while counter < 32:

	variables = dict(
	counter = counter) #name your output


	commands = """
	sbatch reassemblebatch{counter}
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)
	counter += 1









