import json
import pandas as pd 

def findreplace_people(in_file, people_file):
	""" This function requires a csv 'people_file' which contains
	Arches UUIDs and the assoicated people/organisation name to be replace"""

	print("Finding People/Organisaitons and replacing them with new UUIDs...")

	with open (file) as jsonl:
        json_list = list(jsonl)

    new_json_list = []
    for json_str in json_list:
        data = json.loads(json_str)
		people_data = pd.read_csv(people_file)
		for uuid, name in zip(people_data['ResourceID'], df['Name']):
			json_str = json_str.replace(name,uuid)
		new_json_list.append(json_str)


    with open(in_file, 'w') as outfile:
        for item in new_json_list:
            item= json.loads(item)
            json.dump(item, outfile)
            outfile.write('\n')