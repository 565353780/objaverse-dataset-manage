import json
import pprint

with open('/home/chli/chLi/Dataset/Objaverse/metadata.json', 'r') as f:
    data = json.load(f)

keys = list(data.keys())
print(len(keys))
pprint.pprint(data[keys[0]])
