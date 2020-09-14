from RSTiles import remove_rs_tiles
from AATiles import aa_tree_restructure
from GeographyTiles import combine_geography_tiles
from GeometryTiles import combine_geometry_tiles
from GridSquareIds import findreplace_gridid
#from PeopleOrganisations import findreplace_people
from InitialInfo import initialising

# 1. Load in jsonl file (this code would have to change for json)
in_file = '../eamena/pkg/business_data/v3resources-all-2020-08-18-Heritage Place.jsonl'

initialising(in_file)

# RULE 1: Combine all Resource Summary Tiles (delete the rest)
remove_rs_tiles(in_file)

# RULE 2: Combine Gemoetery Tiles (if >1 GPE tile put data into first)
combine_geometry_tiles(in_file)

# RULE 3: Combine all Geography Tiles (delete the rest)
combine_geography_tiles(in_file)

# RULE 4: If there is a subperiod copy and attach period certainty

# RULE 5: Combine all Archaeological Assessment Tiles and reconfigure tree
aa_tree_restructure(in_file)

# RULE 6: Find and replace Gridsquare names with UUIDs
grid_file = '../eamena/pkg/business_data/v3resources-all-2020-08-18-Grid Square.jsonl'
findreplace_gridid(in_file, grid_file)

# RULE 7: Find and replace People names with UUIDs
# findreplace_people(in_file, people_csv_file)
