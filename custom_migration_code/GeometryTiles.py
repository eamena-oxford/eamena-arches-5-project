import json
import uuid

def combine_geometry_tiles(in_file):

    print("Combining Geometry Tiles...")

    geometry = '3080eebe-c2c5-11ea-9026-02e7594ce0a0'
    with open (in_file) as jsonl:
            json_list = list(jsonl)

    new_json_list = []
    for json_str in json_list:
        data = json.loads(json_str)

        # find the correct tiles 
        tile_number = []
        for i,tile in enumerate(data['tiles']):
            tile['tile_number'] = i
            if tile['nodegroup_id'] == geometry:
                tile_number.append(i)

        for i,tile in enumerate(data['tiles']):   
            for number in tile_number[1:]:
                if tile['tile_number'] == number:
                    for uuid in data['tiles'][number]['data']:
                        data['tiles'][tile_number[0]]['data'][uuid] = data['tiles'][number]['data'][uuid]
                      
                          
        for tile in data['tiles'][:]:
            if tile['tile_number'] in tile_number[1:]:
                data['tiles'].remove(tile)
             
                    

        json_str = json.dumps(data)
        new_json_list.append(json_str)


    with open(in_file, 'w') as outfile:
        for item in new_json_list:
            item= json.loads(item)
            json.dump(item, outfile)
            outfile.write('\n')
    print("Complete!")