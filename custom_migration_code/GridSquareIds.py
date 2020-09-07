import json
import pandas as pd 

def findreplace_gridid(in_file, grid_file):
	print("Finding Grid Squares and replacing with new UUIDS...")
	with open (file) as jsonl:
        json_list = list(jsonl)

    new_json_list = []
    for json_str in json_list:
        data = json.loads(json_str)
		grid_sqaures = pd.read_csv(grid_file)
		for uuid, grid_id in zip(grid_sqaures['ResourceID'], df['Grid ID']):
			json_str = json_str.replace(grid_id,uuid)
		new_json_list.append(json_str)


    with open(in_file, 'w') as outfile:
        for item in new_json_list:
            item= json.loads(item)
            json.dump(item, outfile)
            outfile.write('\n')