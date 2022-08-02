# https://fedingo.com/how-to-read-yaml-file-to-dict-in-python/

import yaml

with open("dict_def.yaml", 'r') as stream:
    try:
        parsed_yaml=yaml.safe_load(stream)
        print(parsed_yaml)
    except yaml.YAMLError as exc:
        print(exc)

