#!/usr/bin/env python3

"""
Validate a config file against the config-schema.json
"""

from jsonschema import validate
import argparse
import json


def load_json_from_file(fileName, returnObj = True):
    ''' loads JSON from file and returns dict '''
    with open(fileName) as fh:
        contents = fh.read()
    return json.loads(contents) if returnObj else contents


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='validate a meta-data sheet config file', allow_abbrev=False)
    parser.add_argument('-s', '--schemaFile', help="full path to config-schema.json", required=True)
    parser.add_argument('-c', '--configFile', help="full path to config file to be validated", required=True)
    args = parser.parse_args()

    
    schema = load_json_from_file(args.schemaFile, True)
    config = load_json_from_file(args.configFile, True)
    
    # print(json.dumps(schema, indent=2))

    schema = {
        "additionalProperties": False,
        "description": "Validator specification",
        "properties": {
            "type": {
                "description": "type of validator",
                "type": "string"
            },
        },
        "required": [
            "type"
        ],
        "type": "object"
    }
    
    validate(instance=config, schema=schema)