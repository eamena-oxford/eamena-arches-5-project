import json

def findreplace_gridid(in_file, grid_file):
    print("Finding Grid Squares and replacing with new UUIDS...")
    with open(in_file) as jsonl:
        json_list = list(jsonl)

    new_json_list = []
    map = {}
    with open(grid_file) as jsonl:
        for item in list(jsonl):
            gridsquare = json.loads(item)
            gridresid = gridsquare['resourceinstance']['resourceinstanceid']
            for tile in gridsquare['tiles']:
                gridid = tile['data']['b3628db0-742d-11ea-b4d0-02e7594ce0a0'] # This is the UUID for 'Grid ID' in the Heritage Place model
                map[gridid] = gridresid

    keys = map.keys()
    for json_str in json_list:
        data = json.loads(json_str)
        new_tiles = []
        for tile in data['tiles']:
            new_data = tile['data']
            for data_item in tile['data'].keys():
                check_value = tile['data'][data_item]
                if isinstance(check_value, str):
                    if check_value in keys:
                        check_value = map[check_value]
                new_data[data_item] = check_value
            tile['data'] = new_data
            new_tiles.append(tile)
        data['tiles'] = new_tiles
        new_json_list.append(json.dumps(data))

    with open(in_file, 'w') as outfile:
        for item in new_json_list:
            item= json.loads(item)
            json.dump(item, outfile)
            outfile.write('\n')
    print("Complete!")
