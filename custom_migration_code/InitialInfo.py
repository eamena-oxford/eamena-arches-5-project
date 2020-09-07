import json
import uuid


def initialising(in_file):

	print("Initialising...")

	with open(in_file) as jsonl:
	    json_list = list(jsonl)

	print(f'Processing {len(json_list)} jsonl records...')
