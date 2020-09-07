import json
import uuid


def aa_tree_restructure(in_file):

	print("Reorganising Archaeological Assement Tree...")
	nodes = ["34cfe9b3-c2c0-11ea-9026-02e7594ce0a0", 
	        "34cfea13-c2c0-11ea-9026-02e7594ce0a0",
	         "34cfe9fe-c2c0-11ea-9026-02e7594ce0a0",
	        "34cfe9b0-c2c0-11ea-9026-02e7594ce0a0"]
	AA = "34cfe9b3-c2c0-11ea-9026-02e7594ce0a0"
	SFA = "34cfea13-c2c0-11ea-9026-02e7594ce0a0"
	SFIB = "34cfe9fe-c2c0-11ea-9026-02e7594ce0a0"
	SFFTB = "34cfe9b0-c2c0-11ea-9026-02e7594ce0a0"

	# ONLY 1 AA TILE


	with open(in_file) as jsonl:
	    json_list = list(jsonl)

	new_json_list = []
	for json_str in json_list:
	    data = json.loads(json_str)

	    
	    # 1. Identify AA tiles
	    AA_tiles = []
	    for i,tile in enumerate(data['tiles']):
	        tile['tile_number'] = i
	        if tile['nodegroup_id'] == AA:
	            AA_tiles.append(i)


	    # 2. Delete all but first AA tile         
	    for tile in data['tiles'][:]:
	        if tile['tile_number'] in AA_tiles[1:]:
	            data['tiles'].remove(tile)

	     # reassign tile numbers           
	    for i,tile in enumerate(data['tiles']):
	        tile['tile_number'] = i

	    try:
	    	AA_parent_tile = data['tiles'][AA_tiles[0]]['tileid']
	    except: 
	    	AA_parent_tile = None

	    # 3. Assign all SFAs to have the one AA parent
	    for i,tile in enumerate(data['tiles']):
	         if tile['nodegroup_id'] == SFA:
	                tile['parenttile_id'] = AA_parent_tile
	           

	    #4. Find empty SFA? . Assign SFFTB or SFIBs with no parents a SFA tile
	    childless_SFA_tiles = []
	    for i,tile in enumerate(data['tiles']):
	        if tile['nodegroup_id'] == SFA:
	            SFA_tile = tile['tileid']
	            num_children = 0
	            for child in data['tiles']:
	                if child['parenttile_id'] == SFA_tile:
	                    num_children += 1
	            if num_children == 0:
	                childless_SFA_tiles.append(tile['tile_number'])


	    # delete all empty SFAs?    
	    for tile in data['tiles']:
	        if tile['tile_number'] in childless_SFA_tiles:
	            data['tiles'].remove(tile)
	               

	     # reassign tile numbers           
	    for i,tile in enumerate(data['tiles']):
	        tile['tile_number'] = i


	    # Finds SFFTB or SFIB tiles with no parents 
	    parentless_SFFTB_SFIB_tiles = []
	    for i,tile in enumerate(data['tiles']):
	        if tile['nodegroup_id'] in [SFFTB, SFIB]:
	            if tile['parenttile_id'] == None:
	                parentless_SFFTB_SFIB_tiles.append(tile['tile_number'])

	    # Creates each of these a new parent SFA
	    for parentless_tile in parentless_SFFTB_SFIB_tiles:
	        # 1. generate tile id
	        new_id = str(uuid.uuid4())
	        

	        # 2. generate new tile with that id
	        new_tile = {
	        'data': {},
	        'nodegroup_id': SFA,
	        'parenttile_id': AA,
	        'provisionaledits': None,
	        'resourceinstance_id': '0d304840-51ec-4adb-960e-bbdf2f7da060',
	        'sortorder': 0,
	        'tileid': new_id,
	        'tile_number': len(data['tiles'])}
	        # 3. add the new tile
	       
	        data['tiles'].append(new_tile)
	        #4 assign the parentless SFFTB or SFIB to this new tile
	        data['tiles'][parentless_tile]['parenttile_id'] = new_id
	        
	    json_str = json.dumps(data)
	    new_json_list.append(json_str)
	    

	with open(in_file, 'w') as outfile:
	    for item in new_json_list:
	        item= json.loads(item)
	        json.dump(item, outfile)
	        outfile.write('\n')
	print("Complete!")