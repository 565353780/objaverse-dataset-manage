import json
import pprint

with open('./objaverse/metadata.json', 'r') as f:
    data = json.load(f)

keys = list(data.keys())
print(len(keys))
pprint.pprint(data[keys[0]])
