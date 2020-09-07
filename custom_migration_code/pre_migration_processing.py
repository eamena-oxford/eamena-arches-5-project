# Pre Migration Processing
import json
file = '../eamena/pkg/v3data/business_data/250_v3_heritage_places.jsonl'
with open (file) as jsonl:
        json_list = list(jsonl)
 
new_json_list=[]      
for json_str in json_list:
    # run through 1,2,3,4,5 and replace effect type and cert
    for i in range(1,6):
        json_str = json_str.replace(f"EFFECT_TYPE_{i}", "EFFECT_TYPE")
        json_str = json_str.replace(f"EFFECT_CERTAINTY_{i}", "EFFECT_CERTAINTY")
    new_json_list.append(json_str)

with open(file, 'w') as outfile:
        for item in new_json_list:
            item= json.loads(item)
            json.dump(item, outfile)
            outfile.write('\n')