#!/usr/bin/env python

'''
transform ISA-tab to ISA-json and output
'''
from __future__ import print_function
import isatools
import isa.isatab2json as isatab2json
from isa.custom_isatab import validate as isa_validate
import logging

import argparse
import sys
import os
import json

def convert():
    '''
    validate & convert the isa-tab file
    '''
    invalid = False
    isaJson = isatab2json.convert(args.tabdir, use_new_parser=True,  config_dir=args.config) \
      if args.config \
      else isatab2json.convert(args.tabdir, use_new_parser=True)

    with open(args.output, 'w') as of:
        print(json.dumps(isaJson, indent=4, sort_keys=True, separators=(',', ': ')), file=of)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate an ISA-TAB')
    parser.add_argument('-t', '--tabdir', help="full path to directory containing ISA-TAB files", required=True)
    parser.add_argument('-c', '--config', help="full path to directory containing config files", required=False)
    parser.add_argument('-o', '--output', help="full path to output file", required=True)
    args = parser.parse_args()

    convert()