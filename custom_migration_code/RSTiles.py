import json
import uuid

# 1. Load in jsonl file (this code would have to change for json)
    
def remove_rs_tiles(in_file):

    print("Removing extra Resource Summary Tiles and moving data...")
    with open (in_file) as jsonl:
            json_list = list(jsonl)

    # Tile UUIDS
    RS = '34cfe98f-c2c0-11ea-9026-02e7594ce0a0'

    # 2. Post-migration EAMENA data processing 
    new_json_list = []
    for json_str in json_list:
        data = json.loads(json_str)

    # RULE 1: Combine all Resource Summary Tiles (delete the rest)
        
        # identify RS tiles 
        RS_tile_ids = []
        for tile in data['tiles']:
            if tile['nodegroup_id'] == RS:
                RS_tile_ids.append(tile['tileid'])
        
        
        # Find children tiles 
        RS_children_tile_ids = []
        for tile in data['tiles']:
            if tile['parenttile_id'] in RS_tile_ids:
                RS_children_tile_ids.append(tile['tileid'])

        #  Delete all but first RS tile
        for tile in data['tiles'][:]:
            if tile['tileid'] in RS_tile_ids[1:]:
                data['tiles'].remove(tile) 

        #Assign parent RS tile - some records have no RS.
        try:
            RS_parent_tile = RS_tile_ids[0]
        except:
            RS_parent_tile = None
           
        
        # 3. Assign all children to have the one RS parent
        for i,tile in enumerate(data['tiles']):
             if tile['tileid'] in RS_children_tile_ids:
                    tile['parenttile_id'] = RS_parent_tile
        
        # 4. Delete empty children that should contain data...
        data_nodegroup_ids = [
            '34cfe9dd-c2c0-11ea-9026-02e7594ce0a0',
            '34cfe9dd-c2c0-11ea-9026-02e7594ce0a0',
            '34cfe9dd-c2c0-11ea-9026-02e7594ce0a0',
            '34cfe9ad-c2c0-11ea-9026-02e7594ce0a0',
            '34cfe9ef-c2c0-11ea-9026-02e7594ce0a0',
            ]

        for tile in data['tiles']:
            if tile['parenttile_id'] == RS_parent_tile and tile['data'] == {}:#and tile['nodegroup_id'] in data_nodegroup_ids:
                data['tiles'].remove(tile)


        json_str = json.dumps(data)
        new_json_list.append(json_str)


    with open(in_file, 'w') as outfile:
        for item in new_json_list:
            item= json.loads(item)
            json.dump(item, outfile)
            outfile.write('\n')

    print("Complete!")

# RULE 2: Combine Gemoetery Tiles (if >1 GPE tile put data into first)
# RULE 3: Combine all Geography Tiles (delete the rest)
# RULE 4: If there is a subperiod copy and attach period certainty
# RULE 5: Combine all Archaeological Assessment Tiles and reconfigure tree

# RULE 6: Find and replace Gridsquare names with UUIDs
# RULE 7: Find and replace People names with UUIDs

